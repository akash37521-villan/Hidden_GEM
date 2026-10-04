# Hidden Gem 🏔️
*Authentic Local Tourism & Spatial Matchmaking in Himachal Pradesh*

Hidden Gem is a full-stack spatial web application designed to bypass commercial tourist corridors. By utilizing radius-based geospatial matchmaking, the platform connects visitors directly with local residents to uncover authentic, off-the-beaten-path experiences within a 100km radius of Solan.

## ✨ Core Features
* *Geospatial Querying:* Utilizes PostGIS to instantly calculate and filter destinations and local guides within a strict 100km radius of the user's base.
* *Interactive Web Mapping:* Integrates Leaflet.js to render responsive, custom map layers pinpointing offbeat locations over default mountain landscapes.
* *Decoupled Architecture:* A strict separation of concerns utilizing a lightweight vanilla frontend communicating securely via API to a heavy-lifting Python backend.
* *Secure Data Management:* Implements Supabase for robust user authentication and media storage.

## 🛠️ Technology Stack
*Frontend (Client-Side)*
* HTML5, CSS3, Vanilla JavaScript
* Leaflet.js (Interactive Mapping)
* Deployed on Vercel

*Backend (Server-Side)*
* Python & Django REST Framework
* Docker (Containerization)
* Deployed on Render Web Services

*Database & Cloud Infrastructure*
* PostgreSQL with PostGIS Extension (Render)
* Supabase (Authentication & Object Storage)

## 🏗️ System Architecture
The application operates on a modern microservices-inspired architecture. The frontend remains framework-free to prioritize lightning-fast load times and DOM manipulation, securely fetching data from the containerized Django REST API. Complex spatial calculations (distance logic, bounding boxes) are offloaded directly to the PostGIS database layer to minimize backend memory usage and optimize response times.

## 🚀 Deployment Status
* *Database:* Active (PostgreSQL/PostGIS on Render)
* *API:* Containerized via Docker 
* *Frontend:* CDN Integrated & Supabase Initialized
