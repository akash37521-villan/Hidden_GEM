from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from .models import Location
from .serializers import LocationSerializer, NearbyLocationSerializer
from .permissions import IsLocalGuideOrReadOnly


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet providing full CRUD for Location plus a custom `nearby` action.

    Endpoint map:
        POST   /api/locations/               → create (guides only)
        GET    /api/locations/               → list all
        GET    /api/locations/{id}/          → retrieve one
        PUT    /api/locations/{id}/          → update (owner guide only)
        DELETE /api/locations/{id}/          → destroy (owner guide only)
        GET    /api/locations/nearby/        → geospatial radius search
    """

    queryset = Location.objects.select_related("added_by").all()
    serializer_class = LocationSerializer
    permission_classes = [IsLocalGuideOrReadOnly]

    def perform_create(self, serializer):
        """Automatically assign the currently authenticated guide as added_by."""
        serializer.save(added_by=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        url_path="nearby",
        permission_classes=[permissions.AllowAny],
    )
    def nearby(self, request):
        """
        GET /api/locations/nearby/?lat=<float>&lng=<float>&radius=<km>

        Returns all Locations within `radius` kilometres of the given
        coordinates, annotated with their exact distance and ordered
        nearest-first.

        Implementation notes:
        - Point(x=lng, y=lat): GIS convention is (longitude, latitude).
        - geography=True on the model means ST_DWithin works in METRES,
          so we convert km → m for the `D(m=...)` filter.
        - .annotate(distance=Distance(...)) adds the computed distance so
          the serializer can surface it without a second DB round-trip.
        - ST_DWithin uses a spatial index (GIST) automatically — O(log n).
        """
        # ── 1. Parse & validate query parameters ───────────────────────────
        try:
            lat = float(request.query_params["lat"])
            lng = float(request.query_params["lng"])
        except (KeyError, ValueError):
            return Response(
                {"error": "`lat` and `lng` query parameters are required and must be numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            radius_km = float(request.query_params.get("radius", 100))
        except ValueError:
            return Response(
                {"error": "`radius` must be a number (kilometres)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return Response(
                {"error": "Invalid coordinates. lat ∈ [-90,90], lng ∈ [-180,180]."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if radius_km <= 0 or radius_km > 500:
            return Response(
                {"error": "`radius` must be between 0 and 500 km."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── 2. Build the reference point ────────────────────────────────────
        # srid=4326 must match the PointField srid on the model.
        origin = Point(x=lng, y=lat, srid=4326)

        # ── 3. Geospatial query ─────────────────────────────────────────────
        # D(m=...) creates a Distance object in metres.
        # geography=True on the field means PostGIS interprets this as metres
        # on the Earth's surface (great-circle distance), not flat-earth degrees.
        radius_m = radius_km * 1000

        locations = (
            Location.objects.filter(
                coordinates__dwithin=(origin, D(m=radius_m))
            )
            .annotate(distance=Distance("coordinates", origin))
            .select_related("added_by")
            .order_by("distance")
        )

        # ── 4. Optional category filter ─────────────────────────────────────
        category = request.query_params.get("category")
        if category:
            locations = locations.filter(category=category)

        # ── 5. Paginate & serialize ─────────────────────────────────────────
        page = self.paginate_queryset(locations)
        if page is not None:
            serializer = NearbyLocationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NearbyLocationSerializer(locations, many=True)
        return Response(serializer.data)
