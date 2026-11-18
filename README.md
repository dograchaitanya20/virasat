# Virasat (विरासत) — The Living Digital Tapestry of India

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django 5.x / 6.x](https://img.shields.io/badge/Django-5.x%20%7C%206.x-092E20.svg)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)
[![HTMX](https://img.shields.io/badge/HTMX-1.9.12-3366CC.svg)](https://htmx.org/)
[![Alpine.js](https://img.shields.io/badge/Alpine.js-3.13-77C1D2.svg)](https://alpinejs.dev/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passing-brightgreen.svg)]()

> *"अयं निजः परो वेति गणना लघुचेतसाम् । उदारचरितानां तु वसुधैव कुटुम्बकम् ॥"*  
> — **Maha Upanishad**: *To the noble-hearted, the entire world is one family.*

**Virasat (विरासत)** is a museum-grade digital showcase celebrating five millennia of India's architectural marvels, sacred calendar rituals, classical performing arts, indigenous handicrafts, regional culinary traditions, and historical milestones.

Designed with an **editorial heritage-luxe** aesthetic (warm sandstone, deep indigo, royal gold, and terracotta), Virasat blends server-rendered Django templates with **HTMX** and **Alpine.js** for immediate reactivity, **Leaflet.js** for cartography, and **GSAP** for smooth scroll-driven storytelling.

---

## 🏛️ Key Features

1. **Cinematic Hero & Dashboard**:
   - High-impact parallax banner with Devanagari calligraphy (`पाँच सहस्राब्दियों की जीवंत संस्कृति`).
   - Dynamic animated counters ribbon (28+ States, 42+ UNESCO Sites, 100+ Festivals, 5000+ Years).
   - "Festival of the Season" spotlight card.
   - Horizontal Swiper carousel of featured UNESCO monuments.
   - 6 Cultural Pillar discovery portals (Monuments, Classical Arts, Crafts, Cuisine, Timeline, Atlas).

2. **Interactive India Atlas (Leaflet.js & HTMX)**:
   - Full-bleed geographic atlas with color-coded cultural regional pins.
   - Interactive hover tooltips.
   - Clicking any state or selecting from the jump menu triggers an HTMX drawer side panel revealing that state's monuments, festivals, crafts, and food delicacies without page reloads.

3. **UNESCO World Heritage & Monuments**:
   - Filterable catalog by State, Category (Monument, Temple, Fort, Cave, Natural, Living Heritage), and UNESCO inscription.
   - Live HTMX search and instant filtering with pagination.
   - Detail pages featuring:
     - GLightbox zoomable galleries
     - Embedded Leaflet mini-map with exact coordinates
     - Architectural style, construction date, and commissioning rulers
     - In-depth historical origin chronicle and visiting guidelines
     - One-click "Save to My Collection" bookmarking

4. **Living Festivals Calendar**:
   - Month-wise calendar tabs (January to December) + "Happening This Month" highlight badges.
   - Filtering by cultural/religious tradition (Pan-Indian, Hinduism, Islam, Sikhism, Buddhism, Tribal/Harvest).
   - Sacred rites, spiritual significance, and festival prasadam foods.

5. **Arts, Crafts & Classical Music**:
   - Filterable categories: Classical Dance, Vocal/Instrumental Music, Folk Painting, Sculpture/Craft, Handloom Textiles, and Traditional Theatre.
   - Inscribed UNESCO Intangible Heritage tags.
   - Lineage histories, techniques, instruments, and living master gurus.

6. **Regional Cuisine Explorer**:
   - Dietary filter (Pure Vegetarian vs. Non-Vegetarian).
   - Meal course filter (Breakfast/Snack, Main Course, Dessert/Sweet).
   - Spice Heat Index (Mild, Medium, Fiery).
   - Culinary stories, signature spice botany, and preparation times.

7. **Historical Timeline of India**:
   - Scroll-driven vertical timeline charting 15 pivotal milestones from the Indus Valley Civilization (c. 2600 BCE), Mauryan Ashokan Edicts, Golden Gupta Age, Cholas, Vijayanagara, Mughals, Marathas, Freedom Struggle, to the Sovereign Republic.

8. **Test Your India IQ (Interactive Challenge & Leaderboard)**:
   - 10-question randomized trivia challenge spanning all categories.
   - Live timer and instant feedback on selection (green/red) with historical context explanation cards.
   - Score calculation, accuracy percentage, and Heritage Rank (e.g. *Grand National Archivist*).
   - Submit score to the national public leaderboard.

9. **Community Cultural Stories**:
   - Community-contributed travel diaries and folklore articles.
   - Logged-in users can compose and publish new stories.

10. **Command Palette Global Search (`Ctrl+K` / `⌘K`)**:
    - Quick search modal indexing Monuments, Festivals, Dances, Dishes, and States with grouped results.

11. **User Accounts & Personal Collection**:
    - Authentication (Sign Up, Sign In, Sign Out).
    - Profile dossier management (Bio, Avatar, Location, Favorite State).
    - "My Collection" bookmarks page.
    - Personal quiz attempt history.

12. **Bilingual Support & Dark/Light Mode**:
    - English / हिन्दी (Hindi) language switcher using Django `i18n` message catalogs (`django.mo`).
    - Dark mode and light mode persisted in `localStorage`.

---

## 🎨 UI/UX Design System

- **Color Tokens**:
  - *Sandstone Parchment*: `#FAF8F5` (Light base), `#F5EFEB`
  - *Deep Indigo / Midnight*: `#0B0E14` (Dark base), `#111827`
  - *Metallic Gold*: `#D4AF37`, `#F3E5AB`
  - *Vibrant Saffron*: `#FF8F00`, `#E65100`
  - *Terracotta Clay*: `#C85A32`
  - *Peacock Teal*: `#0D5C75`
- **Typography**:
  - Headings: `Cinzel` & `Cormorant Garamond`
  - Body: `Plus Jakarta Sans`
  - Devanagari (Hindi): `Noto Sans Devanagari`
- **Subtle Motifs**: Geometric Indian jaali lattice background patterns in pure CSS.

---

## 🛠️ Architecture & Tech Stack

```
Django_CA/
├── apps/
│   ├── core/          # Home, Map, Timeline, About, Contact, Search, API
│   ├── states/        # State/Region models, views, and map side panel
│   ├── heritage/      # HeritageSite & gallery models, list, detail
│   ├── festivals/     # Sacred calendar & rituals
│   ├── arts/          # Classical dances, music, paintings, textiles
│   ├── cuisine/       # State culinary explorer & veg/non-veg filtering
│   ├── stories/       # Community folklore & articles
│   ├── quiz/          # "Test Your India IQ" engine & leaderboard
│   └── accounts/      # UserProfile, generic Bookmarks, auth
├── templates/         # Semantic HTML5 + HTMX + Alpine.js templates
├── static/
│   ├── css/virasat.css# Design system variables, glassmorphism, cards
│   └── js/app.js      # Theme toggle, search shortcut, toast engine
├── tests/             # 16 unit and integration tests (pytest-django)
├── virasat_project/   # Django settings, URLs, WSGI, ASGI
├── manage.py
├── requirements.txt
├── Procfile
└── render.yaml
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Virtual Environment

```bash
cd Django_CA
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
npm install
```

### 3. Build Tailwind CSS (Self-Contained Offline Stylesheet)

All CSS utilities are compiled locally into `static/css/tailwind.css` (no CDN runtime dependency):

```bash
npm run build:css
# or directly with npx:
npx tailwindcss -i ./static/css/tailwind.input.css -o ./static/css/tailwind.css --minify
```

For development auto-rebuild on template changes:
```bash
npm run watch:css
```

All vendor JavaScript and CSS libraries (HTMX v1.9.12, Alpine.js v3.13.8, GSAP & ScrollTrigger v3.12.5, Swiper v11, Leaflet v1.9.4, and GLightbox) are bundled in `static/vendor/` and referenced locally via Django `{% static %}`.

### 4. Initialize Database & Seed Content

```bash
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --no-input
```

The `seed_data` command will automatically populate:
- **28 States and Union Territories**
- **25+ Heritage Sites** (Taj Mahal, Hampi, Khajuraho, Ajanta, Konark, etc.)
- **20+ Cultural Festivals**
- **20+ Classical Arts & Crafts**
- **20+ Regional Cuisines**
- **15 Historical Timeline Milestones**
- **30+ Quiz Questions with explanatory historical context**
- Default demo accounts

### 4. Run the Development Server

```bash
python manage.py runserver
```

Open your browser at **`http://127.0.0.1:8000/`**.

---

## 🔑 Default Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Superuser / Archivist** | `admin` | `admin123` | Full access to Django admin at `/admin/` |
| **Explorer Demo** | `heritage_explorer` | `explorer123` | Pre-loaded with bookmarks and quiz scores |

---

## 🧪 Test Suite

Run the automated test suite using `pytest`:

```bash
pytest
```

Output:
```
tests/test_models.py ....                                                [ 25%]
tests/test_quiz_logic.py ..                                              [ 37%]
tests/test_seed_command.py .                                             [ 43%]
tests/test_views.py .........                                            [100%]
============================= 16 passed in 2.86s ==============================
```

---

## 🌐 Read-Only REST API

Virasat exposes clean, read-only JSON endpoints powered by Django REST Framework:

- `GET /api/stats/` — Summary counts of all indexed cultural records
- `GET /api/states/` — List of all 28 states & regions
- `GET /api/heritage/` — List of monuments, categories, and coordinates
- `GET /api/festivals/` — Sacred calendar events
- `GET /api/arts/` — Classical performing arts and master crafts
- `GET /api/cuisine/` — Regional recipes and dietary flags
- `GET /api/timeline/` — Chronological historical milestones

---

## 🚢 Production Deployment

### Option A: Render (1-Click via `render.yaml`)
1. Create a new Web Service on [Render](https://render.com/).
2. Connect your Git repository.
3. Render automatically picks up `render.yaml` and executes:
   `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py seed_data`
   and starts Gunicorn:
   `gunicorn virasat_project.wsgi:application --bind 0.0.0.0:$PORT`

### Option B: Railway / Heroku
The included `Procfile` declares the web process and release phase:
```Procfile
web: gunicorn virasat_project.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py seed_data
```

---

## 📜 Ethical Licensing & Attribution
- All historical narratives, monument profiles, and culinary lore are researched from authentic archival records (Archaeological Survey of India, UNESCO World Heritage Centre, Sangeet Natak Akademi).
- Photographic imagery is sourced from royalty-free and Creative Commons Wikimedia Commons archives.

*Built with reverence for the eternal cultural traditions of India.*
