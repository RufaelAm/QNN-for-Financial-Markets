# Configuration Template for QNN Financial Markets
# Copy this file to config.py and fill in your actual values
# DO NOT commit config.py to version control!

# QuantConnect API Configuration
QUANTCONNECT_API_KEY = "YOUR_API_KEY_HERE"
QUANTCONNECT_API_SECRET = "YOUR_API_SECRET_HERE"
QUANTCONNECT_USER_ID = "YOUR_USER_ID_HERE"

# Trading Parameters (these can be adjusted based on your strategy)
INITIAL_CASH = 100000
START_DATE = (2024, 1, 1)
END_DATE = (2025, 1, 1)
TARGET_SYMBOL = "SPY"

# Quantum Circuit Parameters
NUM_QUBITS = 2
TRAINING_ITERATIONS = 200
LEARNING_RATE = 0.05
QUANTUM_SHOTS = 1024

# Risk Management
MAX_POSITION_SIZE = 1.0  # Maximum portfolio allocation to single position
STOP_LOSS_PERCENTAGE = 0.05  # 5% stop loss
TAKE_PROFIT_PERCENTAGE = 0.10  # 10% take profit

# Model Parameters (load from trained model file instead of hardcoding)
TRAINED_PARAMETERS_FILE = "trained_parameters.npy"

# Logging and Monitoring
LOG_LEVEL = "INFO"
ENABLE_DETAILED_LOGGING = True
SAVE_TRADING_LOGS = True
SAVE_BACKTEST_RESULTS = True

# Security Settings
ENCRYPT_SENSITIVE_DATA = True
USE_SECURE_CONNECTIONS = True
VALIDATE_SSL_CERTIFICATES = True