"""
Secure configuration loader for QNN Financial Markets
Handles environment variables and configuration files securely
"""
import os
import numpy as np
from typing import Tuple, Optional
import warnings

class SecureConfig:
    """Secure configuration handler for sensitive trading parameters"""
    
    def __init__(self):
        self.config = {}
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from environment variables or config file"""
        # Try to load from environment variables first (most secure)
        self.config = {
            'quantconnect_api_key': os.getenv('QUANTCONNECT_API_KEY'),
            'quantconnect_api_secret': os.getenv('QUANTCONNECT_API_SECRET'),
            'quantconnect_user_id': os.getenv('QUANTCONNECT_USER_ID'),
            'initial_cash': int(os.getenv('INITIAL_CASH', '100000')),
            'start_date': self._parse_date_env('START_DATE', (2024, 1, 1)),
            'end_date': self._parse_date_env('END_DATE', (2025, 1, 1)),
            'target_symbol': os.getenv('TARGET_SYMBOL', 'SPY'),
            'num_qubits': int(os.getenv('NUM_QUBITS', '2')),
            'training_iterations': int(os.getenv('TRAINING_ITERATIONS', '200')),
            'learning_rate': float(os.getenv('LEARNING_RATE', '0.05')),
            'quantum_shots': int(os.getenv('QUANTUM_SHOTS', '1024')),
            'max_position_size': float(os.getenv('MAX_POSITION_SIZE', '1.0')),
            'stop_loss_percentage': float(os.getenv('STOP_LOSS_PERCENTAGE', '0.05')),
            'take_profit_percentage': float(os.getenv('TAKE_PROFIT_PERCENTAGE', '0.10')),
            'trained_parameters_file': os.getenv('TRAINED_PARAMETERS_FILE', 'trained_parameters.npy'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'enable_detailed_logging': os.getenv('ENABLE_DETAILED_LOGGING', 'True').lower() == 'true',
            'save_trading_logs': os.getenv('SAVE_TRADING_LOGS', 'True').lower() == 'true',
            'save_backtest_results': os.getenv('SAVE_BACKTEST_RESULTS', 'True').lower() == 'true',
        }
        
        # If environment variables are not set, try to load from config.py
        if not self.config['quantconnect_api_key']:
            try:
                import config
                self._load_from_config_file(config)
            except ImportError:
                warnings.warn(
                    "No configuration found. Please either:\n"
                    "1. Set environment variables (recommended for production)\n"
                    "2. Copy config_template.py to config.py and fill in values"
                )
    
    def _parse_date_env(self, env_var: str, default: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Parse date from environment variable"""
        date_str = os.getenv(env_var)
        if date_str:
            try:
                year, month, day = map(int, date_str.split('-'))
                return (year, month, day)
            except ValueError:
                warnings.warn(f"Invalid date format for {env_var}, using default")
        return default
    
    def _load_from_config_file(self, config_module):
        """Load configuration from config.py file"""
        config_vars = {
            'quantconnect_api_key': 'QUANTCONNECT_API_KEY',
            'quantconnect_api_secret': 'QUANTCONNECT_API_SECRET',
            'quantconnect_user_id': 'QUANTCONNECT_USER_ID',
            'initial_cash': 'INITIAL_CASH',
            'start_date': 'START_DATE',
            'end_date': 'END_DATE',
            'target_symbol': 'TARGET_SYMBOL',
            'num_qubits': 'NUM_QUBITS',
            'training_iterations': 'TRAINING_ITERATIONS',
            'learning_rate': 'LEARNING_RATE',
            'quantum_shots': 'QUANTUM_SHOTS',
            'max_position_size': 'MAX_POSITION_SIZE',
            'stop_loss_percentage': 'STOP_LOSS_PERCENTAGE',
            'take_profit_percentage': 'TAKE_PROFIT_PERCENTAGE',
            'trained_parameters_file': 'TRAINED_PARAMETERS_FILE',
            'log_level': 'LOG_LEVEL',
            'enable_detailed_logging': 'ENABLE_DETAILED_LOGGING',
            'save_trading_logs': 'SAVE_TRADING_LOGS',
            'save_backtest_results': 'SAVE_BACKTEST_RESULTS',
        }
        
        for config_key, module_var in config_vars.items():
            if hasattr(config_module, module_var) and not self.config[config_key]:
                self.config[config_key] = getattr(config_module, module_var)
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def load_trained_parameters(self) -> Optional[np.ndarray]:
        """Securely load trained parameters from file"""
        params_file = self.get('trained_parameters_file')
        if params_file and os.path.exists(params_file):
            try:
                return np.load(params_file)
            except Exception as e:
                warnings.warn(f"Failed to load trained parameters: {e}")
        return None
    
    def validate_configuration(self) -> bool:
        """Validate that required configuration is present"""
        required_keys = ['quantconnect_api_key', 'quantconnect_api_secret']
        missing_keys = [key for key in required_keys if not self.config.get(key)]
        
        if missing_keys:
            warnings.warn(f"Missing required configuration: {missing_keys}")
            return False
        return True

# Global configuration instance
config = SecureConfig()