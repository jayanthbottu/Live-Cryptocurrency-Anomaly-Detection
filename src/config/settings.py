# src/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# ============= API CREDENTIALS =============
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# ============= CRYPTOCURRENCY PAIRS =============
SYMBOLS = [
    # Major Coins
    "BTCUSDT",      # Bitcoin
    "ETHUSDT",      # Ethereum
    "BNBUSDT",      # Binance Coin
    "SOLUSDT",      # Solana
    "XRPUSDT",      # Ripple
    
    # DeFi & Smart Contract Platforms
    "ADAUSDT",      # Cardano
    "DOTUSDT",      # Polkadot
    "AVAXUSDT",     # Avalanche
    "MATICUSDT",    # Polygon
    "LINKUSDT",     # Chainlink
    
    # Meme & Popular Coins
    "DOGEUSDT",     # Dogecoin
    "SHIBUSDT",     # Shiba Inu
    "PEPEUSDT",     # Pepe
    
    # Additional Altcoins
    "UNIUSDT",      # Uniswap
    "LTCUSDT",      # Litecoin
    "ATOMUSDT",     # Cosmos
    "NEARUSDT",     # NEAR Protocol
    "APTUSDT",      # Aptos
    "ARBUSDT",      # Arbitrum
    "OPUSDT",       # Optimism
]

# ============= INDIAN MARKET INDICES =============
INDIAN_INDICES = {
    "NIFTY_50": {
        "name": "NIFTY 50",
        "symbol": "^NSEI",
        "base_value": 22500,
        "description": "NSE's benchmark index of top 50 companies"
    },
    "SENSEX": {
        "name": "SENSEX",
        "symbol": "^BSESN",
        "base_value": 74000,
        "description": "BSE's benchmark index of top 30 companies"
    },
    "NIFTY_BANK": {
        "name": "NIFTY BANK",
        "symbol": "^NSEBANK",
        "base_value": 48500,
        "description": "Index of top banking stocks"
    },
    "NIFTY_IT": {
        "name": "NIFTY IT",
        "symbol": "^CNXIT",
        "base_value": 35000,
        "description": "Index of top IT sector stocks"
    }
}

# ============= TRADING PARAMETERS =============
TIMEFRAME = "1m"  # Default timeframe
DEFAULT_LIMIT = 200  # Default number of candles to fetch

TIMEFRAME_OPTIONS = {
    "1m": {"name": "1 Minute", "seconds": 60},
    "5m": {"name": "5 Minutes", "seconds": 300},
    "15m": {"name": "15 Minutes", "seconds": 900},
    "30m": {"name": "30 Minutes", "seconds": 1800},
    "1h": {"name": "1 Hour", "seconds": 3600},
    "4h": {"name": "4 Hours", "seconds": 14400},
    "1d": {"name": "1 Day", "seconds": 86400},
}

# ============= ANOMALY DETECTION PARAMETERS =============
ANOMALY_THRESHOLD = 3.0  # Z-score threshold for volatility anomalies
VOLUME_CONTAMINATION = 0.1  # Percentage of data considered as anomalies
MULTI_FEATURE_CONTAMINATION = 0.15  # For multi-feature anomaly detection

# Statistical thresholds
PRICE_SPIKE_THRESHOLD = 0.05  # 5% sudden price change
BOLLINGER_BAND_MULTIPLIER = 2.0  # Standard deviations for Bollinger Bands

# ============= TECHNICAL INDICATORS =============
INDICATOR_SETTINGS = {
    "SMA": {
        "short": 20,
        "long": 50,
        "extra_long": 200
    },
    "EMA": {
        "fast": 12,
        "slow": 26,
        "signal": 9
    },
    "RSI": {
        "period": 14,
        "overbought": 70,
        "oversold": 30
    },
    "MACD": {
        "fast": 12,
        "slow": 26,
        "signal": 9
    },
    "BOLLINGER": {
        "period": 20,
        "std_dev": 2
    },
    "ATR": {
        "period": 14
    },
    "STOCHASTIC": {
        "k_period": 14,
        "d_period": 3
    }
}

# ============= ALERT SETTINGS =============
ALERT_THRESHOLDS = {
    "price_change_percent": 5.0,  # Alert if price changes by 5%
    "volume_multiplier": 3.0,  # Alert if volume is 3x average
    "rsi_overbought": 80,
    "rsi_oversold": 20,
    "volatility_spike": 3.5,  # Z-score threshold
}

# ============= DASHBOARD SETTINGS =============
REFRESH_INTERVALS = {
    "fast": 3,      # 3 seconds
    "normal": 5,    # 5 seconds
    "slow": 10,     # 10 seconds
    "manual": None  # Manual refresh only
}

CHART_THEMES = {
    "dark": "plotly_dark",
    "light": "plotly_white",
    "cyberpunk": "plotly_dark"  # Custom styling
}

# Color schemes
COLOR_SCHEME = {
    "bullish": "#00ff88",
    "bearish": "#ff4444",
    "neutral": "#888888",
    "warning": "#ffe3ab",
    "danger": "#f6a1a1",
    "success": "#00ff00",
    "info": "#00aaff",
    "gradient_primary": ["#00f260", "#0575e6"],
    "gradient_secondary": ["#667eea", "#764ba2"],
}

# ============= RISK MANAGEMENT =============
RISK_LEVELS = {
    "low": {
        "color": "green",
        "threshold": 0.02,
        "description": "Low volatility - Safe to trade"
    },
    "medium": {
        "color": "cyan",
        "threshold": 0.05,
        "description": "Moderate volatility - Exercise caution"
    },
    "high": {
        "color": "orange",
        "threshold": 0.10,
        "description": "High volatility - Risk warning"
    },
    "extreme": {
        "color": "red",
        "threshold": float('inf'),
        "description": "Extreme volatility - Avoid trading"
    }
}

# ============= API RATE LIMITS =============
BINANCE_RATE_LIMITS = {
    "requests_per_minute": 1200,
    "orders_per_second": 10,
    "orders_per_day": 200000,
}

# ============= DATA RETENTION =============
DATA_RETENTION = {
    "intraday": 7,      # Keep 7 days of minute data
    "daily": 365,       # Keep 1 year of daily data
    "cache_ttl": 60,    # Cache timeout in seconds
}

# ============= LOGGING CONFIGURATION =============
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/trading_dashboard.log"

# ============= FEATURE FLAGS =============
FEATURES = {
    "enable_live_trading": False,      # Disable real trading by default
    "enable_backtesting": True,
    "enable_ml_predictions": True,
    "enable_social_sentiment": False,  # Future feature
    "enable_news_integration": False,  # Future feature
    "enable_telegram_alerts": False,   # Future feature
}

# ============= ADVANCED ANALYTICS =============
ANALYTICS_CONFIG = {
    "enable_correlation_matrix": True,
    "enable_market_regime_detection": True,
    "enable_pattern_recognition": True,
    "enable_seasonal_analysis": True,
    "min_data_points": 100,
}

# ============= MACHINE LEARNING =============
ML_CONFIG = {
    "models": {
        "isolation_forest": {
            "n_estimators": 200,
            "contamination": 0.1,
            "random_state": 42,
            "max_samples": "auto",
        },
        "lstm": {
            "units": 50,
            "epochs": 50,
            "batch_size": 32,
            "lookback": 60,
        }
    },
    "feature_engineering": {
        "use_technical_indicators": True,
        "use_volume_profile": True,
        "use_price_action": True,
        "normalize_features": True,
    }
}

# ============= EXPORT SETTINGS =============
EXPORT_FORMATS = ["CSV", "Excel", "JSON", "PDF"]
EXPORT_PATH = "exports/"

# ============= NOTIFICATIONS =============
NOTIFICATION_CHANNELS = {
    "email": {
        "enabled": False,
        "smtp_server": "",
        "smtp_port": 587,
    },
    "telegram": {
        "enabled": False,
        "bot_token": "",
        "chat_id": "",
    },
    "discord": {
        "enabled": False,
        "webhook_url": "",
    }
}

# ============= SYSTEM INFO =============
APP_VERSION = "2.0.0"
APP_NAME = "Elite Market Intelligence Dashboard"
AUTHOR = "AI Trading Systems"
DESCRIPTION = "Advanced real-time market monitoring with ML-powered anomaly detection"