#!/usr/bin/env python3
"""
Plumber Demo Builder — Interactive AI-powered demo websites for local businesses.

Generates self-selling demo pages with:
- Multi-theme support (Modern Light, Warm Local, Dark Cyberpunk, Corporate Bold)
- Auto-theme detection based on business name
- 5 plumbing cost calculators (drain, water heater, pipe leak, toilet, sewer)
- AI chat widget (keyword-smart responses)
- Calendly booking integration
- Trust bar + emergency CTA
- Before/after framing with original website link

Usage:
  python3 builder.py [count] [--tier A|B|AB]
  python3 builder.py --single {lead_id}
  python3 builder.py 1 --theme warm-local    (force specific theme)

GitHub: https://github.com/sujitchan431/plumber-demo-builder
"""

import os, sys, requests, json, re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from themes import THEMES, detect_theme

SUPABASE_URL = "https://qipxrvspucmwzchswhix.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
PATCH_HEADERS = {**HEADERS, "Content-Type": "application/json", "Prefer": "return=minimal"}

DEMO_ROOT = "/var/www/demo.thebluewhale.online/plumber"
CAL_LINK = "https://calendly.com/sujitchan431/30min"

PLUMBING_SERVICES = [
    ("🚿", "Drain Cleaning", "Clogged drains? Hydro-jetting and snake service. Same-day available."),
    ("🔥", "Water Heater Service", "Tankless & traditional water heater repair, install, and flush."),
    ("🚽", "Toilet Repair & Install", "Running, leaking, or clogged. We fix and install all models."),
    ("💧", "Pipe Repair & Leak Detection", "Leaky pipes, slab leaks, repiping — we find and fix fast."),
    ("🏠", "Sewer Line Service", "Camera inspection, trenchless repair, and rooter service."),
    ("⚡", "Emergency Plumbing", "24/7 emergency response. Burst pipe? We're there in 30 min or less."),
]


def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower().strip()).strip('-')[:50]


def get_leads(count, tier, single_id=None):
    """Fetch plumbing leads from Supabase, ordered by score."""
    if single_id:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/businesses"
            f"?select=id,business_name,city,phone,email,website,rating,review_count,address,raw_data"
            f"&id=eq.{single_id}",
            headers=HEADERS,
        )
        if r.status_code != 200:
            print(f"DB error: {r.status_code}")
            return None
        data = r.json()
        if not data:
            return None
        lead = data[0]
        raw = lead.get("raw_data") or {}
        if isinstance(raw, str):
            try: raw = json.loads(raw)
            except: raw = {}
        lead["_score"] = raw.get("pipeline_score", 0)
        return [lead]

    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/businesses"
        f"?select=id,business_name,city,phone,email,website,rating,review_count,address,raw_data"
        f"&industry=eq.plumbers"
        f"&order=raw_data->pipeline_score.desc"
        f"&limit=300",
        headers=HEADERS,
    )
    if r.status_code != 200:
        print(f"DB error: {r.status_code}")
        return []

    leads = r.json()
    filtered = []
    for lead in leads:
        raw = lead.get("raw_data") or {}
        if isinstance(raw, str):
            try: raw = json.loads(raw)
            except: raw = {}

        lead_tier = raw.get("pipeline_tier", "D")
        lead["_score"] = raw.get("pipeline_score", 0)

        if tier == "A" and lead_tier != "A":
            continue
        if tier == "B" and lead_tier not in ("A", "B"):
            continue

        filtered.append(lead)
    return filtered[:count]


def generate_demo(lead, theme_name=None):
    """Generate interactive plumbing demo website HTML."""
    name = lead.get("business_name", "Your Local Plumber")
    city = lead.get("city", "Wyoming")
    phone = lead.get("phone", "")
    email = lead.get("email", "")
    website = lead.get("website", "")
    rating = lead.get("rating", 5.0)
    reviews = lead.get("review_count", 0)

    phone_display = phone if phone else "(307) 555-0123"
    phone_link = re.sub(r'[^\d+]', '', phone_display) if phone else "3075550123"
    first_name = name.split()[0] if name.split() else name
    location = f"{city}, WY" if city else "Wyoming"

    # Theme selection
    if not theme_name or theme_name == "auto":
        theme_name = detect_theme(name)
    theme = THEMES.get(theme_name, THEMES["modern-light"])

    star_count = min(5, max(1, int(rating)))
    stars = "★" * star_count + ("½" if rating % 1 >= 0.5 else "")

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — 24/7 Plumbing in {location}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; scroll-behavior: smooth; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; }}
{theme["css"]}

  /* Layout (shared across themes) */
  .hero {{ padding: 100px 0 70px; text-align: center; position: relative; }}
  .hero-content {{ position: relative; z-index: 1; }}
  .hero .badge {{ display: inline-block; padding: 8px 18px; border-radius: 20px; font-size: 14px; margin-bottom: 20px; animation: pulse 2s infinite; font-weight: 600; }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.7; }} }}
  .hero h1 {{ font-size: clamp(32px, 5vw, 52px); font-weight: 800; margin-bottom: 14px; line-height: 1.2; }}
  .hero .subtitle {{ font-size: 18px; max-width: 550px; margin: 0 auto 8px; }}
  .hero .location {{ font-size: 15px; margin-bottom: 25px; }}
  .hero .rating-display {{ display: inline-flex; align-items: center; gap: 8px; margin-bottom: 28px; font-size: 18px; }}
  .hero .stars {{ font-size: 22px; letter-spacing: 2px; }}
  .hero .cta-group {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }}
  .btn {{ padding: 14px 28px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s; text-decoration: none; display: inline-block; }}
  .btn-primary {{ box-shadow: 0 0 20px rgba(0,0,0,0.15); }}
  .btn-primary:hover {{ transform: translateY(-2px); }}
  .btn-outline {{ background: transparent; }}
  .btn-outline:hover {{ opacity: 0.9; }}
  .btn-emergency {{ animation: pulse 1.5s infinite; }}

  .trust-bar {{ display: flex; justify-content: center; gap: 50px; flex-wrap: wrap; padding: 35px 0; }}
  .trust-item {{ text-align: center; }}
  .trust-item .num {{ font-size: 28px; font-weight: 800; }}
  .trust-item .label {{ font-size: 13px; color: var(--muted); margin-top: 4px; }}

  .section {{ padding: 60px 0; }}
  .section h2 {{ font-size: 32px; font-weight: 700; text-align: center; margin-bottom: 8px; }}
  .section .subtitle {{ text-align: center; color: var(--muted); margin-bottom: 40px; font-size: 16px; }}

  .existing-site {{ text-align: center; padding: 8px 0 0; }}
  .existing-site a {{ font-size: 13px; text-decoration: none; border-bottom: 1px dashed; }}

  .calc-tabs {{ display: flex; gap: 8px; justify-content: center; margin-bottom: 24px; flex-wrap: wrap; }}
  .calc-tab {{ padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; transition: all 0.2s; }}

  .calculator {{ border-radius: 16px; padding: 36px; max-width: 600px; margin: 0 auto; }}
  .calculator label {{ display: block; font-size: 14px; color: var(--muted); margin-bottom: 6px; margin-top: 16px; }}
  .calculator select {{ width: 100%; padding: 14px; border-radius: 8px; font-size: 15px; cursor: pointer; }}
  .calculator select:focus {{ border-color: var(--accent); outline: none; }}
  .estimate {{ padding: 20px; margin: 20px 0; text-align: center; display: none; border-radius: 10px; }}
  .estimate.show {{ display: block; animation: fadeIn 0.3s; }}
  @keyframes fadeIn {{ from{{opacity:0;}} to{{opacity:1;}} }}
  .estimate .price {{ font-size: 36px; font-weight: 800; }}
  .estimate .range {{ font-size: 14px; color: var(--muted); margin-top: 4px; }}
  .calc-hidden {{ display: none; }}

  .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
  .service-card {{ border-radius: 12px; padding: 28px; transition: transform 0.2s, border-color 0.2s; }}
  .service-card:hover {{ transform: translateY(-4px); }}
  .service-card .icon {{ font-size: 32px; margin-bottom: 12px; }}
  .service-card h3 {{ font-size: 18px; margin-bottom: 8px; }}
  .service-card p {{ font-size: 14px; color: var(--muted); }}

  .chat-toggle {{ position: fixed; bottom: 24px; right: 24px; width: 56px; height: 56px; border-radius: 50%; color: #fff; font-size: 24px; border: none; cursor: pointer; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.3); transition: transform 0.2s; background: var(--accent); }}
  .chat-toggle:hover {{ transform: scale(1.1); }}
  .chat-window {{ position: fixed; bottom: 90px; right: 24px; width: 360px; max-height: 500px; border-radius: 16px; z-index: 999; display: none; flex-direction: column; overflow: hidden; }}
  .chat-window.open {{ display: flex; }}
  .chat-header {{ padding: 16px; font-weight: 700; display: flex; align-items: center; gap: 10px; color: #fff; background: var(--accent); }}
  .chat-header .status {{ width: 8px; height: 8px; background: #fff; border-radius: 50%; animation: pulse 2s infinite; }}
  .chat-body {{ padding: 16px; flex:1; overflow-y:auto; max-height: 320px; display: flex; flex-direction: column; gap: 10px; }}
  .chat-msg {{ padding: 10px 14px; border-radius: 12px; font-size: 14px; max-width: 85%; animation: fadeIn 0.3s; }}
  .chat-msg.user {{ align-self: flex-end; background: var(--accent); color: #fff; }}
  .chat-input-area {{ padding: 12px; border-top: 1px solid var(--border); display: flex; gap: 8px; }}

  .cta-section {{ text-align: center; padding: 80px 0; }}
  .cta-section h2 {{ font-size: 36px; margin-bottom: 16px; }}

  footer {{ text-align: center; padding: 40px 0; font-size: 14px; }}
  footer a {{ color: var(--accent); text-decoration: none; }}

  @media (max-width: 768px) {{
    .hero {{ padding: 60px 0 40px; }}
    .chat-window {{ width: calc(100vw - 30px); right: 8px; bottom: 80px; }}
    .trust-bar {{ gap: 20px; }}
  }}
</style>
</head>
<body>

<!-- HERO -->
<section class="hero">
  <div class="container hero-content">
    <div class="badge">⚡ AI-Powered 24/7 Emergency Response</div>
    <h1>{name}<br><span style="color:{theme['accent_hex']}">Plumbing Done Right</span></h1>
    <p class="subtitle">Professional plumbing services in {location}. Our AI receptionist answers every call instantly — even at 2 AM. No more missed calls, no more lost customers.</p>
    <p class="location">📍 {location}</p>
    <div class="rating-display">
      <span class="stars">{stars}</span>
      <strong>{rating}</strong>
      <span style="font-size:14px;">({reviews} reviews)</span>
    </div>
    <div class="cta-group">
      <a href="tel:{phone_link}" class="btn btn-emergency">📞 Emergency Repair</a>
      <a href="{CAL_LINK}" target="_blank" class="btn btn-primary">📅 Book Service</a>
      <a href="#calculator" class="btn btn-outline">💰 Get Estimate</a>
    </div>
  </div>
</section>

<!-- TRUST BAR -->
<div class="trust-bar">
  <div class="trust-item"><div class="num">24/7</div><div class="label">Emergency Service</div></div>
  <div class="trust-item"><div class="num">{rating}</div><div class="label">Google Rating</div></div>
  <div class="trust-item"><div class="num">100%</div><div class="label">Satisfaction</div></div>
  <div class="trust-item"><div class="num">30m</div><div class="label">Avg Response Time</div></div>
</div>
'''
    if website and website.startswith("http"):
        html += f'\n<div class="existing-site"><a href="{website}" target="_blank">📎 View original website →</a></div>'

    # Service cards
    service_cards = "\n".join(
        f'      <div class="service-card"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>'
        for icon, title, desc in PLUMBING_SERVICES
    )

    html += f'''
<!-- COST CALCULATOR -->
<section class="section" id="calculator">
  <div class="container">
    <h2>💰 Instant Plumbing Cost Estimator</h2>
    <p class="subtitle">Get a rough estimate before we arrive — transparent pricing, no surprises</p>
    
    <div class="calc-tabs">
      <button class="calc-tab active" onclick="switchCalc('drain')">🚿 Drain</button>
      <button class="calc-tab" onclick="switchCalc('heater')">🔥 Water Heater</button>
      <button class="calc-tab" onclick="switchCalc('leak')">💧 Pipe Leak</button>
      <button class="calc-tab" onclick="switchCalc('toilet')">🚽 Toilet</button>
      <button class="calc-tab" onclick="switchCalc('sewer')">🏠 Sewer</button>
    </div>

    <!-- Drain -->
    <div class="calculator" id="calc-drain">
      <label>Type of clog</label>
      <select id="drain-type" onchange="calcDrain()">
        <option value="">-- Select --</option>
        <option value="sink">Kitchen/Bathroom sink</option>
        <option value="shower">Shower/tub drain</option>
        <option value="main">Main line clog</option>
        <option value="toilet">Toilet clog</option>
      </select>
      <label>Severity</label>
      <select id="drain-severity" onchange="calcDrain()">
        <option value="">-- Select --</option>
        <option value="mild">Slow draining</option>
        <option value="moderate">Standing water</option>
        <option value="severe">Completely blocked</option>
        <option value="emergency">Backing up / flooding</option>
      </select>
      <div class="estimate" id="drain-estimate">
        <div class="price" id="drain-price">$0</div>
        <div class="range" id="drain-range">Typical range: $100 – $500</div>
        <p style="margin-top:12px;font-size:14px;color:var(--muted);">Includes camera inspection. Final price confirmed on-site.</p>
      </div>
    </div>

    <!-- Water Heater -->
    <div class="calculator calc-hidden" id="calc-heater">
      <label>Service needed</label>
      <select id="heater-type" onchange="calcHeater()">
        <option value="">-- Select --</option>
        <option value="repair">Repair (not heating / leaking)</option>
        <option value="replace">Replace existing unit</option>
        <option value="tankless">Install tankless system</option>
        <option value="flush">Flush & maintenance</option>
      </select>
      <label>Unit type</label>
      <select id="heater-fuel" onchange="calcHeater()">
        <option value="">-- Select --</option>
        <option value="gas">Gas</option>
        <option value="electric">Electric</option>
        <option value="tankless">Tankless</option>
      </select>
      <div class="estimate" id="heater-estimate">
        <div class="price" id="heater-price">$0</div>
        <div class="range" id="heater-range">Typical range varies by unit</div>
      </div>
    </div>

    <!-- Pipe Leak -->
    <div class="calculator calc-hidden" id="calc-leak">
      <label>Leak location</label>
      <select id="leak-location" onchange="calcLeak()">
        <option value="">-- Select --</option>
        <option value="under-sink">Under sink</option>
        <option value="wall">Inside wall</option>
        <option value="slab">Slab/foundation leak</option>
        <option value="yard">Yard/underground</option>
        <option value="burst">Burst pipe (gushing)</option>
      </select>
      <label>Urgency</label>
      <select id="leak-urgency" onchange="calcLeak()">
        <option value="">-- How soon? --</option>
        <option value="emergency">Emergency (ASAP)</option>
        <option value="today">Today</option>
        <option value="week">This week</option>
      </select>
      <div class="estimate" id="leak-estimate">
        <div class="price" id="leak-price">$0</div>
        <div class="range" id="leak-range">Typical range: $150 – $4,000</div>
      </div>
    </div>

    <!-- Toilet -->
    <div class="calculator calc-hidden" id="calc-toilet">
      <label>Issue</label>
      <select id="toilet-issue" onchange="calcToilet()">
        <option value="">-- Select --</option>
        <option value="clog">Clogged toilet</option>
        <option value="running">Constantly running</option>
        <option value="leak">Leaking at base</option>
        <option value="install">Install new toilet</option>
        <option value="flush">Won't flush properly</option>
      </select>
      <div class="estimate" id="toilet-estimate">
        <div class="price" id="toilet-price">$0</div>
        <div class="range" id="toilet-range">Typical range: $95 – $600</div>
      </div>
    </div>

    <!-- Sewer -->
    <div class="calculator calc-hidden" id="calc-sewer">
      <label>Issue</label>
      <select id="sewer-issue" onchange="calcSewer()">
        <option value="">-- Select --</option>
        <option value="backup">Sewage backing up</option>
        <option value="slow">Slow drains throughout</option>
        <option value="smell">Sewage smell in yard</option>
        <option value="inspect">Camera inspection only</option>
        <option value="replace">Line needs replacement</option>
      </select>
      <div class="estimate" id="sewer-estimate">
        <div class="price" id="sewer-price">$0</div>
        <div class="range" id="sewer-range">Typical range: $250 – $15,000</div>
      </div>
    </div>
  </div>
</section>

<!-- SERVICES -->
<section class="section">
  <div class="container">
    <h2>🛠️ Plumbing Services in {location}</h2>
    <p class="subtitle">Complete residential & commercial plumbing solutions</p>
    <div class="services-grid">
{service_cards}
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="cta-section">
  <div class="container">
    <h2>Stop Losing Plumbing Calls at 2 AM</h2>
    <p style="color:var(--muted);margin-bottom:30px;font-size:18px;">Most plumbing businesses miss 40% of emergency calls. Our AI-powered system answers every call, books jobs automatically, and sends you the details.</p>
    <a href="{CAL_LINK}" target="_blank" class="btn btn-primary" style="font-size:18px;padding:18px 36px;">📅 See It In Action — Free Demo</a>
  </div>
</section>

<!-- CHAT WIDGET -->
<button class="chat-toggle" onclick="toggleChat()">💬</button>
<div class="chat-window" id="chat-window">
  <div class="chat-header"><div class="status"></div> {name} — 24/7 AI Assistant</div>
  <div class="chat-body" id="chat-body">
    <div class="chat-msg bot">👋 Hi! I'm {first_name}'s AI assistant. I can help with: drain cleaning quotes, water heater questions, emergency service, or booking an appointment. What do you need?</div>
  </div>
  <div class="chat-input-area">
    <input type="text" id="chat-input" placeholder="Clogged drain, leaky pipe..." onkeypress="if(event.key==='Enter')sendChat()">
    <button class="btn btn-primary" style="padding:10px 16px;font-size:14px;" onclick="sendChat()">Send</button>
  </div>
</div>

<footer>
  <p>{name} — AI-Powered Plumbing in {location} | Theme: {theme["name"]}</p>
  <p style="margin-top:8px;font-size:13px;">This is an interactive demo — <a href="{CAL_LINK}">Book a real demo →</a></p>
  <p style="margin-top:16px;font-size:11px;">Built with 🛠️ Plumber Demo Builder</p>
</footer>

<script>
function switchCalc(type) {{
  document.querySelectorAll('.calc-tab').forEach(t => t.classList.remove('active'));
  event.target.classList.add('active');
  ['drain','heater','leak','toilet','sewer'].forEach(id => {{
    document.getElementById('calc-' + id).classList.toggle('calc-hidden', id !== type);
  }});
}}

function calcDrain() {{
  const type = document.getElementById('drain-type').value;
  const severity = document.getElementById('drain-severity').value;
  if (!type || !severity) return;
  const base = {{sink:{{mild:110,moderate:175,severe:250,emergency:350}},shower:{{mild:120,moderate:200,severe:280,emergency:400}},main:{{mild:250,moderate:400,severe:600,emergency:900}},toilet:{{mild:95,moderate:150,severe:220,emergency:350}}}};
  const price = base[type]?.[severity] || 200;
  document.getElementById('drain-price').textContent = '$' + price;
  document.getElementById('drain-range').textContent = 'Range: $' + Math.round(price*0.75) + ' – $' + Math.round(price*1.3);
  document.getElementById('drain-estimate').classList.add('show');
}}

function calcHeater() {{
  const type = document.getElementById('heater-type').value;
  const fuel = document.getElementById('heater-fuel').value;
  if (!type || !fuel) return;
  const prices = {{repair:{{gas:350,electric:300,tankless:500}},replace:{{gas:1800,electric:1500,tankless:3500}},tankless:{{gas:3200,electric:2800,tankless:3500}},flush:{{gas:150,electric:150,tankless:200}}}};
  const price = prices[type]?.[fuel] || 500;
  document.getElementById('heater-price').textContent = '$' + price.toLocaleString();
  document.getElementById('heater-estimate').classList.add('show');
}}

function calcLeak() {{
  const loc = document.getElementById('leak-location').value;
  const urgency = document.getElementById('leak-urgency').value;
  if (!loc || !urgency) return;
  const base = {{'under-sink':150,wall:400,slab:2500,yard:1800,burst:800}};
  const mult = {{emergency:1.5,today:1.2,week:1.0}};
  const price = Math.round((base[loc]||300) * (mult[urgency]||1));
  document.getElementById('leak-price').textContent = '$' + price.toLocaleString();
  document.getElementById('leak-range').textContent = 'Range: $' + Math.round(price*0.7).toLocaleString() + ' – $' + Math.round(price*1.4).toLocaleString();
  document.getElementById('leak-estimate').classList.add('show');
}}

function calcToilet() {{
  const issue = document.getElementById('toilet-issue').value;
  if (!issue) return;
  const prices = {{clog:95,running:125,leak:180,install:450,flush:110}};
  document.getElementById('toilet-price').textContent = '$' + prices[issue];
  document.getElementById('toilet-estimate').classList.add('show');
}}

function calcSewer() {{
  const issue = document.getElementById('sewer-issue').value;
  if (!issue) return;
  const prices = {{backup:1200,slow:350,smell:500,inspect:250,replace:8500}};
  document.getElementById('sewer-price').textContent = '$' + prices[issue].toLocaleString();
  document.getElementById('sewer-estimate').classList.add('show');
}}

function toggleChat() {{
  const w = document.getElementById('chat-window');
  w.classList.toggle('open');
  if (w.classList.contains('open')) document.getElementById('chat-input').focus();
}}

const chatResponses = {{
  'clog':"We clear drain clogs fast! Kitchen/bathroom clogs start at $95, main line from $250. Most cleared in under an hour. Need emergency service?",
  'drain':"Slow or clogged drain? We use professional camera inspection + hydro-jetting. Average cost: $110-$400. Want a specific estimate using the calculator above?",
  'water heater':"Water heater issues? We repair all brands — gas, electric, and tankless. Repairs from $150, replacements from $1,500. No hot water? We can be there today.",
  'leak':"A leak can cause serious damage fast. Under-sink leaks from $150. Wall/slab leaks need specialized equipment. For active flooding, call our emergency line NOW.",
  'toilet':"Toilet clogged, running, or leaking? Basic repairs from $95. New installation from $450. We stock parts for all major brands.",
  'emergency':"🚨 Call us now at {phone_display} for immediate dispatch. Our on-call plumber can be there in 30 minutes or less. Don't wait — water damage gets expensive fast.",
  'pricing':"Transparent pricing — all estimates are free, confirmed BEFORE work begins. Use our calculator above for instant ballpark numbers.",
  'booking':"Great! Book directly here: {CAL_LINK} — or tell me your preferred date/time.",
  'sewer':"Sewer line problems are serious. Camera inspection $250. Trenchless repair can save your yard. Prices from $350 to $8,500+ for replacements.",
  'default':"I'm {first_name}'s AI assistant, available 24/7. I can help with: drain cleaning, water heaters, leak repair, toilet issues, sewer lines, or emergency service. What can I help with?",
}};

function sendChat() {{
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;
  const body = document.getElementById('chat-body');
  body.innerHTML += '<div class="chat-msg user">' + msg + '</div>';
  input.value = '';
  setTimeout(() => {{
    const lower = msg.toLowerCase();
    let resp = chatResponses.default;
    for (const [k, v] of Object.entries(chatResponses)) {{ if (lower.includes(k)) {{ resp = v; break; }} }}
    body.innerHTML += '<div class="chat-msg bot">' + resp + '</div>';
    body.scrollTop = body.scrollHeight;
  }}, 600);
  body.scrollTop = body.scrollHeight;
}}
</script>
</body>
</html>'''
    return html, theme_name


def update_lead(lead_id, demo_url, theme_name):
    """Save demo URL and theme to lead's raw_data in Supabase."""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{lead_id}&select=raw_data",
        headers=HEADERS,
    )
    raw = {}
    if r.status_code == 200:
        data = r.json()
        if data and isinstance(data, list) and len(data) > 0:
            raw = data[0].get("raw_data") or {}
            if isinstance(raw, str):
                raw = json.loads(raw) if raw else {}
    raw["demo_url"] = demo_url
    raw["demo_theme"] = theme_name
    raw["demo_generated_at"] = datetime.now().isoformat()
    raw["demo_version"] = "v2-multi-theme"

    requests.patch(
        f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{lead_id}",
        json={"raw_data": raw},
        headers=PATCH_HEADERS,
    )


def main():
    single_id = None
    count = 10
    tier = "AB"
    theme_name = "auto"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--single":
            single_id = args[i + 1]; i += 2
        elif args[i] == "--tier":
            tier = args[i + 1] if i + 1 < len(args) else "AB"; i += 2
        elif args[i] == "--theme":
            theme_name = args[i + 1]; i += 2
        elif args[i].isdigit():
            count = int(args[i]); i += 1
        else:
            i += 1

    # Validate theme
    if theme_name != "auto" and theme_name not in THEMES:
        print(f"❌ Unknown theme '{theme_name}'. Available: {', '.join(THEMES.keys())}")
        return

    print("╔══════════════════════════════════════════╗")
    print("║   🛠️  Plumber Demo Builder v2           ║")
    print("║   Multi-Theme Interactive Demos          ║")
    print("╚══════════════════════════════════════════╝")
    print(f"Tier: {tier} | Theme: {theme_name} | Output: {DEMO_ROOT}\n")

    leads = get_leads(count, tier, single_id)
    if not leads:
        print("No leads found."); return

    print(f"Leads: {len(leads)}\n{'='*50}")

    generated = 0
    for i, lead in enumerate(leads):
        name = lead.get("business_name", "Unknown")
        lead_id = lead["id"][:8]
        score = lead.get("_score", "?")

        html, used_theme = generate_demo(lead, theme_name)

        demo_dir = os.path.join(DEMO_ROOT, lead_id)
        os.makedirs(demo_dir, exist_ok=True)
        index_path = os.path.join(demo_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)

        demo_url = f"https://demo.thebluewhale.online/plumber/{lead_id}/"
        update_lead(lead["id"], demo_url, used_theme)

        theme_label = THEMES[used_theme]["name"]
        print(f"[{i+1}/{len(leads)}] [{score}] {name[:40]:40} 🎨 {theme_label}")
        generated += 1

    print(f"\n{'='*50}")
    print(f"✅ {generated} demos generated")
    print(f"🌐 https://demo.thebluewhale.online/plumber/")

    # Theme distribution summary
    if generated > 1:
        from collections import Counter
        theme_counts = Counter()
        for lead in leads:
            _, t = generate_demo(lead, "auto")
            theme_counts[t] += 1
        print(f"\n📊 Theme distribution:")
        for t, c in theme_counts.most_common():
            print(f"   {THEMES[t]['name']:20} {c} site(s)")

    if leads:
        # Print theme key
        theme_list = ", ".join(f"{k} ({v['name']})" for k, v in THEMES.items())
        print(f"\n🎨 Available themes: {theme_list}")
        print(f"   Default: auto-detect based on business name")
        print(f"   Override: --theme warm-local")


if __name__ == "__main__":
    main()
