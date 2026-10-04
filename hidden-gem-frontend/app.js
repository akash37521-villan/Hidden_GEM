const { createClient } = supabase;
const supabaseUrl = 'https://drygpobnfwgfamfraamc.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxxeXdjdnl4bnhqZnZpdHZ1emdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTEwODc4NjYsImV4cCI6MjEwNjY2Mzg2Nn0.8MMN5cgfobKjIKIwBSwbGCxuBRX61ww9wc9eeCgppmY';
const supabaseClient = createClient(supabaseUrl, supabaseKey);
/**
 * Hidden Gem & Regional Explorer — Solan & 100 km Radius
 * Core client application: Handles Leaflet.js map initialization,
 * PostGIS spatial API communication, radius filtering, and DOM updates.
 */

// ── Geographic Constants ───────────────────────────────────────────────
const SOLAN_CENTER = [30.9045, 77.0967]; // Latitude, Longitude for Solan, HP
const DEFAULT_RADIUS_KM = 100;

// Default fallback mountain landscape (Himachal Pradesh pine ridges)
const FALLBACK_MOUNTAIN_IMAGE = "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80";

// Curated Verified Photography from Wikimedia Commons & Authentic Himachal Regional Archives
const INITIAL_LOCATIONS = [
  {
    id: 1,
    title: "Dagshai Cantt & Museum",
    category: "Colonial Heritage",
    description: "Historic 1847 stone military jail and heritage museum framed by old-growth chir pine ridges.",
    latitude: 30.8845,
    longitude: 77.0512,
    distance_km: 14.2,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/3/34/Dagshai_Museum_Front_Gate.jpg",
    added_by: "Arun Verma (Local Resident)"
  },
  {
    id: 2,
    title: "Yungdrung Bon Monastery, Dolanji",
    category: "Monastery",
    description: "Authentic Bon monastic complex (Menri) preserving pre-Buddhist Tibetan spiritual wisdom, thangka art, and prayer wheels.",
    latitude: 30.8491,
    longitude: 77.1652,
    distance_km: 18.6,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/d/d0/Menri_Feb_2016.jpg",
    added_by: "Tenzin Norbu (Dolanji Guide)"
  },
  {
    id: 3,
    title: "Phagu's Traditional Dham",
    category: "Local Eatery",
    description: "70-year-old family dhaba in Old Solan serving authentic Himachali madra, sepu badi, and khatta cooked in brass vessels.",
    latitude: 30.9068,
    longitude: 77.0982,
    distance_km: 1.2,
    image_url: "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=800&q=80",
    added_by: "Savita Sharma (Culinary Resident)"
  },
  {
    id: 4,
    title: "Kuthar Fort & Spring Pools",
    category: "Colonial Heritage",
    description: "An 800-year-old stone fortress estate near Subathu featuring freshwater mountain springs, wooden carved pillars, and royal battlements.",
    latitude: 30.9812,
    longitude: 76.9634,
    distance_km: 24.1,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/4/46/Entrance_of_palace_of_Kuthar_Princely_State%2CHimachal_Prades%2CIndia.jpg",
    added_by: "Bhupesh Thakur (Heritage Historian)"
  },
  {
    id: 5,
    title: "Chail Wildlife Deep Pine Sanctuary",
    category: "Sanctuary",
    description: "Dense oak, cedar, and chir pine reserve sheltering Himalayan cheer pheasants, barking deer, and silent walking tracks.",
    latitude: 30.9654,
    longitude: 77.2145,
    distance_km: 38.5,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/5/5e/Chailhill.jpg",
    added_by: "Meena Dogra (Botanical Guide)"
  },
  {
    id: 6,
    title: "Gilbert Trail Cliff Walk, Kasauli",
    category: "Mountain Trail",
    description: "A narrow 1.5 km cliffside path hugging steep mountain drops, renowned for valley fog rolling up from the plains and rich birdlife.",
    latitude: 30.8978,
    longitude: 76.9682,
    distance_km: 28.0,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/1/1d/Kasauli_hills.jpg",
    added_by: "Rajan Singh (Trail Specialist)"
  },
  {
    id: 7,
    title: "Sadhupul Riverbed Stream Dining",
    category: "Local Eatery",
    description: "Dine on rustic benches set directly into the ankle-deep crystal current of the Ashwani river beneath shaded pine slopes.",
    latitude: 30.9856,
    longitude: 77.1352,
    distance_km: 17.8,
    image_url: "https://images.unsplash.com/photo-1508873696983-2df5703bc20d?auto=format&fit=crop&w=800&q=80",
    added_by: "Rajan Singh (Trail Specialist)"
  },
  {
    id: 8,
    title: "Karol Tibba Summit & Pandava Cave",
    category: "Mountain Trail",
    description: "Highest peak in the Solan range (2,240 m). The unmarked trail leads past ancient Pandava meditation caves to a 360° summit vista.",
    latitude: 30.9234,
    longitude: 77.1218,
    distance_km: 16.3,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/6/67/Solan_panorama.jpg",
    added_by: "Rajan Singh (Trail Specialist)"
  },
  {
    id: 9,
    title: "Mohan Meakin Brewery (1855)",
    category: "Colonial Heritage",
    description: "Asia's oldest operating brewery featuring red-brick Victorian distillery architecture nestled in a terraced pine valley.",
    latitude: 30.9021,
    longitude: 77.0911,
    distance_km: 2.5,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/6/6a/Kasauli_Brewery_03.jpg",
    added_by: "Bhupesh Thakur (Heritage Historian)"
  },
  {
    id: 10,
    title: "Chadwick Falls Glen, Shimla",
    category: "Mountain Trail",
    description: "An 86-meter cascade tucked deep in the ancient cedar sanctuary of the Glen forest, far below Mall Road.",
    latitude: 31.1182,
    longitude: 77.1354,
    distance_km: 48.2,
    image_url: "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=800&q=80",
    added_by: "Rajan Singh (Trail Specialist)"
  },
  {
    id: 11,
    title: "Jatoli Shiva Ancient Temple",
    category: "Colonial Heritage",
    description: "Asia's highest temple spire (Dravidian-Himalayan stone carving) perched on a peaceful pine slope south of Solan.",
    latitude: 30.8655,
    longitude: 77.1264,
    distance_km: 7.5,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/f/fe/Jatoli_Shiv_Temple.jpg",
    added_by: "Arun Verma (Local Resident)"
  },
  {
    id: 12,
    title: "Barog Station (UNESCO World Heritage)",
    category: "Colonial Heritage",
    description: "Historic 1903 colonial wooden shingle railway station and Tunnel 33 on the Kalka-Shimla heritage line.",
    latitude: 30.8931,
    longitude: 77.0818,
    distance_km: 8.9,
    image_url: "https://upload.wikimedia.org/wikipedia/commons/c/cf/BarogRailwayStation_Barog_HP_PICT0342.jpg",
    added_by: "Bhupesh Thakur (Heritage Historian)"
  }
];

// ── Application State ──────────────────────────────────────────────────
let appState = {
  radiusKm: DEFAULT_RADIUS_KM,
  activeCategory: "All",
  searchQuery: "",
  locations: [...INITIAL_LOCATIONS],
  map: null,
  radiusCircle: null,
  markerLayerGroup: null,
  markerMap: new Map() // maps location id -> Leaflet marker instance
};

// ── 1. Map Initialization (Leaflet.js) ─────────────────────────────────
function initMap() {
  /**
   * Initialize Leaflet map centered on Solan (30.9045° N, 77.0967° E).
   * Uses CartoDB Voyager tiles for an earthy, high-contrast palette
   * that seamlessly complements "Warm Oatmeal" and "Deep Pine Green".
   */
  appState.map = L.map("map", {
    center: SOLAN_CENTER,
    zoom: 10,
    scrollWheelZoom: false, // Prevents accidental scroll hijacking on page read
  });

  // Base tile layer (OpenStreetMap)
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(appState.map);

  // Solan Hub Marker (Distinct Deep Pine Green circle)
  const solanHubIcon = L.divIcon({
    className: "solan-hub-pin",
    html: `
      <div style="background-color: #1A362D; color:#FFF; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:16px; border:2px solid #FFF; box-shadow:0 4px 12px rgba(0,0,0,0.3);">
        ⛰
      </div>
    `,
    iconSize: [34, 34],
    iconAnchor: [17, 17],
  });

  L.marker(SOLAN_CENTER, { icon: solanHubIcon })
    .addTo(appState.map)
    .bindPopup("<strong>Solan Town Center (Hub)</strong><br>Center point for 100 km exploratory radius.");

  // Group for dynamic location markers
  appState.markerLayerGroup = L.layerGroup().addTo(appState.map);

  // Visual radius boundary circle
  updateRadiusCircle(appState.radiusKm);

  // Render initial locations
  renderMarkers(appState.locations);
}

/**
 * Updates the visual radius circle on the map.
 * In PostGIS, DWithin filters within radius_km * 1000 metres.
 */
function updateRadiusCircle(radiusKm) {
  if (appState.radiusCircle) {
    appState.map.removeLayer(appState.radiusCircle);
  }

  appState.radiusCircle = L.circle(SOLAN_CENTER, {
    radius: radiusKm * 1000, // Leaflet radius is in meters
    color: "#C27A62",        // Muted Terracotta boundary
    weight: 2,
    opacity: 0.8,
    fillColor: "#C27A62",
    fillOpacity: 0.05,
    dashArray: "6, 8"
  }).addTo(appState.map);
}

// ── 2. Marker Rendering on Map ─────────────────────────────────────────
function renderMarkers(locations) {
  // Clear existing markers
  appState.markerLayerGroup.clearLayers();
  appState.markerMap.clear();

  locations.forEach((loc) => {
    // Custom Terracotta Pin matching Design System (#C27A62)
    const customIcon = L.divIcon({
      className: "custom-gem-pin-wrapper",
      html: `
        <div class="custom-gem-pin" title="${loc.title}">
          <i>📍</i>
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -28],
    });

    // Create marker
    const marker = L.marker([loc.latitude, loc.longitude], { icon: customIcon });

    // Interactive card popup with real photography thumbnail
    const popupContent = `
      <div class="map-popup-card">
        <img 
          src="${loc.image_url}" 
          alt="${loc.title}"
          referrerpolicy="no-referrer"
          onerror="this.onerror=null; this.src='${FALLBACK_MOUNTAIN_IMAGE}';"
        >
        <div class="map-popup-body">
          <span class="map-popup-badge">${loc.category}</span>
          <div class="map-popup-title">${loc.title}</div>
          <div class="map-popup-dist">📍 ${loc.distance_km} km from Solan</div>
        </div>
      </div>
    `;

    marker.bindPopup(popupContent);
    marker.addTo(appState.markerLayerGroup);

    // Save marker reference for synchronization with list clicks
    appState.markerMap.set(loc.id, marker);
  });
}

// ── 3. Locations Grid Rendering ────────────────────────────────────────
function renderLocationsGrid(locations) {
  const gridEl = document.getElementById("locations-grid");
  const countEl = document.getElementById("results-count");

  countEl.textContent = locations.length;

  if (locations.length === 0) {
    gridEl.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; background: #FFFFFF; border-radius: 12px; border: 1px dashed rgba(26,54,45,0.2);">
        <p style="font-size: 1.1rem; font-weight: 700; color: var(--color-primary);">No hidden gems found within this radius.</p>
        <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-top: 4px;">Try expanding your search radius to 50 km or 100 km.</p>
      </div>
    `;
    return;
  }

  gridEl.innerHTML = locations.map((loc) => `
    <article class="location-card" id="card-${loc.id}">
      <div class="location-card__image-wrap">
        <img 
          src="${loc.image_url}" 
          alt="${loc.title}" 
          loading="lazy"
          referrerpolicy="no-referrer"
          onerror="this.onerror=null; this.src='${FALLBACK_MOUNTAIN_IMAGE}';"
        >
        <span class="location-card__tag">${loc.category}</span>
        <span class="location-card__distance">${loc.distance_km} km away</span>
      </div>
      <div class="location-card__body">
        <h3 class="location-card__title">${loc.title}</h3>
        <p class="location-card__desc">${loc.description}</p>
        <div class="location-card__footer">
          <span class="location-card__guide">By: ${loc.added_by}</span>
          <button
            type="button"
            class="location-card__action"
            onclick="focusLocationOnMap(${loc.id}, ${loc.latitude}, ${loc.longitude})"
          >
            Show on Map ↗
          </button>
        </div>
      </div>
    </article>
  `).join("");
}

// ── 4. Map & Card Interactive Synchronization ──────────────────────────
window.focusLocationOnMap = function (id, lat, lng) {
  if (!appState.map) return;

  // Pan smoothly to coordinate
  appState.map.setView([lat, lng], 13, { animate: true, duration: 1 });

  // Open corresponding Leaflet popup
  const marker = appState.markerMap.get(id);
  if (marker) {
    marker.openPopup();
  }

  // Scroll smoothly to map section if card is below the fold
  const mapElement = document.getElementById("map-section");
  if (mapElement) {
    mapElement.scrollIntoView({ behavior: "smooth" });
  }
};

// ── 5. Backend Fetch & Filter Logic ────────────────────────────────────
/**
 * Calls Django REST Framework endpoint:
 * GET /api/locations/nearby/?lat=30.9045&lng=77.0967&radius={radiusKm}
 * If offline or backend container not yet launched, falls back to the client dataset seamlessly.
 */
async function fetchNearbyLocations() {
  const [solanLat, solanLng] = SOLAN_CENTER;
  const endpoint = `/api/locations/nearby/?lat=${solanLat}&lng=${solanLng}&radius=${appState.radiusKm}`;

  try {
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error("API call failed, using local dataset");
    const data = await response.json();

    // Map DRF API payload to unified location structure
    appState.locations = data.map((item) => ({
      id: item.id,
      title: item.title,
      category: item.category,
      description: item.description,
      latitude: item.latitude || (item.coordinates ? item.coordinates.y : 30.9045),
      longitude: item.longitude || (item.coordinates ? item.coordinates.x : 77.0967),
      distance_km: item.distance_km || (item.distance_m ? Math.round(item.distance_m / 100) / 10 : 0),
      image_url: item.image_url || "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
      added_by: item.added_by || "Verified Local Guide"
    }));
  } catch {
    // Graceful fallback to client-side spatial dataset
    appState.locations = INITIAL_LOCATIONS.filter(
      (loc) => loc.distance_km <= appState.radiusKm
    );
  }

  applyClientFilters();
}

/**
 * Filters the active location pool by Category and Keyword Search.
 */
function applyClientFilters() {
  let filtered = appState.locations.filter((loc) => {
    // Radius condition
    if (loc.distance_km > appState.radiusKm) return false;

    // Category condition
    if (appState.activeCategory !== "All" && loc.category !== appState.activeCategory) {
      return false;
    }

    // Search query condition
    if (appState.searchQuery.trim() !== "") {
      const q = appState.searchQuery.toLowerCase().trim();
      const matchTitle = loc.title.toLowerCase().includes(q);
      const matchDesc = loc.description.toLowerCase().includes(q);
      const matchCat = loc.category.toLowerCase().includes(q);
      if (!matchTitle && !matchDesc && !matchCat) return false;
    }

    return true;
  });

  // Re-render UI and markers
  renderLocationsGrid(filtered);
  renderMarkers(filtered);
}

// ── 6. Event Listeners Setup ───────────────────────────────────────────
function setupEventListeners() {
  // Radius Pill Buttons
  document.querySelectorAll("[data-radius]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-radius]").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      appState.radiusKm = parseFloat(btn.dataset.radius);
      updateRadiusCircle(appState.radiusKm);
      fetchNearbyLocations();
    });
  });

  // Category Pill Buttons
  document.querySelectorAll("[data-category]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("[data-category]").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      appState.activeCategory = btn.dataset.category;
      applyClientFilters();
    });
  });

  // Search input keystrokes
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      appState.searchQuery = e.target.value;
      applyClientFilters();
    });
  }

  const searchBtn = document.getElementById("search-submit");
  if (searchBtn) {
    searchBtn.addEventListener("click", () => {
      document.getElementById("explorer-section").scrollIntoView({ behavior: "smooth" });
    });
  }
}

// ── Initialization on DOM Ready ────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initMap();
  setupEventListeners();
  fetchNearbyLocations();
});
