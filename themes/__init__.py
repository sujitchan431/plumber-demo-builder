"""
Theme definitions for plumbing demo builder.
5 themes: bold, hero, minimal, modern, trust.
Each theme exposes get_styles() and get_accent() for the template engine.
"""

THEMES = {
    "minimal": {
        "name": "Minimal",
        "description": "Clean, professional — best for established plumbing companies (default)",
        "css": """
  :root { --bg: #f8fafc; --card: #ffffff; --accent: #2563eb; --accent-glow: #3b82f6; --text: #1e293b; --muted: #64748b; --danger: #dc2626; --blue: #0ea5e9; --light-bg: #f1f5f9; --border: #e2e8f0; }
  body { background: var(--bg); color: var(--text); }
  .hero { background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: #fff; }
  .hero .subtitle { color: rgba(255,255,255,0.8); }
  .hero .badge { background: rgba(255,255,255,0.2); color: #fff; }
  .hero .location { color: rgba(255,255,255,0.7); }
  .hero .rating-display { color: #fff; }
  .hero .stars { color: #ffd700; }
  .trust-bar { background: #fff; border-bottom: 1px solid var(--border); }
  .service-card { box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .calculator { background: #fff; border: 1px solid var(--border); }
  .calculator select { background: #f8fafc; color: var(--text); border: 1px solid var(--border); }
  .calc-tab { background: #f1f5f9; color: var(--text); border-color: var(--border); }
  .calc-tab.active { background: var(--accent); color: #fff; }
  .cta-section { background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%); border-radius: 0; margin: 0; }
  .cta-section h2 { color: #fff; }
  .chat-msg.bot { background: #f1f5f9; color: var(--text); }
  .chat-window { background: #fff; border-color: var(--border); box-shadow: 0 10px 40px rgba(0,0,0,0.15); }
  .chat-input-area input { background: #f8fafc; border-color: var(--border); color: var(--text); }
  footer { background: #fff; }
  .existing-site a { color: var(--muted); }
""",
        "accent_hex": "#2563eb",
    },
    "trust": {
        "name": "Trust",
        "description": "Warm, neighborhood feel — best for family-run shops and local hardware stores",
        "css": """
  :root { --bg: #fefce8; --card: #fffbeb; --accent: #d97706; --accent-glow: #f59e0b; --text: #3e2e1f; --muted: #78716c; --danger: #b91c1c; --blue: #0891b2; --light-bg: #fef3c7; --border: #e7d5a8; }
  body { background: var(--bg); color: var(--text); font-family: 'Georgia', 'Times New Roman', serif; }
  h1, h2, h3 { font-family: 'Georgia', serif; }
  .hero { background: linear-gradient(135deg, #78350f 0%, #92400e 100%); color: #fff; }
  .hero .subtitle { color: rgba(255,255,255,0.8); }
  .hero .badge { background: rgba(255,255,255,0.15); color: #ffd700; }
  .hero .location { color: rgba(255,255,255,0.7); }
  .hero .rating-display { color: #fff; }
  .hero .stars { color: #ffd700; }
  .trust-bar { background: #fff; border-bottom: 2px solid #d97706; }
  .trust-item .num { color: #92400e; }
  .service-card { background: #fff; border: 1px solid var(--border); border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  .service-card:hover { border-color: #d97706; }
  .calculator { background: #fff; border: 1px solid var(--border); }
  .calculator select { background: #fffbeb; color: var(--text); border: 1px solid var(--border); }
  .calc-tab { background: #fff; color: var(--text); border-color: var(--border); }
  .calc-tab.active { background: #92400e; color: #fff; }
  .btn-primary { background: #b45309; color: #fff; }
  .btn-primary:hover { background: #92400e; }
  .btn-outline { border-color: #92400e; color: #92400e; }
  .cta-section { background: linear-gradient(135deg, #451a03 0%, #78350f 100%); border-radius: 0; margin: 0; }
  .chat-msg.bot { background: #fef3c7; color: var(--text); }
  .chat-window { background: #fff; border-color: var(--border); }
  .chat-input-area input { background: #fffbeb; border-color: var(--border); color: var(--text); }
  .chat-header { background: #92400e; }
  footer { background: #fff; border-top: 2px solid #d97706; }
""",
        "accent_hex": "#d97706",
    },
    "hero": {
        "name": "Hero",
        "description": "Bold urgency — best for 24/7 emergency services and rapid-response plumbers",
        "css": """
  :root { --bg: #0a0a14; --card: #141428; --accent: #ff6b35; --accent-glow: #ff8c5a; --text: #e0e0e0; --muted: #888; --danger: #ff3333; --blue: #4da6ff; --light-bg: #1a1a2e; --border: rgba(255,255,255,0.05); }
  body { background: var(--bg); color: var(--text); }
  .hero { background: radial-gradient(ellipse at top, #1a1a2e 0%, #0a0a14 70%); color: var(--text); }
  .hero .subtitle { color: var(--muted); }
  .hero .badge { background: rgba(255,107,53,0.15); color: var(--accent-glow); }
  .hero .location { color: var(--muted); }
  .hero .stars { color: #FFD700; }
  .trust-bar { border-bottom: 1px solid var(--border); }
  .service-card { background: var(--card); border: 1px solid var(--border); }
  .service-card:hover { border-color: rgba(255,107,53,0.3); }
  .calculator { background: var(--card); border: 1px solid var(--border); }
  .calculator select { background: #0e0e1a; color: var(--text); border: 1px solid var(--border); }
  .calc-tab { background: transparent; color: var(--muted); border-color: rgba(255,255,255,0.08); }
  .calc-tab.active { background: var(--accent); color: #fff; }
  .cta-section { background: linear-gradient(135deg, #1a0f0a 0%, #0a0a14 100%); }
  .chat-msg.bot { background: #1e1e35; color: var(--text); }
  .chat-window { background: var(--card); border-color: var(--border); }
  .chat-input-area input { background: #0e0e1a; border-color: var(--border); color: var(--text); }
""",
        "accent_hex": "#ff6b35",
    },
    "bold": {
        "name": "Bold",
        "description": "Polished, high-authority — best for larger franchises and multi-location operations",
        "css": """
  :root { --bg: #ffffff; --card: #ffffff; --accent: #0f172a; --accent-glow: #1e293b; --text: #0f172a; --muted: #475569; --danger: #dc2626; --blue: #3b82f6; --light-bg: #f8fafc; --border: #e2e8f0; }
  body { background: #fff; color: var(--text); }
  .hero { background: #0f172a; color: #fff; }
  .hero .subtitle { color: #94a3b8; }
  .hero .badge { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
  .hero .location { color: #94a3b8; }
  .hero .rating-display { color: #fff; }
  .hero .stars { color: #ffd700; }
  .trust-bar { background: #f8fafc; border-bottom: 1px solid var(--border); }
  .trust-item .num { color: #0f172a; }
  .service-card { background: #fff; border: 1px solid var(--border); border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
  .service-card:hover { border-color: #0f172a; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
  .calculator { background: #fff; border: 1px solid var(--border); }
  .calculator select { background: #fff; color: var(--text); border: 1px solid var(--border); }
  .calc-tab { background: #f8fafc; color: var(--text); border-color: var(--border); }
  .calc-tab.active { background: #0f172a; color: #fff; }
  .btn-primary { background: #0f172a; color: #fff; border-radius: 4px; }
  .btn-primary:hover { background: #1e293b; }
  .btn-outline { border-color: #0f172a; color: #0f172a; border-radius: 4px; }
  .btn-emergency { background: #dc2626; color: #fff; border-radius: 4px; animation: none; }
  .cta-section { background: #f8fafc; border-top: 1px solid var(--border); border-radius: 0; margin: 0; }
  .cta-section h2 { color: #0f172a; }
  .chat-msg.bot { background: #f1f5f9; }
  .chat-window { background: #fff; border-color: var(--border); box-shadow: 0 4px 24px rgba(0,0,0,0.12); }
  .chat-input-area input { background: #fff; border-color: var(--border); color: var(--text); }
  .chat-header { background: #0f172a; color: #fff; }
  footer { background: #0f172a; color: #94a3b8; }
  .existing-site a { color: var(--muted); }
  .section h2 { color: #0f172a; }
""",
        "accent_hex": "#0f172a",
    },
    "modern": {
        "name": "Modern",
        "description": "Sleek, contemporary — best for tech-forward plumbing companies. Dark gradient with violet accents.",
        "css": """
  :root { --bg: #0f0f23; --card: #1a1a2e; --accent: #7c3aed; --accent-glow: #a78bfa; --text: #e2e8f0; --muted: #94a3b8; --danger: #ef4444; --blue: #818cf8; --light-bg: #16213e; --border: rgba(255,255,255,0.06); }
  body { background: var(--bg); color: var(--text); font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .hero { background: linear-gradient(160deg, #1e1b4b 0%, #0f0f23 40%, #1a1a2e 100%); color: #fff; position: relative; overflow: hidden; }
  .hero::before { content: ''; position: absolute; top: -50%; right: -20%; width: 600px; height: 600px; background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%); border-radius: 50%; }
  .hero .subtitle { color: #a78bfa; }
  .hero .badge { background: rgba(124,58,237,0.2); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
  .hero .location { color: #94a3b8; }
  .hero .rating-display { color: #fff; }
  .hero .stars { color: #fbbf24; }
  .trust-bar { background: var(--card); border-bottom: 1px solid var(--border); }
  .trust-item .num { color: #a78bfa; }
  .service-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.2); transition: transform 0.2s, border-color 0.2s; }
  .service-card:hover { border-color: rgba(124,58,237,0.5); transform: translateY(-2px); }
  .calculator { background: var(--card); border: 1px solid var(--border); border-radius: 12px; }
  .calculator select { background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 8px; }
  .calc-tab { background: transparent; color: var(--muted); border: 1px solid var(--border); border-radius: 8px; }
  .calc-tab.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .btn-primary { background: var(--accent); color: #fff; border-radius: 8px; font-weight: 600; }
  .btn-primary:hover { background: #6d28d9; box-shadow: 0 4px 16px rgba(124,58,237,0.3); }
  .btn-outline { border-color: var(--accent); color: var(--accent); border-radius: 8px; }
  .btn-emergency { background: var(--danger); color: #fff; border-radius: 8px; animation: pulse-modern 2s infinite; }
  @keyframes pulse-modern { 0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); } 50% { box-shadow: 0 0 0 12px rgba(239,68,68,0); } }
  .cta-section { background: linear-gradient(160deg, #1e1b4b 0%, #0f0f23 100%); border-radius: 0; margin: 0; }
  .cta-section h2 { color: #fff; }
  .chat-msg.bot { background: #16213e; color: var(--text); }
  .chat-window { background: var(--card); border: 1px solid var(--border); border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
  .chat-input-area input { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; color: var(--text); }
  .chat-header { background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); }
  footer { background: var(--card); border-top: 1px solid var(--border); color: var(--muted); }
  .existing-site a { color: var(--muted); }
  .section h2 { color: #e2e8f0; }
""",
        "accent_hex": "#7c3aed",
    },
}


def detect_theme(business_name: str) -> str:
    """Auto-detect the best theme for a business based on name keywords."""
    name_lower = business_name.lower()

    # Emergency/24/7 → Hero
    if any(w in name_lower for w in ["24/7", "emergency", "express", "rapid", "quick", "911", "rescue", "fire"]):
        return "hero"

    # Hardware, family-run → Trust
    if any(w in name_lower for w in ["hardware", "true value", "ace", "family", "home depot", "lowe", "local"]):
        return "trust"

    # Franchise, large ops → Bold
    if any(w in name_lower for w in ["pro", "group", "corp", "inc", "llc", "enterprise", "partner", "solution", "system"]):
        return "bold"

    # Tech-forward keywords → Modern
    if any(w in name_lower for w in ["tech", "smart", "digital", "flow", "solution", "innovation", "green", "eco"]):
        return "modern"

    # Default → Minimal
    return "minimal"
