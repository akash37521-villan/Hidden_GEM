"""
Management command to seed authentic hidden gems across Solan, Chail,
Dagshai, Kuthar, Dolanji, Kasauli, Subathu, Waknaghat, and Shimla
within a 100 km radius of Solan, Himachal Pradesh.
"""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from app.locations.models import Location
from app.users.models import CustomUser


PLACES_DATA = [
    {
        "title": "Dagshai Cantt Pine Trail",
        "category": Location.Category.MOUNTAIN_TRAIL,
        "description": "A 4 km serene deodar trail winding through the historic 1847 cantonment cemetery and silent pine ridges.",
        "lat": 30.8845,
        "lng": 77.0512,
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "guide_username": "arun_solan",
    },
    {
        "title": "Yungdrung Bon Monastery, Dolanji",
        "category": Location.Category.MONASTERY,
        "description": "One of the few Bon monasteries in the world, preserving ancient pre-Buddhist Tibetan spiritual traditions and colorful prayer halls.",
        "lat": 30.8491,
        "lng": 77.1652,
        "image_url": "https://images.unsplash.com/photo-1582650625119-3a31f8418365?auto=format&fit=crop&w=800&q=80",
        "guide_username": "tenzin_dolanji",
    },
    {
        "title": "Phagu's Traditional Dham",
        "category": Location.Category.LOCAL_EATERY,
        "description": "70-year-old family dhaba in Old Solan serving authentic Himachali madra, sepu badi, and khatta cooked in brass vessels.",
        "lat": 30.9068,
        "lng": 77.0982,
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=800&q=80",
        "guide_username": "savita_food",
    },
    {
        "title": "Kuthar Fort & Spring Pools",
        "category": Location.Category.COLONIAL_HERITAGE,
        "description": "An 800-year-old fort complex with freshwater mountain springs, wooden carved pillars, and royal Rajput-Pahadi battlements.",
        "lat": 30.9812,
        "lng": 76.9634,
        "image_url": "https://images.unsplash.com/photo-1599818816930-3f7b823b8fdd?auto=format&fit=crop&w=800&q=80",
        "guide_username": "bhupesh_heritage",
    },
    {
        "title": "Chail Wildlife Deep Pine Sanctuary",
        "category": Location.Category.SANCTUARY,
        "description": "Dense oak, cedar, and chir pine reserve sheltering Himalayan cheer pheasants, barking deer, and silent walking tracks.",
        "lat": 30.9654,
        "lng": 77.2145,
        "image_url": "https://images.unsplash.com/photo-1511497584788-87676104235f?auto=format&fit=crop&w=800&q=80",
        "guide_username": "meena_flora",
    },
    {
        "title": "Gilbert Trail Cliff Walk, Kasauli",
        "category": Location.Category.MOUNTAIN_TRAIL,
        "description": "A narrow 1.5 km cliffside path hugging steep mountain drops, renowned for valley fog rolling up from the plains and rich birdlife.",
        "lat": 30.8978,
        "lng": 76.9682,
        "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80",
        "guide_username": "rajan_trails",
    },
    {
        "title": "Sadhupul Riverbed Stream Dining",
        "category": Location.Category.LOCAL_EATERY,
        "description": "Dine on rustic benches set directly into the ankle-deep crystal current of the Ashwani river beneath shaded pine slopes.",
        "lat": 30.9856,
        "lng": 77.1352,
        "image_url": "https://images.unsplash.com/photo-1508873696983-2df5703bc20d?auto=format&fit=crop&w=800&q=80",
        "guide_username": "savita_food",
    },
    {
        "title": "Karol Tibba Summit & Pandava Cave",
        "category": Location.Category.MOUNTAIN_TRAIL,
        "description": "Highest peak in the Solan range (2,240 m). The unmarked trail leads past ancient Pandava meditation caves to a 360° summit vista.",
        "lat": 30.9234,
        "lng": 77.1218,
        "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
        "guide_username": "rajan_trails",
    },
    {
        "title": "Mohan Meakin Brewery (1855)",
        "category": Location.Category.COLONIAL_HERITAGE,
        "description": "Asia's oldest operating brewery featuring red-brick Victorian distillery architecture nestled in a terraced pine valley.",
        "lat": 30.9021,
        "lng": 77.0911,
        "image_url": "https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?auto=format&fit=crop&w=800&q=80",
        "guide_username": "bhupesh_heritage",
    },
    {
        "title": "Chadwick Falls Glen, Shimla",
        "category": Location.Category.MOUNTAIN_TRAIL,
        "description": "An 86-meter cascade tucked deep in the ancient cedar sanctuary of the Glen forest, far below Mall Road.",
        "lat": 31.1182,
        "lng": 77.1354,
        "image_url": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=800&q=80",
        "guide_username": "rajan_trails",
    },
    {
        "title": "Shoolini Mata Ancient Mandir",
        "category": Location.Category.COLONIAL_HERITAGE,
        "description": "The sacred hilltop shrine that gives Solan its name. Renowned for its calm morning hymns and valley views.",
        "lat": 30.9082,
        "lng": 77.1065,
        "image_url": "https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=800&q=80",
        "guide_username": "meena_flora",
    },
    {
        "title": "Barog Tunnel 33 (UNESCO World Heritage)",
        "category": Location.Category.COLONIAL_HERITAGE,
        "description": "The longest straight tunnel (1,143 m) on the historic 1903 Kalka-Shimla rail line, rich with railway folklore.",
        "lat": 30.8931,
        "lng": 77.0818,
        "image_url": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
        "guide_username": "bhupesh_heritage",
    }
]


class Command(BaseCommand):
    help = "Seeds authentic hidden gems within 100 km of Solan with real Unsplash photography."

    def handle(self, *args, **options):
        self.stdout.write("Seeding local guides and hidden gems...")

        guides_meta = {
            "arun_solan": ("Arun Verma", "Local Guide (Solan)"),
            "tenzin_dolanji": ("Tenzin Norbu", "Monastic Culture Guide"),
            "savita_food": ("Savita Sharma", "Culinary Heritage Guide"),
            "bhupesh_heritage": ("Bhupesh Thakur", "Historic Architecture Guide"),
            "meena_flora": ("Meena Dogra", "Botanical & Sanctuary Guide"),
            "rajan_trails": ("Rajan Singh", "Himalayan Ridge Tracker"),
        }

        guide_objs = {}
        for username, (first_name, role_title) in guides_meta.items():
            user, _ = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "role": CustomUser.Role.LOCAL_GUIDE,
                    "email": f"{username}@hiddengem.in",
                },
            )
            guide_objs[username] = user

        created_count = 0
        updated_count = 0

        for item in PLACES_DATA:
            point = Point(x=item["lng"], y=item["lat"], srid=4326)
            guide = guide_objs.get(item["guide_username"], list(guide_objs.values())[0])

            loc, created = Location.objects.update_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "category": item["category"],
                    "image_url": item.get("image_url", ""),
                    "coordinates": point,
                    "added_by": guide,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {len(PLACES_DATA)} locations within 100 km of Solan! "
                f"({created_count} created, {updated_count} updated)"
            )
        )
