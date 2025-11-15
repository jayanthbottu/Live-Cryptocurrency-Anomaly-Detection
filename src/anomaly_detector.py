import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats
from config.settings import ANOMALY_THRESHOLD

class AnomalyDetector:
    """Advanced anomaly detection system with multiple algorithms"""
    
    @staticmethod
    def detect_volatility_anomalies(df: pd.DataFrame, window: int = 20, threshold: float = ANOMALY_THRESHOLD):
        """Detect price volatility anomalies using rolling Z-score"""
        df = df.copy()
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(window=window).std()
        
        # Calculate Z-score
        mean_vol = df['volatility'].mean()
        std_vol = df['volatility'].std()
        df['z_score'] = (df['volatility'] - mean_vol) / std_vol
        df['is_anomaly'] = np.abs(df['z_score']) > threshold
        
        return df
    
    @staticmethod
    def detect_volume_anomalies(df: pd.DataFrame, contamination: float = 0.1):
        """Detect volume anomalies using Isolation Forest"""
        df = df.copy()
        
        # Prepare volume data
        volume_data = df[['volume']].values.reshape(-1, 1)
        
        # Apply Isolation Forest
        model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100,
            max_samples='auto'
        )
        
        df['volume_anomaly'] = model.fit_predict(volume_data)
        df['is_volume_anomaly'] = df['volume_anomaly'] == -1
        df['volume_anomaly_score'] = model.score_samples(volume_data)
        
        return df
    
    @staticmethod
    def detect_price_spikes(df: pd.DataFrame, threshold: float = 0.05):
        """Detect sudden price spikes or drops"""
        df = df.copy()
        df['price_change'] = df['close'].pct_change()
        df['is_spike'] = np.abs(df['price_change']) > threshold
        return df
    
    @staticmethod
    def detect_pattern_anomalies(df: pd.DataFrame, window: int = 20):
        """Detect anomalies in price patterns using statistical methods"""
        df = df.copy()
        
        # Calculate moving statistics
        df['rolling_mean'] = df['close'].rolling(window=window).mean()
        df['rolling_std'] = df['close'].rolling(window=window).std()
        
        # Upper and lower bounds (Bollinger Bands concept)
        df['upper_bound'] = df['rolling_mean'] + (2 * df['rolling_std'])
        df['lower_bound'] = df['rolling_mean'] - (2 * df['rolling_std'])
        
        # Detect breakouts
        df['is_pattern_anomaly'] = (
            (df['close'] > df['upper_bound']) | 
            (df['close'] < df['lower_bound'])
        )
        
        return df
    
    @staticmethod
    def detect_multi_feature_anomalies(df: pd.DataFrame, contamination: float = 0.15):
        """Advanced multi-feature anomaly detection"""
        df = df.copy()
        
        # Create features
        df['returns'] = df['close'].pct_change()
        df['log_volume'] = np.log1p(df['volume'])
        df['price_momentum'] = df['close'].diff()
        df['volume_momentum'] = df['volume'].diff()
        
        # Select features for anomaly detection
        features = ['returns', 'log_volume', 'price_momentum', 'volume_momentum']
        feature_data = df[features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        feature_data_scaled = scaler.fit_transform(feature_data)
        
        # Apply Isolation Forest
        model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=200,
            max_samples='auto',
            bootstrap=True
        )
        
        df['multi_anomaly'] = model.fit_predict(feature_data_scaled)
        df['is_multi_anomaly'] = df['multi_anomaly'] == -1
        df['anomaly_score'] = model.score_samples(feature_data_scaled)
        
        return df
    
    @staticmethod
    def get_anomaly_severity(df: pd.DataFrame):
        """Calculate overall anomaly severity score"""
        df = df.copy()
        
        anomaly_cols = [col for col in df.columns if 'is_' in col and 'anomaly' in col]
        if anomaly_cols:
            df['anomaly_count'] = df[anomaly_cols].sum(axis=1)
            df['severity'] = pd.cut(
                df['anomaly_count'],
                bins=[-np.inf, 0, 1, 2, np.inf],
                labels=['Normal', 'Low', 'Medium', 'High']
            )
        else:
            df['severity'] = 'Normal'
        
        return df
    
    @staticmethod
    def get_anomaly_report(df: pd.DataFrame):
        """Generate comprehensive anomaly report"""
        anomaly_cols = [col for col in df.columns if 'is_' in col and 'anomaly' in col]
        
        report = {
            'total_anomalies': 0,
            'anomaly_types': {},
            'recent_anomalies': [],
            'severity_distribution': {}
        }
        
        for col in anomaly_cols:
            count = df[col].sum()
            report['total_anomalies'] += count
            report['anomaly_types'][col.replace('is_', '').replace('_', ' ').title()] = int(count)
        
        # Get recent anomalies (last 10)
        recent_mask = df[anomaly_cols].any(axis=1)
        recent_df = df[recent_mask].tail(10)
        
        if not recent_df.empty:
            report['recent_anomalies'] = recent_df[['timestamp', 'close', 'volume']].to_dict('records')
        
        # Severity distribution
        if 'severity' in df.columns:
            severity_counts = df['severity'].value_counts().to_dict()
            report['severity_distribution'] = {str(k): int(v) for k, v in severity_counts.items()}
        
        return report