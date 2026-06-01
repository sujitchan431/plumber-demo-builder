# Plumber Demo Builder 🛠️

**Interactive AI-powered demo websites for local plumbing businesses.**

Generates self-selling demo pages that a prospect can play with — cost calculators, AI chat, booking — so the demo sells itself before you ever make the call.

Inspired by the [GHL Wizard video](https://youtu.be/3hKn54Vdnjg): *"Show them what AI does, don't tell them."*

## Features

- 🎨 **4 themes** — Modern Light, Warm Local, Dark Cyberpunk, Corporate Bold (auto-detected or manual)
- 💰 **5 cost calculators** — Drain cleaning, water heater, pipe leak, toilet, sewer line
- 💬 **AI chat widget** — Keyword-smart responses for plumbing FAQs (no API key needed)
- 📅 **Calendly booking integration** — Direct "Book Service" CTA
- 🔴 **Emergency CTA** — Pulsing button for 24/7 dispatch
- 📊 **Trust bar** — Google rating, response time, satisfaction stats
- 📎 **Before/after framing** — Links to their original (bad) website
- 🔗 **Supabase integration** — Pulls leads, writes demo URLs back

## Quick Start

```bash
# Install deps
pip install -r requirements.txt

# Set Supabase key
export SUPABASE_SERVICE_ROLE_KEY="your-key"

# Generate top 5 A-tier demos
python3 builder.py 5 --tier A

# Generate one specific lead
python3 builder.py --single abc12345

# Force a theme
python3 builder.py 3 --theme warm-local
```

## Themes

| Theme | Best For | Auto-Detection |
|---|---|---|
| `modern-light` | Established plumbing companies | Default (no keyword match) |
| `warm-local` | Family-run shops, hardware stores | "hardware", "ace", "home depot", "family" |
| `dark-cyberpunk` | 24/7 emergency services | "emergency", "express", "rapid", "24/7" |
| `corporate-bold` | Franchises, multi-location | "pro", "llc", "inc", "enterprise" |

## How It Works

1. Pulls leads from Supabase (sorted by pipeline score)
2. For each lead, auto-detects best theme from business name
3. Generates a standalone `index.html` with:
   - Personalized hero, services, and trust bar
   - Interactive cost calculators (5 categories)
   - AI chat widget with plumbing-specific responses
   - Calendly booking link
4. Saves to `/var/www/pipeline.sujitbuilds.com/demos/{lead_id}/`
5. Updates Supabase with demo URL and theme name

## Project Structure

```
plumber-demo-builder/
├── builder.py          # Main script
├── themes/
│   └── __init__.py     # Theme definitions + auto-detection
├── requirements.txt
└── README.md
```

## Demo Output

Each generated demo is a self-contained HTML file — no server, no build step, no framework. Just open in a browser.

Live demos: `https://pipeline.sujitbuilds.com/demos/`
