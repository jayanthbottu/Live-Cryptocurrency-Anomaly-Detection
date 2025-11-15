# 🚀 Elite Market Intelligence Dashboard

> **Advanced Real-Time Market Monitoring System with ML-Powered Anomaly Detection**

A cutting-edge trading dashboard that combines cryptocurrency market data with Indian stock indices (NIFTY, SENSEX) for comprehensive market analysis. Features real-time anomaly detection, advanced technical indicators, and interactive visualizations.

---

## ✨ Key Features

### 🎯 **Core Capabilities**
- 📊 **Real-Time Data Streaming** - Live cryptocurrency prices from Binance
- 🇮🇳 **Indian Market Integration** - NIFTY 50, SENSEX, NIFTY BANK monitoring
- 🤖 **AI-Powered Anomaly Detection** - Machine learning algorithms detect market anomalies
- 📈 **Advanced Technical Analysis** - 15+ technical indicators (RSI, MACD, Bollinger Bands, etc.)
- 🎨 **Professional UI** - Dark theme with gradient designs and smooth animations
- ⚡ **Lightning Fast** - Optimized for performance with auto-refresh capabilities

### 🧠 **Anomaly Detection Algorithms**
1. **Volatility Anomalies** - Z-score based detection
2. **Volume Spikes** - Isolation Forest algorithm
3. **Price Pattern Anomalies** - Statistical breakout detection
4. **Multi-Feature Analysis** - Combined feature anomaly detection
5. **Severity Classification** - Automatic risk level assessment

### 📊 **Technical Indicators**
- Moving Averages (SMA 20, 50, 200)
- Exponential Moving Averages (EMA 12, 26)
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Bollinger Bands
- ATR (Average True Range)
- Volume Analysis
- Price Momentum

---

## 🛠️ Installation Guide

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Binance API credentials (free account)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/market-intelligence-dashboard.git
cd market-intelligence-dashboard
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Required Packages:**
```txt
streamlit==1.28.0
pandas==2.1.1
numpy==1.24.3
plotly==5.17.0
python-binance==1.0.17
scikit-learn==1.3.1
scipy==1.11.3
python-dotenv==1.0.0
requests==2.31.0
```

### **Step 4: Configure API Keys**

Create a `.env` file in the project root:

```bash
# .env
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
```

**How to Get Binance API Keys:**
1. Visit [Binance.com](https://www.binance.com)
2. Register/Login to your account
3. Go to **Account** → **API Management**
4. Create a new API key
5. **Important:** Enable "Enable Reading" (no trading permissions needed)
6. Copy API Key and Secret to `.env` file

### **Step 5: Project Structure**

Create the following directory structure:

```
market-intelligence-dashboard/
│
├── src/
│   ├── config/
│   │   └── settings.py          # Configuration file
│   ├── data_fetcher.py           # Binance API integration
│   ├── anomaly_detector.py       # ML anomaly detection
│   └── app.py                    # Main Streamlit application
│
├── logs/                         # Application logs
├── exports/                      # Data export directory
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

### **Step 6: Create Required Files**

**data_fetcher.py** - Create this file in `src/`:
```python
from binance.client import Client
import pandas as pd
from config.settings import BINANCE_API_KEY, BINANCE_API_SECRET

class BinanceDataFetcher:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    
    def get_klines(self, symbol, interval, limit=200):
        """Fetch OHLCV data from Binance"""
        klines = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
```

---

## 🚀 Running the Dashboard

### **Start the Application**
```bash
streamlit run src/app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

### **Alternative: Specify Port**
```bash
streamlit run src/app.py --server.port 8080
```

---

## 📱 Usage Guide

### **1. Market Selection**
- **🪙 Cryptocurrency** - Monitor Bitcoin, Ethereum, and 20+ crypto pairs
- **📈 Indian Indices** - Track NIFTY 50, SENSEX, NIFTY BANK
- **🌐 Combined View** - Overview of both markets simultaneously

### **2. Customize Settings**
- **Timeframe:** Choose from 1m, 5m, 15m, 1h, 4h, 1d
- **Data Points:** Adjust historical data range (50-500 candles)
- **Auto-Refresh:** Enable automatic updates (3-30 seconds)
- **Indicators:** Toggle technical indicators on/off
- **Sensitivity:** Adjust anomaly detection sensitivity

### **3. Reading the Charts**

**Color Coding:**
- 🟢 **Green Candles** - Price increased
- 🔴 **Red Candles** - Price decreased
- 🔺 **Red Triangles** - Volatility anomaly detected
- 🔶 **Orange Diamonds** - Volume spike detected

**Indicator Lines:**
- **Orange Line** - 20-period Simple Moving Average
- **Blue Line** - 50-period Simple Moving Average
- **Gray Dashed Lines** - Bollinger Bands (volatility zones)

### **4. Understanding Anomalies**

**Severity Levels:**
- ✅ **Normal** - No anomalies detected
- 🟡 **Low** - Minor deviation from normal
- 🟠 **Medium** - Moderate anomaly, monitor closely
- 🔴 **High** - Significant anomaly, high risk

### **5. Technical Indicators Interpretation**

**RSI (Relative Strength Index):**
- **>70** = Overbought (potential reversal down)
- **<30** = Oversold (potential reversal up)
- **30-70** = Neutral zone

**MACD:**
- **MACD > Signal** = Bullish momentum
- **MACD < Signal** = Bearish momentum
- **Crossovers** = Potential trend changes

---

## 🎨 Dashboard Features

### **Real-Time Metrics**
- 💰 Current Price
- 📈 24h High/Low
- 📊 Trading Volume
- 🎯 RSI Value
- 📉 Trend Direction

### **Interactive Charts**
- **Candlestick Chart** - OHLC price action
- **Volume Bars** - Trading volume visualization
- **RSI Panel** - Momentum indicator
- **Multiple Indicators** - Overlay technical analysis

### **Alert System**
- Price change notifications
- Volume spike alerts
- Anomaly warnings
- Trend reversal signals

### **Data Export**
- CSV format for Excel
- JSON for further analysis
- PDF reports (coming soon)

---

## 🔧 Advanced Configuration

### **Modify Anomaly Sensitivity**

Edit `src/config/settings.py`:
```python
ANOMALY_THRESHOLD = 3.0  # Increase for fewer alerts, decrease for more
VOLUME_CONTAMINATION = 0.1  # Percentage of anomalies
```

### **Add Custom Cryptocurrency Pairs**

Edit `SYMBOLS` list in `settings.py`:
```python
SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "YOURTOKENUSDT",  # Add your token here
]
```

### **Customize Indicator Periods**
```python
INDICATOR_SETTINGS = {
    "RSI": {"period": 14},  # Change to your preference
    "SMA": {"short": 20, "long": 50},
}
```

---

## 📊 Indian Market Integration

### **Current Implementation**
The dashboard includes simulated data for:
- **NIFTY 50** - NSE Benchmark Index
- **SENSEX** - BSE Benchmark Index
- **NIFTY BANK** - Banking Sector Index

### **Integration with Live Data**

To connect with real Indian market data, integrate with:

**Option 1: NSE Python API**
```bash
pip install nsepython
```

**Option 2: Yahoo Finance**
```bash
pip install yfinance
```

**Option 3: AlphaVantage**
```bash
pip install alpha_vantage
```

---

## 🐛 Troubleshooting

### **Common Issues**

**1. API Key Errors**
```
Error: Invalid API key
```
**Solution:** Check `.env` file has correct credentials

**2. Rate Limit Exceeded**
```
Error: 429 Too Many Requests
```
**Solution:** Reduce refresh rate or wait 1 minute

**3. Module Not Found**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Activate virtual environment and reinstall dependencies

**4. Connection Timeout**
```
ConnectionError: Unable to connect to Binance
```
**Solution:** Check internet connection and Binance API status

### **Debug Mode**

Run with verbose logging:
```bash
streamlit run src/app.py --logger.level=debug
```

---

## 🎓 Educational Resources

### **Learn Trading Basics**
- [Investopedia - Trading](https://www.investopedia.com/trading-4427765)
- [Binance Academy](https://academy.binance.com/)
- [TradingView Education](https://www.tradingview.com/education/)

### **Technical Analysis**
- [Understanding RSI](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Indicator Guide](https://www.investopedia.com/terms/m/macd.asp)
- [Bollinger Bands Explained](https://www.investopedia.com/terms/b/bollingerbands.asp)

### **Machine Learning in Trading**
- [Anomaly Detection Methods](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [Time Series Analysis](https://www.tensorflow.org/tutorials/structured_data/time_series)

---

## 🔒 Security Best Practices

1. **Never share your API keys**
2. **Use API keys with read-only permissions**
3. **Add `.env` to `.gitignore`**
4. **Regenerate keys if compromised**
5. **Enable 2FA on exchange accounts**

---

## 🚀 Future Enhancements

- [ ] Live NSE/BSE data integration
- [ ] Telegram/Discord alert bot
- [ ] Portfolio tracking
- [ ] Backtesting framework
- [ ] Social sentiment analysis
- [ ] News integration
- [ ] Mobile responsive design
- [ ] Multi-language support

---

## 📄 License

MIT License - Free to use and modify

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📧 Support

For issues and questions:
- **GitHub Issues:** [Open an issue](https://github.com/yourusername/repo/issues)
- **Email:** support@example.com
- **Discord:** [Join our community](#)

---

## ⭐ Show Your Support

If you find this project useful, please give it a ⭐ on GitHub!

---

<div align="center">

**Built with ❤️ using Python, Streamlit, and Machine Learning**

[Documentation](#) • [Report Bug](#) • [Request Feature](#)

</div>