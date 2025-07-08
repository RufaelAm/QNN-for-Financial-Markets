# QNN for Financial Markets

Here is a position trading QNN that generates stable returns by leveraging Quantum neural networks to predict stock prices for the use of low volatility markets. This strategy enables the capture of higher complexity trends in the financial market by qubit encoding of market data allowing innovative detail in input feeding of stock prices resulting in higher precision for price derivative analysis, enabling higher accuracy trades. Ensure this strategy is run in QuantConnect, keeping up to date with Qiskit support to ensure reproducible results.

## Security and Privacy Considerations

This repository has been configured with security best practices to protect sensitive trading and API information:

### 🔒 Sensitive Data Protection

- **API Keys**: Never commit API keys, secrets, or credentials to version control
- **Trading Parameters**: Trained model parameters are loaded from secure files, not hardcoded
- **Configuration**: Use environment variables or secure config files for sensitive settings

### 📋 Configuration Setup

1. **Environment Variables (Recommended for Production)**:
   ```bash
   cp .env.template .env
   # Edit .env with your actual values
   ```

2. **Configuration File (Alternative)**:
   ```bash
   cp config_template.py config.py
   # Edit config.py with your actual values
   ```

3. **Required Settings**:
   - `QUANTCONNECT_API_KEY`: Your QuantConnect API key
   - `QUANTCONNECT_API_SECRET`: Your QuantConnect API secret
   - `QUANTCONNECT_USER_ID`: Your QuantConnect user ID

### 🛡️ Security Features

- **Comprehensive .gitignore**: Prevents accidental commit of sensitive files
- **Secure Configuration Loader**: Handles environment variables and config files safely
- **Risk Management**: Built-in stop-loss and take-profit mechanisms
- **Parameter Validation**: Ensures required configuration is present before execution

### 📁 Files to Keep Private

The following files should NEVER be committed to version control:
- `.env` - Environment variables with sensitive data
- `config.py` - Configuration file with API keys
- `trained_parameters.npy` - Trained model parameters
- `*.log` - Trading logs that may contain sensitive information
- `trading_logs/` - Directory with detailed trading history
- Any files containing API keys, credentials, or personal trading data

### 🚨 Security Checklist

Before deploying or sharing this repository:

- [ ] Verify no API keys or secrets are hardcoded
- [ ] Ensure `.env` and `config.py` are in `.gitignore`
- [ ] Check that `trained_parameters.npy` is not committed
- [ ] Validate all sensitive files are excluded from version control
- [ ] Review commit history for any accidentally committed secrets

### 📊 Risk Management

The trading algorithm includes several risk management features:

- **Position Sizing**: Configurable maximum position size
- **Stop Loss**: Automatic stop-loss execution when losses exceed threshold
- **Take Profit**: Automatic profit-taking when gains exceed threshold
- **Parameter Validation**: Ensures configuration is valid before trading

### 🔧 Usage

1. Set up your configuration (see Configuration Setup above)
2. Train your quantum neural network using `QNN_Training.ipynb`
3. Save trained parameters to `trained_parameters.npy`
4. Deploy the algorithm in QuantConnect with your secure configuration

### ⚠️ Disclaimer

This software is for educational and research purposes. Trading involves significant financial risk. Always validate strategies thoroughly before deploying with real money. The authors are not responsible for any financial losses incurred through the use of this software.
