#!/usr/bin/env python3
"""
Plumber Outreach Sender — sends personalized cold emails via Resend.
Pulls A-tier leads from Supabase with demo URLs, generates copy using
the cold-email-outreach framework, sends via Resend API.

Usage:
  python3 outreach_sender.py --dry-run        (preview without sending)
  python3 outreach_sender.py --count 5         (send to top 5 A-tier)
  python3 outreach_sender.py --all             (send to all A-tier)
  python3 outreach_sender.py --lead abc12345   (send to one specific lead)

Requires: RESEND_API_KEY in .env
"""

import os, sys, json, re, requests
from datetime import datetime

SUPABASE_URL = "https://qipxrvspucmwzchswhix.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
RESEND_KEY = os.environ.get("RESEND_API_KEY", "")

HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
PATCH_HEADERS = {**HEADERS, "Content-Type": "application/json", "Prefer": "return=minimal"}

FROM_EMAIL = "sujit@thebluewhale.online"
FROM_NAME = "Sujit"

# ── Subject Line Templates ──────────────────────────────

SUBJECTS = [
    "{name}'s new website — quick question",
    "cute. is {first_name} taking on more clients?",
    "Built something for {name} — thought you'd want to see",
    "Q about {name}'s online presence",
]

# ── Email Body Templates ────────────────────────────────

TEMPLATES = [
    # Template A: Humble + demo link
    """Hey {first_name},

Not sure if you're the right person, but I put together something for
{name} — an interactive demo of what your website could look like with
AI-powered booking, instant cost calculators, and 24/7 chat.

{emoji} {demo_url}

Already built it. No strings, no cost. If you like what you see, happy
to chat about making it real for {name}. If not, no worries at all.

Would genuinely love your thoughts either way.

Thanks,
{from_name}""",

    # Template B: Social proof + zero-risk
    """Hey {first_name},

Been helping local plumbing businesses in Wyoming upgrade their online
presence with AI-powered websites that actually book jobs.

I put together a free demo for {name} — interactive calculators,
24/7 AI chat, and instant booking. Here's what it looks like:

{emoji} {demo_url}

You don't pay anything unless it actually drives results. Already built
the demo — worst case, you spent 30 seconds looking at a cool website.

Want me to send over more details? Happy to jump on a quick call too.

Thanks,
{from_name}""",

    # Template C: Neighbor/local angle
    """Hey {first_name},

Q from a fellow {city} business watcher — I've been looking at plumbing
companies in the area and noticed {name} could use a refresh.

So I built one. Interactive cost calculators, AI chat, 24/7 booking.
Took a few minutes, and the result is here:

{emoji} {demo_url}

No catch. Not selling anything today. Just thought you'd find it
interesting — and if it sparks an idea, happy to talk.

Let me know what you think!

{from_name}""",
]


def get_leads(count=None, single_id=None):
    """Fetch A-tier plumbing leads that haven't been emailed yet."""
    if single_id:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/businesses"
            "?select=id,business_name,city,phone,email,website,rating,review_count,raw_data"
            f"&id=eq.{single_id}",
            headers=HEADERS,
        )
        if r.status_code != 200:
            print(f"DB error: {r.status_code}")
            return None
        data = r.json()
        if not data:
            print("Lead not found")
            return None
        lead = data[0]
        raw = lead.get("raw_data") or {}
        if isinstance(raw, str):
            try: raw = json.loads(raw)
            except: raw = {}
        lead["_score"] = raw.get("pipeline_score", 0)
        lead["_tier"] = raw.get("pipeline_tier", "D")
        lead["_demo_url"] = raw.get("demo_url", "")
        lead["_outreach_sent"] = raw.get("outreach_sent_at")
        return [lead]

    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/businesses"
        "?select=id,business_name,city,phone,email,website,rating,review_count,raw_data"
        "&industry=eq.plumbers"
        "&order=raw_data->pipeline_score.desc"
        "&limit=300",
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

        tier = raw.get("pipeline_tier", "D")
        if tier != "A":
            continue

        # Skip already-sent leads
        if raw.get("outreach_sent_at"):
            continue

        lead["_score"] = raw.get("pipeline_score", 0)
        lead["_tier"] = tier
        lead["_demo_url"] = raw.get("demo_url", "")
        lead["_outreach_sent"] = raw.get("outreach_sent_at")

        filtered.append(lead)

    if count:
        filtered = filtered[:count]
    return filtered


def pick_subject(lead):
    """Pick a subject line randomly and fill placeholders."""
    import random
    name = lead.get("business_name", "")
    first = name.split()[0] if name.split() else name
    template = random.choice(SUBJECTS)
    return template.format(name=name, first_name=first)


def pick_body(lead, template_idx=None):
    """Fill an email body template with lead data."""
    import random
    name = lead.get("business_name", "")
    first = name.split()[0] if name.split() else name
    city = lead.get("city", "Wyoming")
    demo_url = lead.get("_demo_url", "")

    idx = template_idx if template_idx is not None else random.randint(0, len(TEMPLATES) - 1)
    template = TEMPLATES[idx]
    emoji = random.choice(["🔗", "👉", "📎"])

    return template.format(
        first_name=first,
        name=name,
        city=city,
        demo_url=demo_url,
        emoji=emoji,
        from_name=FROM_NAME,
    )


def send_email(to_email, to_name, subject, body, dry_run=False):
    """Send via Resend API. Returns (success, message_id or error)."""
    if dry_run:
        return True, "dry-run"

    payload = {
        "from": f"{FROM_NAME} <{FROM_EMAIL}>",
        "to": [f"{to_name} <{to_email}>"],
        "subject": subject,
        "text": body,
    }

    r = requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers={
            "Authorization": f"Bearer {RESEND_KEY}",
            "Content-Type": "application/json",
        },
        timeout=15,
    )

    if r.status_code in (200, 201):
        msg_id = r.json().get("id", "unknown")
        return True, msg_id
    else:
        return False, r.text[:200]


def update_lead(lead_id, subject, body, template_idx, resend_id=None):
    """Record outreach in Supabase."""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{lead_id}&select=raw_data",
        headers=HEADERS,
    )
    raw = {}
    if r.status_code == 200 and r.json():
        raw = r.json()[0].get("raw_data") or {}
    if isinstance(raw, str):
        raw = json.loads(raw) if raw else {}

    raw["outreach_sent_at"] = datetime.now().isoformat()
    raw["outreach_subject"] = subject[:100]
    raw["outreach_template"] = str(template_idx)
    raw["outreach_resend_id"] = resend_id or ""

    requests.patch(
        f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{lead_id}",
        json={"raw_data": raw},
        headers=PATCH_HEADERS,
    )


def main():
    dry_run = "--dry-run" in sys.argv
    send_all = "--all" in sys.argv
    count = None
    single_id = None
    template_idx = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--count":
            count = int(args[i + 1]); i += 2
        elif args[i] == "--lead":
            single_id = args[i + 1]; i += 2
        elif args[i] == "--template":
            template_idx = int(args[i + 1]); i += 2
        else:
            i += 1

    if not dry_run and not RESEND_KEY:
        print("❌ RESEND_API_KEY not set in .env")
        return

    if send_all and not count:
        count = None  # all unsent A-tier

    if not count and not single_id and not send_all:
        count = 3  # default: top 3

    print("╔══════════════════════════════════════╗")
    print("║   📨 Plumber Outreach Sender        ║")
    print("║   Resend + Cold Email Framework     ║")
    print("╚══════════════════════════════════════╝")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'} | From: {FROM_EMAIL}\n")

    leads = get_leads(count, single_id)
    if not leads:
        print("No leads found (all A-tier already sent or no matching leads)")
        return

    print(f"Sending to {len(leads)} leads\n{'='*55}")

    sent = 0
    failed = 0

    for i, lead in enumerate(leads):
        name = lead.get("business_name", "Unknown")
        email = lead.get("email", "")
        demo = lead.get("_demo_url", "no-demo")

        if not email or "@" not in email:
            print(f"[{i+1}] {name[:40]:40} ❌ No email")
            continue

        subject = pick_subject(lead)
        body = pick_body(lead, template_idx)

        print(f"[{i+1}/{len(leads)}] {name[:40]}")
        print(f"  Subject: {subject}")
        print(f"  To: {email[:35]}")
        print(f"  Demo: {demo}")

        if dry_run:
            print(f"  ✉️  [DRY RUN — not sent]\n")
            print(f"  ── Body ──")
            print(body[:300] + ("..." if len(body) > 300 else ""))
            print(f"  ─────────\n")
            sent += 1
            continue

        success, result = send_email(email, name, subject, body)

        if success:
            update_lead(lead["id"], subject, body, template_idx or 0, result)
            print(f"  ✅ Sent (Resend ID: {result[:20]})\n")
            sent += 1
        else:
            print(f"  ❌ Failed: {result[:100]}\n")
            failed += 1

    print(f"{'='*55}")
    print(f"✅ {sent} sent | ❌ {failed} failed")
    if dry_run:
        print("DRY RUN — no emails actually sent. Remove --dry-run to send.")


if __name__ == "__main__":
    main()
