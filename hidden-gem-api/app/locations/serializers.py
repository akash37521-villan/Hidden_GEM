from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Standard JSON serializer for Location.

    Accepts `latitude` and `longitude` as separate write-only fields
    (matching the client-friendly API contract) and builds the PostGIS
    Point internally. On read, exposes `latitude` / `longitude` as
    separate floats — easier to consume than GeoJSON for simple clients.
    """

    latitude = serializers.FloatField(
        write_only=False,
        required=False,
        help_text="Latitude in decimal degrees (WGS84).",
    )
    longitude = serializers.FloatField(
        write_only=False,
        required=False,
        help_text="Longitude in decimal degrees (WGS84).",
    )
    lat = serializers.FloatField(
        write_only=True,
        required=False,
        help_text="Alias for latitude.",
    )
    lng = serializers.FloatField(
        write_only=True,
        required=False,
        help_text="Alias for longitude.",
    )
    added_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Location
        fields = (
            "id",
            "title",
            "description",
            "category",
            "image_url",
            "latitude",
            "longitude",
            "lat",
            "lng",
            "added_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "added_by", "created_at", "updated_at")

    def to_representation(self, instance):
        """Convert PointField back to separate lat/lng floats on read."""
        rep = super().to_representation(instance)
        # Clean up write-only aliases if they appear
        rep.pop("lat", None)
        rep.pop("lng", None)
        if instance.coordinates:
            # PointField stores as (longitude, latitude) per GIS convention (x=lng, y=lat)
            rep["latitude"] = instance.coordinates.y
            rep["longitude"] = instance.coordinates.x
            rep["lat"] = instance.coordinates.y
            rep["lng"] = instance.coordinates.x
        return rep

    def validate(self, attrs):
        """Accept latitude/longitude or lat/lng shorthand."""
        lat = attrs.get("latitude") or attrs.get("lat")
        lng = attrs.get("longitude") or attrs.get("lng")

        if lat is None and self.instance and self.instance.coordinates:
            lat = self.instance.coordinates.y
        if lng is None and self.instance and self.instance.coordinates:
            lng = self.instance.coordinates.x

        if lat is None or lng is None:
            raise serializers.ValidationError(
                "Both latitude (or lat) and longitude (or lng) are required."
            )
        if not (-90 <= lat <= 90):
            raise serializers.ValidationError({"latitude": "Must be between -90 and 90."})
        if not (-180 <= lng <= 180):
            raise serializers.ValidationError({"longitude": "Must be between -180 and 180."})

        # Canonicalize to latitude and longitude
        attrs["latitude"] = lat
        attrs["longitude"] = lng
        attrs.pop("lat", None)
        attrs.pop("lng", None)
        return attrs

    def create(self, validated_data):
        lat = validated_data.pop("latitude")
        lng = validated_data.pop("longitude")
        validated_data["coordinates"] = Point(x=lng, y=lat, srid=4326)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.pop("latitude", None)
        lng = validated_data.pop("longitude", None)
        if lat is not None and lng is not None:
            validated_data["coordinates"] = Point(x=lng, y=lat, srid=4326)
        return super().update(instance, validated_data)


class NearbyLocationSerializer(LocationSerializer):
    """
    Extends LocationSerializer to include `distance_m` and `distance_km`
    computed from PostGIS ST_Distance via `.annotate()`.
    """
    distance_m = serializers.SerializerMethodField()
    distance_km = serializers.SerializerMethodField()

    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ("distance_m", "distance_km")

    def get_distance_m(self, obj) -> float | None:
        distance = getattr(obj, "distance", None)
        if distance is None:
            return None
        return round(distance.m, 1)

    def get_distance_km(self, obj) -> float | None:
        distance = getattr(obj, "distance", None)
        if distance is None:
            return None
        return round(distance.km, 1)
