"""OKJ API v5 — HTTP constants and endpoint paths.

All endpoint path constants are grouped by domain (account, funding, market,
trade).  Prefer importing from this module explicitly rather than
using ``from okj.consts import *``.
"""

# ── Base URL ─────────────────────────────────────────────────────────────────
DEFAULT_BASE_URL: str = "https://api.okj.com"

# ── WebSocket URLs ───────────────────────────────────────────────────────────
# Named here so callers stop retyping them, but deliberately *not* wired up as
# defaults on the WebSocket clients: their ``url`` stays a required argument. A
# default would mean that forgetting the parameter connects to production, and on
# a trading SDK the quiet version of that mistake is the expensive one. REST can
# afford a default because reads are harmless; a private WebSocket subscribes to
# a real account.
DEFAULT_WS_PUBLIC_URL: str = "wss://ws.okj.com/ws/v5/public"
DEFAULT_WS_PRIVATE_URL: str = "wss://ws.okj.com/ws/v5/private"
DEFAULT_WS_BUSINESS_URL: str = "wss://ws.okj.com/ws/v5/business"

# ── HTTP Methods ─────────────────────────────────────────────────────────────
GET = "GET"
POST = "POST"

# ── Request Header Keys ───────────────────────────────────────────────────────
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"

OK_ACCESS_KEY = "OK-ACCESS-KEY"
OK_ACCESS_SIGN = "OK-ACCESS-SIGN"
OK_ACCESS_TIMESTAMP = "OK-ACCESS-TIMESTAMP"
OK_ACCESS_PASSPHRASE = "OK-ACCESS-PASSPHRASE"

# ── Public Data endpoints ─────────────────────────────────────────────────────
INSTRUMENT_INFO = "/api/v5/public/instruments"
SYSTEM_TIME = "/api/v5/public/time"

# ── Account endpoints ─────────────────────────────────────────────────────────
ACCOUNT_INFO = "/api/v5/account/balance"
BILLS_DETAIL = "/api/v5/account/bills"
BILLS_ARCHIVE = "/api/v5/account/bills-archive"
ACCOUNT_CONFIG = "/api/v5/account/config"
MAX_TRADE_SIZE = "/api/v5/account/max-size"
MAX_AVAIL_SIZE = "/api/v5/account/max-avail-size"
FEE_RATES = "/api/v5/account/trade-fee"
FEE_RATES_ALL = "/api/v5/account/trade-fee-all"
MAX_WITHDRAWAL = "/api/v5/account/max-withdrawal"
GET_INSTRUMENTS = "/api/v5/account/instruments"

# ── Funding / Asset endpoints ─────────────────────────────────────────────────
DEPOSIT_ADDRESS = "/api/v5/asset/deposit/address"
GET_BALANCES = "/api/v5/asset/wallet"
FUNDS_TRANSFER = "/api/v5/asset/transfer"
WITHDRAWAL_COIN = "/api/v5/asset/withdrawal"
DEPOSIT_HISTORY = "/api/v5/asset/deposit/history"
WITHDRAWAL_HISTORY = "/api/v5/asset/withdrawal/history"
CURRENCY_INFO = "/api/v5/asset/currencies"
ASSET_VALUATION = "/api/v5/asset/asset-valuation"
LEDGER_RECORD = "/api/v5/asset/ledger"
BANK_CARD_LIST = "/api/v5/asset/bank-card-list"
FIAT_WITHDRAW = "/api/v5/asset/jpywithdrawal"
FIAT_WITHDRAW_RECORD = "/api/v5/asset/jpyWithdrawal/history"
FIAT_DEPOSIT_RECORD = "/api/v5/asset/jpyDeposit/history"
COIN_FEE = "/api/v5/asset/withdrawal/fee"

# ── Market Data endpoints ─────────────────────────────────────────────────────
TICKERS_INFO = "/api/v5/market/tickers"
TICKER_INFO = "/api/v5/market/ticker"
ORDER_BOOKS = "/api/v5/market/books"
GET_BOOKS_FULL = "/api/v5/market/books-full"
MARKET_CANDLES = "/api/v5/market/candles"
HISTORY_CANDLES = "/api/v5/market/history-candles"
MARKET_TRADES = "/api/v5/market/trades"
VOLUME = "/api/v5/market/platform-24-volume"
GET_CALL_AUCTION_DETAILS = "/api/v5/market/call-auction-details"

# ── Trade endpoints ───────────────────────────────────────────────────────────
PLACE_ORDER = "/api/v5/trade/order"
BATCH_ORDERS = "/api/v5/trade/batch-orders"
CANCEL_ORDER = "/api/v5/trade/cancel-order"
CANCEL_BATCH_ORDERS = "/api/v5/trade/cancel-batch-orders"
AMEND_ORDER = "/api/v5/trade/amend-order"
AMEND_BATCH_ORDER = "/api/v5/trade/amend-batch-orders"
CLOSE_POSITION = "/api/v5/trade/close-position"
ORDER_INFO = "/api/v5/trade/order"
ORDERS_PENDING = "/api/v5/trade/orders-pending"
ORDERS_HISTORY = "/api/v5/trade/orders-history"
ORDERS_HISTORY_ARCHIVE = "/api/v5/trade/orders-history-archive"
ORDER_FILLS = "/api/v5/trade/fills"
ORDERS_FILLS_HISTORY = "/api/v5/trade/fills-history"
CANCEL_ALL_ORDERS = "/api/v5/trade/cancel-all-after"
PLACE_ALGO_ORDER = "/api/v5/trade/order-algo"
CANCEL_ALGOS = "/api/v5/trade/cancel-algos"
GET_ALGO_ORDER_DETAILS = "/api/v5/trade/order-algo"
ORDERS_ALGO_PENDING = "/api/v5/trade/orders-algo-pending"
ORDERS_ALGO_HISTORY = "/api/v5/trade/orders-algo-history"
AMEND_ALGO_ORDER = "/api/v5/trade/amend-algos"
