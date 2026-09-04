"""API credentials configuration for test examples.

Copy this file or set the values below before running any example script.

WARNING: Never commit real API keys to version control.
         Consider loading credentials from environment variables instead:

    import os
    API_KEY = os.environ["OKJ_API_KEY"]
    API_SECRET_KEY = os.environ["OKJ_API_SECRET_KEY"]
    PASSPHRASE = os.environ["OKJ_PASSPHRASE"]
"""

# ── REST API credentials ───────────────────────────────────────────────────────
API_KEY = "your_api_key"
API_SECRET_KEY = "your_api_secret_key"
PASSPHRASE = "your_passphrase"

# ── Base URL (switch between environments) ────────────────────────────────────
# Production
DOMAIN = "https://api.okj.com"

# ── WebSocket URLs ────────────────────────────────────────────────────────────
# Production
PRIVATE_URL = "wss://ws.okj.com/ws/v5/private"
BUSINESS_URL = "wss://ws.okj.com/ws/v5/business"
PUBLIC_URL = "wss://ws.okj.com/ws/v5/public"
