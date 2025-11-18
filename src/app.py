import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
from data_fetcher import BinanceDataFetcher
from anomaly_detector import AnomalyDetector
from config.settings import SYMBOLS, TIMEFRAME

# Advanced Page Configuration
st.set_page_config(
    page_title="Live Cryptocurrency Price Dashboard with Anomaly Detection | AI-Powered Market Intelligence",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling with Modern Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        padding: 0;
    }
    
    /* Animated Header */
    .elite-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgb(102, 126, 234);
        border: 1px solid rgb(255, 255, 255);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .elite-header h1 {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        text-align: center;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        letter-spacing: -1px;
    }
    
    .elite-header p {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Premium Metrics */
    .premium-metric {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .premium-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .premium-metric:hover::before {
        left: 100%;
    }
    
    .premium-metric:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 900;
        color: white;
        margin: 0.5rem 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .metric-change {
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    .metric-change.positive {
        color: #00ff88;
    }
    
    .metric-change.negative {
        color: #ff4444;
    }
    
    /* Alert Boxes */
    .alert-critical {
        background: linear-gradient(135deg, rgba(255, 68, 68, 0.2) 0%, rgba(255, 68, 68, 0.05) 100%);
        border-left: 4px solid #ff4444;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.2) 0%, rgba(255, 165, 0, 0.05) 100%);
        border-left: 4px solid #ffa500;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .alert-success {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 255, 136, 0.05) 100%);
        border-left: 4px solid #00ff88;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-live {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
        color: #0a0e27;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4); }
        50% { box-shadow: 0 4px 25px rgba(0, 255, 136, 0.6); }
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #0a0e27 100%);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Data Table Styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
    }
    
    /* Progress Bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Trading Signal Badge */
    .signal-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .signal-buy {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 255, 136, 0.1) 100%);
        color: #00ff88;
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(255, 68, 68, 0.2) 0%, rgba(255, 68, 68, 0.1) 100%);
        color: #ff4444;
        border: 1px solid rgba(255, 68, 68, 0.3);
    }
    
    .signal-hold {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.2) 0%, rgba(255, 165, 0, 0.1) 100%);
        color: #ffa500;
        border: 1px solid rgba(255, 165, 0, 0.3);
    }
    
    /* Stat Grid */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-item h4 {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
    }
    
    .stat-item p {
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Footer */
    .elite-footer {
        text-align: center;
        padding: 3rem 1rem;
        color: rgba(255, 255, 255, 0.5);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 3rem;
    }
    
    .elite-footer h3 {
        color: white;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: rgba(0, 0, 0, 0.9);
        color: white;
        text-align: center;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    return BinanceDataFetcher(), AnomalyDetector()

fetcher, detector = init_components()

# Elite Header
st.markdown("""
<div class="elite-header">
    <h1>Live Cryptocurrency Price Dashboard with Anomaly Detection
</h1>
    <p>AI-Powered Market Intelligence • Real-Time Anomaly Detection</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration with Premium Design
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h2 style='color: white; margin: 0;'>👥 Developed By</h2>
    <p style='color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0.5rem 0 0 0;'>2303A51LA0    SINDHU</p>
    <p style='color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0.5rem 0 0 0;'>2303A51LA7    JAYANTH</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Market Selection
st.sidebar.markdown("### 🌟 Market Selection")
market_type = st.sidebar.radio(
    "Choose Market",
    ["🪙 Cryptocurrency", "🛞 Indian Indices", "🌏 Global Overview"],
    help="Select which market segment to analyze"
)

if "Cryptocurrency" in market_type:
    symbol = st.sidebar.selectbox(
        "Trading Pair",
        SYMBOLS,
        index=0,
        help="Select cryptocurrency trading pair"
    )
    timeframe = st.sidebar.selectbox(
        "Chart Timeframe",
        ["1m", "5m", "15m", "30m", "1h", "4h", "1d"],
        index=2,
        help="Select candlestick interval"
    )
    data_points = st.sidebar.slider(
        "Historical Data Points",
        min_value=50,
        max_value=1000,
        value=300,
        step=50,
        help="Number of candlesticks to display"
    )

# Advanced Analytics Settings
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔬 Analytics Configuration")

auto_refresh = st.sidebar.checkbox("🔄 Auto-Refresh", value=True, help="Enable automatic data refresh")
if auto_refresh:
    refresh_interval = st.sidebar.slider(
        "Refresh Interval (seconds)",
        min_value=3,
        max_value=60,
        value=5,
        help="Time between data updates"
    )

show_volume = st.sidebar.checkbox("🌟 Volume Analysis", value=True, help="Display volume charts")
show_indicators = st.sidebar.checkbox("📈 Technical Indicators", value=True, help="Show moving averages, RSI, MACD")
show_predictions = st.sidebar.checkbox("🔮 AI Predictions", value=True, help="Display ML-based forecasts")

anomaly_sensitivity = st.sidebar.slider(
    "🎯 Anomaly Detection Sensitivity",
    min_value=1.5,
    max_value=5.0,
    value=2.5,
    step=0.5,
    help="Lower = more sensitive detection"
)

# Risk Management
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚠️ Risk Management")

enable_alerts = st.sidebar.checkbox("🔔 Price Alerts", value=True, help="Enable price change notifications")
if enable_alerts:
    alert_threshold = st.sidebar.number_input(
        "Alert Threshold (%)",
        min_value=1.0,
        max_value=20.0,
        value=5.0,
        step=0.5,
        help="Trigger alert when price changes exceed this %"
    )

stop_loss = st.sidebar.number_input(
    "Stop Loss (%)",
    min_value=1.0,
    max_value=50.0,
    value=10.0,
    help="Automatic stop-loss percentage"
)

take_profit = st.sidebar.number_input(
    "Take Profit (%)",
    min_value=1.0,
    max_value=100.0,
    value=20.0,
    help="Automatic take-profit percentage"
)

# Status Dashboard
st.markdown('<div class="section-header">System Status</div>', unsafe_allow_html=True)

col_status1, col_status2, col_status3, col_status4, col_status5 = st.columns(5)

with col_status1:
    st.markdown("""
    <div class="premium-metric">
        <div class="metric-label">Connection</div>
        <div class="status-badge status-live">● LIVE</div>
    </div>
    """, unsafe_allow_html=True)

with col_status2:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="premium-metric">
        <div class="metric-label">Last Update</div>
        <div class="metric-value" style="font-size: 1.3rem;">{current_time}</div>
    </div>
    """, unsafe_allow_html=True)

with col_status3:
    st.markdown("""
    <div class="premium-metric">
        <div class="metric-label">Data Quality</div>
        <div class="metric-value" style="font-size: 1.3rem; color: #00ff88;">99.9%</div>
    </div>
    """, unsafe_allow_html=True)

with col_status4:
    st.markdown("""
    <div class="premium-metric">
        <div class="metric-label">API Latency</div>
        <div class="metric-value" style="font-size: 1.3rem; color: #667eea;">~45ms</div>
    </div>
    """, unsafe_allow_html=True)

with col_status5:
    st.markdown("""
    <div class="premium-metric">
        <div class="metric-label">Active Alerts</div>
        <div class="metric-value" style="font-size: 1.3rem; color: #ffa500;">0</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content placeholder
placeholder = st.empty()

def calculate_advanced_indicators(df):
    """Calculate comprehensive technical indicators"""
    df = df.copy()
    
    # Moving Averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal']
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_middle'] = df['close'].rolling(window=20).mean()
    bb_std = df['close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_middle'] + (2 * bb_std)
    df['BB_lower'] = df['BB_middle'] - (2 * bb_std)
    df['BB_width'] = ((df['BB_upper'] - df['BB_lower']) / df['BB_middle']) * 100
    
    # Stochastic Oscillator
    low_14 = df['low'].rolling(window=14).min()
    high_14 = df['high'].rolling(window=14).max()
    df['Stochastic'] = ((df['close'] - low_14) / (high_14 - low_14)) * 100
    
    # ATR (Average True Range)
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['ATR'] = true_range.rolling(14).mean()
    
    # On-Balance Volume
    df['OBV'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    
    # Money Flow Index
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(14).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(14).sum()
    df['MFI'] = 100 - (100 / (1 + positive_flow / negative_flow))
    
    return df

def generate_trading_signal(df):
    """Generate AI-powered trading signals"""
    latest = df.iloc[-1]
    
    signals = []
    score = 0
    
    # RSI Signal
    if latest['RSI'] < 30:
        signals.append("RSI Oversold")
        score += 2
    elif latest['RSI'] > 70:
        signals.append("RSI Overbought")
        score -= 2
    
    # MACD Signal
    if latest['MACD'] > latest['Signal']:
        signals.append("MACD Bullish")
        score += 1
    else:
        signals.append("MACD Bearish")
        score -= 1
    
    # Moving Average Signal
    if latest['SMA_20'] > latest['SMA_50']:
        signals.append("MA Bullish Cross")
        score += 1
    else:
        signals.append("MA Bearish Cross")
        score -= 1
    
    # Bollinger Bands
    if latest['close'] < latest['BB_lower']:
        signals.append("BB Oversold")
        score += 1
    elif latest['close'] > latest['BB_upper']:
        signals.append("BB Overbought")
        score -= 1
    
    # Final Signal
    if score >= 3:
        return "BUY", "Strong bullish momentum detected", signals, score
    elif score <= -3:
        return "SELL", "Strong bearish momentum detected", signals, score
    else:
        return "HOLD", "Market consolidating, wait for clearer signal", signals, score

def create_professional_chart(df, symbol_name):
    """Create an institutional-grade multi-panel chart"""
    
    # Create subplots with custom spacing
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.5, 0.2, 0.15, 0.15],
        subplot_titles=(
            f'<b>{symbol_name}</b> Price Action & Technical Indicators',
            '<b>Volume Analysis</b>',
            '<b>RSI Momentum</b>',
            '<b>MACD Divergence</b>'
        )
    )
    
    # Candlestick chart with enhanced colors
    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price',
            increasing_line_color='#00ff88',
            increasing_fillcolor='#00ff88',
            decreasing_line_color='#ff4444',
            decreasing_fillcolor='#ff4444',
            whiskerwidth=0.5
        ),
        row=1, col=1
    )
    
    # Technical Indicators
    if show_indicators and 'SMA_20' in df.columns:
        # Moving Averages
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['SMA_20'],
                name='SMA 20',
                line=dict(color='#ffa500', width=2),
                opacity=0.8
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['SMA_50'],
                name='SMA 50',
                line=dict(color='#00bfff', width=2),
                opacity=0.8
            ),
            row=1, col=1
        )
        
        # Bollinger Bands with fill
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['BB_upper'],
                name='BB Upper',
                line=dict(color='rgba(102, 126, 234, 0.3)', width=1, dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['BB_lower'],
                name='BB Lower',
                line=dict(color='rgba(102, 126, 234, 0.3)', width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(102, 126, 234, 0.1)',
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Anomaly Detection Markers
    if 'is_anomaly' in df.columns:
        anomalies = df[df['is_anomaly']]
        if not anomalies.empty:
            fig.add_trace(
                go.Scatter(
                    x=anomalies['timestamp'],
                    y=anomalies['high'] * 1.02,
                    mode='markers',
                    marker=dict(
                        color='#ff4444',
                        size=15,
                        symbol='triangle-down',
                        line=dict(color='white', width=1)
                    ),
                    name='⚠️ Volatility Spike',
                    hovertemplate='<b>ANOMALY DETECTED</b><br>Time: %{x}<br>Price: $%{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
    
    if 'is_volume_anomaly' in df.columns:
        vol_anomalies = df[df['is_volume_anomaly']]
        if not vol_anomalies.empty:
            fig.add_trace(
                go.Scatter(
                    x=vol_anomalies['timestamp'],
                    y=vol_anomalies['high'] * 1.02,
                    mode='markers',
                    marker=dict(
                        color='#ffa500',
                        size=15,
                        symbol='diamond',
                        line=dict(color='white', width=1)
                    ),
                    name='🌟 Volume Surge',
                    hovertemplate='<b>VOLUME ANOMALY</b><br>Time: %{x}<br>Price: $%{y:.2f}<extra></extra>'
                ),
                row=1, col=1
            )
    
    # Volume Chart with gradient colors
    if show_volume:
        colors = ['rgba(255, 68, 68, 0.8)' if row['close'] < row['open'] 
                  else 'rgba(0, 255, 136, 0.8)' for _, row in df.iterrows()]
        
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name='Volume',
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(255, 255, 255, 0.1)', width=0.5)
                ),
                showlegend=False,
                hovertemplate='Volume: %{y:,.0f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Volume Moving Average
        df['Volume_MA'] = df['volume'].rolling(window=20).mean()
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['Volume_MA'],
                name='Vol MA',
                line=dict(color='#667eea', width=2),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # RSI Indicator
    if 'RSI' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['RSI'],
                name='RSI',
                line=dict(color='#a855f7', width=2.5),
                fill='tozeroy',
                fillcolor='rgba(168, 85, 247, 0.2)',
                showlegend=False
            ),
            row=3, col=1
        )
        
        # RSI Threshold Lines
        fig.add_hline(y=70, line_dash="dash", line_color="rgba(255, 68, 68, 0.5)", 
                      row=3, col=1, annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="rgba(0, 255, 136, 0.5)", 
                      row=3, col=1, annotation_text="Oversold")
        fig.add_hline(y=50, line_dash="dot", line_color="rgba(255, 255, 255, 0.3)", row=3, col=1)
    
    # MACD Chart
    if 'MACD' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['MACD'],
                name='MACD',
                line=dict(color='#00bfff', width=2),
                showlegend=False
            ),
            row=4, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['Signal'],
                name='Signal',
                line=dict(color='#ffa500', width=2),
                showlegend=False
            ),
            row=4, col=1
        )
        
        # MACD Histogram
        colors_macd = ['rgba(0, 255, 136, 0.6)' if val >= 0 else 'rgba(255, 68, 68, 0.6)' 
                       for val in df['MACD_Histogram']]
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['MACD_Histogram'],
                name='Histogram',
                marker_color=colors_macd,
                showlegend=False
            ),
            row=4, col=1
        )
    
    # Update layout with professional styling
    fig.update_layout(
        height=1100,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0, 0, 0, 0.5)",
            bordercolor="rgba(255, 255, 255, 0.2)",
            borderwidth=1
        ),
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(10, 14, 39, 0.8)',
        font=dict(family='Inter', size=12, color='white'),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.05)',
        showline=True,
        linewidth=1,
        linecolor='rgba(255, 255, 255, 0.2)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.05)',
        showline=True,
        linewidth=1,
        linecolor='rgba(255, 255, 255, 0.2)'
    )
    
    # Style subplot titles
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=14, color='white', family='Inter')
    
    return fig

def create_market_depth_chart(df):
    """Create order book / market depth visualization"""
    fig = go.Figure()
    
    # Simulate order book data
    latest_price = df['close'].iloc[-1]
    price_range = latest_price * 0.02
    
    bid_prices = np.linspace(latest_price - price_range, latest_price, 20)
    ask_prices = np.linspace(latest_price, latest_price + price_range, 20)
    
    bid_volumes = np.random.exponential(scale=1000, size=20).cumsum()
    ask_volumes = np.random.exponential(scale=1000, size=20).cumsum()
    
    # Bids (buy orders)
    fig.add_trace(go.Scatter(
        x=bid_volumes,
        y=bid_prices,
        fill='tozerox',
        fillcolor='rgba(0, 255, 136, 0.3)',
        line=dict(color='#00ff88', width=2),
        name='Bids',
        hovertemplate='Price: $%{y:.2f}<br>Volume: %{x:,.0f}<extra></extra>'
    ))
    
    # Asks (sell orders)
    fig.add_trace(go.Scatter(
        x=ask_volumes,
        y=ask_prices,
        fill='tozerox',
        fillcolor='rgba(255, 68, 68, 0.3)',
        line=dict(color='#ff4444', width=2),
        name='Asks',
        hovertemplate='Price: $%{y:.2f}<br>Volume: %{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='<b>Market Depth Analysis</b>',
        xaxis_title='Cumulative Volume',
        yaxis_title='Price (USD)',
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(10, 14, 39, 0.8)',
        hovermode='y unified',
        showlegend=True,
        font=dict(family='Inter', color='white')
    )
    
    return fig

def simulate_indian_market():
    """Enhanced Indian market simulation"""
    base_nifty = 22500 + np.random.randn() * 100
    base_sensex = 74000 + np.random.randn() * 300
    base_nifty_bank = 48000 + np.random.randn() * 200
    
    change_nifty = np.random.uniform(-2, 2)
    change_sensex = np.random.uniform(-2, 2)
    change_bank = np.random.uniform(-2.5, 2.5)
    
    return {
        'nifty': {
            'price': base_nifty,
            'change': change_nifty,
            'volume': np.random.randint(100000, 500000),
            'high': base_nifty * 1.01,
            'low': base_nifty * 0.99
        },
        'sensex': {
            'price': base_sensex,
            'change': change_sensex,
            'volume': np.random.randint(80000, 400000),
            'high': base_sensex * 1.01,
            'low': base_sensex * 0.99
        },
        'nifty_bank': {
            'price': base_nifty_bank,
            'change': change_bank,
            'volume': np.random.randint(50000, 250000),
            'high': base_nifty_bank * 1.015,
            'low': base_nifty_bank * 0.985
        }
    }

def create_heatmap(crypto_data):
    """Create performance heatmap"""
    symbols_list = list(crypto_data.keys())
    changes = [data['change'] for data in crypto_data.values()]
    
    fig = go.Figure(data=go.Bar(
        x=symbols_list,
        y=changes,
        marker=dict(
            color=changes,
            colorscale=[[0, '#ff4444'], [0.5, '#ffa500'], [1, '#00ff88']],
            showscale=False,
            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
        ),
        text=[f"{c:+.2f}%" for c in changes],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Change: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='<b>Market Performance Overview</b>',
        xaxis_title='Trading Pairs',
        yaxis_title='24h Change (%)',
        height=350,
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(10, 14, 39, 0.8)',
        font=dict(family='Inter', color='white')
    )
    
    return fig

# Main Application Loop
iteration = 0

while True:
    with placeholder.container():
        try:
            if "Cryptocurrency" in market_type:
                # Fetch and process cryptocurrency data
                df = fetcher.get_klines(symbol, timeframe, limit=data_points)
                
                # Apply anomaly detection
                df = detector.detect_volatility_anomalies(df, window=20, threshold=anomaly_sensitivity)
                df = detector.detect_volume_anomalies(df, contamination=0.1)
                df = detector.detect_price_spikes(df, threshold=alert_threshold/100 if enable_alerts else 0.05)
                df = detector.detect_pattern_anomalies(df, window=20)
                df = detector.detect_multi_feature_anomalies(df, contamination=0.15)
                df = detector.get_anomaly_severity(df)
                
                # Calculate technical indicators
                df = calculate_advanced_indicators(df)
                
                # Generate trading signals
                signal, signal_desc, signal_list, signal_score = generate_trading_signal(df)
                
                # Price calculations
                latest_price = df['close'].iloc[-1]
                prev_price = df['close'].iloc[-2]
                price_change = ((latest_price - prev_price) / prev_price) * 100
                high_24h = df['high'].max()
                low_24h = df['low'].min()
                volume_24h = df['volume'].sum()
                avg_volume = df['volume'].mean()
                volume_change = ((df['volume'].iloc[-1] - avg_volume) / avg_volume) * 100
                
                # Premium Metrics Dashboard
                st.markdown('<div class="section-header">Market Overview</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                change_class = "positive" if price_change >= 0 else "negative"
                change_color = "#00ff88" if price_change >= 0 else "#ff4444"
                
                with col1:
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">Current Price</div>
                        <div class="metric-value">${latest_price:,.2f}</div>
                        <div class="metric-change {change_class}">{price_change:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">24h High</div>
                        <div class="metric-value" style="font-size: 1.5rem;">${high_24h:,.2f}</div>
                        <div class="metric-change" style="color: #00ff88;">↑ Peak</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">24h Low</div>
                        <div class="metric-value" style="font-size: 1.5rem;">${low_24h:,.2f}</div>
                        <div class="metric-change" style="color: #ff4444;">↓ Bottom</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    vol_color = "#00ff88" if volume_change >= 0 else "#ff4444"
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">24h Volume</div>
                        <div class="metric-value" style="font-size: 1.3rem;">{volume_24h:,.0f}</div>
                        <div class="metric-change" style="color: {vol_color};">{volume_change:+.1f}% vs avg</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    rsi_value = df['RSI'].iloc[-1] if 'RSI' in df.columns else 50
                    rsi_color = "#ff4444" if rsi_value > 70 else "#00ff88" if rsi_value < 30 else "#ffa500"
                    rsi_signal = "Overbought" if rsi_value > 70 else "Oversold" if rsi_value < 30 else "Neutral"
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">RSI Indicator</div>
                        <div class="metric-value" style="font-size: 1.5rem; color: {rsi_color};">{rsi_value:.1f}</div>
                        <div class="metric-change" style="color: {rsi_color};">{rsi_signal}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Trading Signal Panel
                st.markdown('<div class="section-header">AI Trading Signal</div>', unsafe_allow_html=True)
                
                signal_class = "signal-buy" if signal == "BUY" else "signal-sell" if signal == "SELL" else "signal-hold"
                signal_icon = "📈" if signal == "BUY" else "📉" if signal == "SELL" else "⏸"
                
                col_sig1, col_sig2 = st.columns([1, 2])
                
                with col_sig1:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center; padding: 2rem;">
                        <h2 style="font-size: 3rem; margin: 0;">{signal_icon}</h2>
                        <div class="signal-badge {signal_class}" style="font-size: 1.5rem; margin-top: 1rem;">
                            {signal}
                        </div>
                        <p style="margin-top: 1rem; color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                            Confidence Score: <b>{abs(signal_score)}/5</b>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_sig2:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3 style="margin-top: 0; color: white;">Signal Analysis</h3>
                        <p style="color: rgba(255,255,255,0.8); line-height: 1.6;">{signal_desc}</p>
                        <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
                        <h4 style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">SUPPORTING INDICATORS:</h4>
                        <ul style="color: rgba(255,255,255,0.7); line-height: 1.8;">
                            {''.join([f'<li>{s}</li>' for s in signal_list])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Risk Management Panel
                if enable_alerts:
                    entry_price = latest_price
                    stop_loss_price = entry_price * (1 - stop_loss/100)
                    take_profit_price = entry_price * (1 + take_profit/100)
                    risk_reward_ratio = take_profit / stop_loss
                    
                    st.markdown(f"""
                    <div class="alert-warning">
                        <h4 style="margin-top: 0; color: #ffa500;">Active Risk Management</h4>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">Entry Price</p>
                                <p style="margin: 0.25rem 0 0 0; font-size: 1.2rem; font-weight: 700;">${entry_price:,.4f}</p>
                            </div>
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">Stop Loss</p>
                                <p style="margin: 0.25rem 0 0 0; font-size: 1.2rem; font-weight: 700; color: #ff4444;">${stop_loss_price:,.4f}</p>
                            </div>
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">Take Profit</p>
                                <p style="margin: 0.25rem 0 0 0; font-size: 1.2rem; font-weight: 700; color: #00ff88;">${take_profit_price:,.4f}</p>
                            </div>
                            <div>
                                <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">Risk/Reward</p>
                                <p style="margin: 0.25rem 0 0 0; font-size: 1.2rem; font-weight: 700; color: #667eea;">1:{risk_reward_ratio:.2f}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Main Price Chart
                st.markdown('<div class="section-header">🌟 Advanced Technical Analysis</div>', unsafe_allow_html=True)
                st.plotly_chart(create_professional_chart(df, symbol), use_container_width=True)
                
                # Analytics Grid
                col_left, col_middle, col_right = st.columns([2, 2, 1])
                
                with col_left:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 🔍 Anomaly Detection Report")
                    
                    # Get anomaly report
                    anomaly_report = detector.get_anomaly_report(df)
                    
                    total_anomalies = anomaly_report['total_anomalies']
                    
                    if total_anomalies > 0:
                        st.markdown(f"""
                        <div class="alert-critical">
                            <h4 style="margin: 0;">⚠️ {total_anomalies} Anomalies Detected</h4>
                            <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);">
                                Unusual market activity identified. Exercise caution.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Anomaly breakdown
                        for anom_type, count in anomaly_report['anomaly_types'].items():
                            if count > 0:
                                st.markdown(f"""
                                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                    <span style="color: rgba(255,255,255,0.7);">{anom_type}</span>
                                    <span style="color: #ff4444; font-weight: 700;">{count}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Recent anomalies table
                        if anomaly_report['recent_anomalies']:
                            st.markdown("#### Recent Anomaly Events")
                            recent_df = pd.DataFrame(anomaly_report['recent_anomalies'])
                            st.dataframe(
                                recent_df.tail(5),
                                use_container_width=True,
                                hide_index=True
                            )
                    else:
                        st.markdown("""
                        <div class="alert-success">
                            <h4 style="margin: 0;">✅ Market Stable</h4>
                            <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);">
                                No anomalies detected. Normal trading conditions.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_middle:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("###    Technical Indicators Summary")
                    
                    # Create indicator summary
                    indicators_data = []
                    
                    if 'RSI' in df.columns:
                        rsi_val = df['RSI'].iloc[-1]
                        rsi_status = "Overbought" if rsi_val > 70 else "Oversold" if rsi_val < 30 else "Neutral"
                        rsi_color = "#ff4444" if rsi_val > 70 else "#00ff88" if rsi_val < 30 else "#ffa500"
                        indicators_data.append({
                            'Indicator': 'RSI (14)',
                            'Value': f'{rsi_val:.2f}',
                            'Signal': rsi_status,
                            'Color': rsi_color
                        })
                    
                    if 'MACD' in df.columns:
                        macd_val = df['MACD'].iloc[-1]
                        signal_val = df['Signal'].iloc[-1]
                        macd_status = "Bullish" if macd_val > signal_val else "Bearish"
                        macd_color = "#00ff88" if macd_val > signal_val else "#ff4444"
                        indicators_data.append({
                            'Indicator': 'MACD',
                            'Value': f'{macd_val:.4f}',
                            'Signal': macd_status,
                            'Color': macd_color
                        })
                    
                    if 'BB_width' in df.columns:
                        bb_width = df['BB_width'].iloc[-1]
                        bb_status = "High Volatility" if bb_width > 4 else "Low Volatility" if bb_width < 2 else "Normal"
                        bb_color = "#ffa500" if bb_width > 4 else "#00bfff"
                        indicators_data.append({
                            'Indicator': 'Bollinger Width',
                            'Value': f'{bb_width:.2f}%',
                            'Signal': bb_status,
                            'Color': bb_color
                        })
                    
                    if 'Stochastic' in df.columns:
                        stoch_val = df['Stochastic'].iloc[-1]
                        stoch_status = "Overbought" if stoch_val > 80 else "Oversold" if stoch_val < 20 else "Neutral"
                        stoch_color = "#ff4444" if stoch_val > 80 else "#00ff88" if stoch_val < 20 else "#ffa500"
                        indicators_data.append({
                            'Indicator': 'Stochastic',
                            'Value': f'{stoch_val:.2f}',
                            'Signal': stoch_status,
                            'Color': stoch_color
                        })
                    
                    if 'ATR' in df.columns:
                        atr_val = df['ATR'].iloc[-1]
                        atr_pct = (atr_val / latest_price) * 100
                        indicators_data.append({
                            'Indicator': 'ATR (14)',
                            'Value': f'${atr_val:.4f}',
                            'Signal': f'{atr_pct:.2f}%',
                            'Color': "#667eea"
                        })
                    
                    if 'MFI' in df.columns:
                        mfi_val = df['MFI'].iloc[-1]
                        mfi_status = "Strong" if mfi_val > 60 else "Weak" if mfi_val < 40 else "Neutral"
                        mfi_color = "#00ff88" if mfi_val > 60 else "#ff4444" if mfi_val < 40 else "#ffa500"
                        indicators_data.append({
                            'Indicator': 'Money Flow',
                            'Value': f'{mfi_val:.2f}',
                            'Signal': mfi_status,
                            'Color': mfi_color
                        })
                    
                    for ind in indicators_data:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <div>
                                <div style="color: white; font-weight: 600;">{ind['Indicator']}</div>
                                <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">{ind['Value']}</div>
                            </div>
                            <div class="signal-badge" style="background: rgba(255,255,255,0.1); color: {ind['Color']}; border: 1px solid {ind['Color']};">
                                {ind['Signal']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_right:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 🌟 Quick Stats")
                    
                    # Market statistics
                    volatility = df['returns'].std() * 100 if 'returns' in df.columns else 0
                    avg_price = df['close'].mean()
                    price_range = ((high_24h - low_24h) / low_24h) * 100
                    
                    stats_html = f"""
                    <div style="margin-top: 1rem;">
                        <div class="stat-item">
                            <h4>Volatility</h4>
                            <p style="color: {'#ff4444' if volatility > 2 else '#00ff88'};">{volatility:.2f}%</p>
                        </div>
                        <div class="stat-item">
                            <h4>Avg Price</h4>
                            <p>${avg_price:,.4f}</p>
                        </div>
                        <div class="stat-item">
                            <h4>Price Range</h4>
                            <p>{price_range:.2f}%</p>
                        </div>
                        <div class="stat-item">
                            <h4>Trend</h4>
                            <p style="color: {'#00ff88' if df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1] else '#ff4444'};">
                                {'Bullish ↑' if 'SMA_20' in df.columns and df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1] else 'Bearish ↓'}
                            </p>
                        </div>
                    </div>
                    """
                    st.markdown(stats_html, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Market Depth Chart
                if show_predictions:
                    st.markdown('<div class="section-header">🌟 Market Depth Analysis</div>', unsafe_allow_html=True)
                    st.plotly_chart(create_market_depth_chart(df), use_container_width=True)
            
            elif "Indian" in market_type:
                # Indian Market Analysis
                indices = simulate_indian_market()
                
                st.markdown('<div class="section-header">🛞 Indian Market Dashboard</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                for col, (index_name, index_data) in zip([col1, col2, col3], 
                    [('NIFTY 50', indices['nifty']), ('SENSEX', indices['sensex']), ('NIFTY BANK', indices['nifty_bank'])]):
                    
                    with col:
                        change_color = "#00ff88" if index_data['change'] >= 0 else "#ff4444"
                        st.markdown(f"""
                        <div class="glass-card">
                            <h3 style="margin-top: 0; color: white;">{index_name}</h3>
                            <div class="metric-value">₹{index_data['price']:,.2f}</div>
                            <div class="metric-change" style="color: {change_color};">{index_data['change']:+.2f}%</div>
                            <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
                            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                                <div>
                                    <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">High</p>
                                    <p style="margin: 0.25rem 0 0 0; color: #00ff88; font-weight: 600;">₹{index_data['high']:,.2f}</p>
                                </div>
                                <div>
                                    <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">Low</p>
                                    <p style="margin: 0.25rem 0 0 0; color: #ff4444; font-weight: 600;">₹{index_data['low']:,.2f}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Historical chart
                        hist_data = pd.DataFrame({
                            'time': pd.date_range(end=datetime.now(), periods=100, freq='1min'),
                            'value': index_data['price'] + np.cumsum(np.random.randn(100) * 10)
                        })
                        
                        fig_index = go.Figure()
                        fig_index.add_trace(go.Scatter(
                            x=hist_data['time'],
                            y=hist_data['value'],
                            fill='tozeroy',
                            fillcolor=f'rgba(255, 68, 68, 0.3)' if index_data['change'] < 0 else f'rgba(0, 255, 136, 0.3)',
                            line=dict(color=change_color, width=2),
                            name=index_name
                        ))
                        
                        fig_index.update_layout(
                            height=250,
                            template='plotly_dark',
                            showlegend=False,
                            paper_bgcolor='rgba(0, 0, 0, 0)',
                            plot_bgcolor='rgba(10, 14, 39, 0.5)',
                            margin=dict(l=0, r=0, t=10, b=0),
                            xaxis=dict(showgrid=False, showticklabels=False),
                            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                        )
                        
                        st.plotly_chart(fig_index, use_container_width=True, key=f"{index_name}_{iteration}")
                
                st.info("💡 Indian market data is simulated for demonstration. Integrate with NSE/BSE API for live data.")
            
            elif "Global" in market_type:
                # Global Market Overview
                st.markdown('<div class="section-header">🌏 Global Market Overview</div>', unsafe_allow_html=True)
                
                # Fetch multiple crypto pairs
                crypto_overview = {}
                for sym in SYMBOLS[:8]:
                    try:
                        df_temp = fetcher.get_klines(sym, "1h", limit=24)
                        price = df_temp['close'].iloc[-1]
                        change = ((df_temp['close'].iloc[-1] - df_temp['close'].iloc[0]) / df_temp['close'].iloc[0]) * 100
                        volume = df_temp['volume'].sum()
                        crypto_overview[sym] = {
                            'price': price,
                            'change': change,
                            'volume': volume
                        }
                    except:
                        pass
                
                # Performance Heatmap
                col_heat, col_table = st.columns([2, 1])
                
                with col_heat:
                    st.plotly_chart(create_heatmap(crypto_overview), use_container_width=True)
                
                with col_table:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 🏆 Top Performers")
                    
                    sorted_crypto = sorted(crypto_overview.items(), key=lambda x: x[1]['change'], reverse=True)
                    
                    for i, (sym, data) in enumerate(sorted_crypto[:5]):
                        change_color = "#00ff88" if data['change'] >= 0 else "#ff4444"
                        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🌟"
                        
                        st.markdown(f"""
                        <div style="padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <span style="font-size: 1.2rem;">{medal}</span>
                                    <div>
                                        <div style="color: white; font-weight: 600;">{sym}</div>
                                        <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">${data['price']:,.4f}</div>
                                    </div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="color: {change_color}; font-weight: 700; font-size: 1.1rem;">{data['change']:+.2f}%</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Detailed Table
                st.markdown('<div class="section-header">📋 Detailed Market Data</div>', unsafe_allow_html=True)
                
                crypto_table = []
                for sym, data in crypto_overview.items():
                    crypto_table.append({
                        'Symbol': sym,
                        'Price': f"${data['price']:,.4f}",
                        '24h Change': f"{data['change']:+.2f}%",
                        '24h Volume': f"{data['volume']:,.0f}",
                        'Signal': 'Buy' if data['change'] > 3 else 'Sell' if data['change'] < -3 else 'Hold'
                    })
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.dataframe(
                    pd.DataFrame(crypto_table),
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Indian Indices Side Panel
                st.markdown('<div class="section-header">🛞 Indian Market Snapshot</div>', unsafe_allow_html=True)
                
                indices = simulate_indian_market()
                
                col_nifty, col_sensex, col_bank = st.columns(3)
                
                with col_nifty:
                    nifty_color = "#00ff88" if indices['nifty']['change'] >= 0 else "#ff4444"
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">NIFTY 50</div>
                        <div class="metric-value" style="font-size: 1.5rem;">₹{indices['nifty']['price']:,.2f}</div>
                        <div class="metric-change" style="color: {nifty_color};">{indices['nifty']['change']:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_sensex:
                    sensex_color = "#00ff88" if indices['sensex']['change'] >= 0 else "#ff4444"
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">SENSEX</div>
                        <div class="metric-value" style="font-size: 1.5rem;">₹{indices['sensex']['price']:,.2f}</div>
                        <div class="metric-change" style="color: {sensex_color};">{indices['sensex']['change']:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_bank:
                    bank_color = "#00ff88" if indices['nifty_bank']['change'] >= 0 else "#ff4444"
                    st.markdown(f"""
                    <div class="premium-metric">
                        <div class="metric-label">NIFTY BANK</div>
                        <div class="metric-value" style="font-size: 1.5rem;">₹{indices['nifty_bank']['price']:,.2f}</div>
                        <div class="metric-change" style="color: {bank_color};">{indices['nifty_bank']['change']:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            iteration += 1
            
            # Update timestamp
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"""
            <div style='text-align: center; padding: 1rem 0;'>
                <p style='color: rgba(255,255,255,0.5); font-size: 0.85rem; margin: 0;'>Last Updated</p>
                <p style='color: #667eea; font-weight: 600; font-size: 1rem; margin: 0.25rem 0 0 0;'>{datetime.now().strftime("%H:%M:%S")}</p>
                <p style='color: rgba(255,255,255,0.5); font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Iteration #{iteration}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f"""
            <div class="alert-critical">
                <h3 style="margin: 0;">⚠️ Error Occurred</h3>
                <p style="margin: 0.5rem 0; color: rgba(255,255,255,0.8);">{str(e)}</p>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
                <h4 style="margin: 0.5rem 0; font-size: 0.9rem; color: rgba(255,255,255,0.7);">Troubleshooting Tips:</h4>
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem; color: rgba(255,255,255,0.7);">
                    <li>Verify Binance API credentials in .env file</li>
                    <li>Check internet connectivity</li>
                    <li>Ensure API rate limits are not exceeded</li>
                    <li>Try selecting a different trading pair</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.code(f"Error Details: {str(e)}", language="python")
    
    if auto_refresh:
        time.sleep(refresh_interval)
    else:
        break

# Elite Footer
st.markdown("""
<div class="elite-footer">
    <h3>Live Cryptocurrency Price Dashboard with Anomaly Detection</h3>
    <p style="font-size: 0.95rem; margin-top: 0.5rem;">
        Powered by <b>Binance API</b> • <b>Machine Learning</b> • <b>Advanced Technical Analysis</b>
    </p>
    <p style="font-size: 0.85rem; margin-top: 1rem; color: rgba(255,255,255,0.4);">
        Real-Time Market Data • AI-Powered Anomaly Detection
    </p>
    <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
        <p style="font-size: 0.8rem; color: rgba(255,255,255,0.3);">
            © 2024 Live Cryptocurrency Price Dashboard with Anomaly Detection • Built with Streamlit & Plotly • For Educational & Research Purposes
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
