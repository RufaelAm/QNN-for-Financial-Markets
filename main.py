# region imports
from AlgorithmImports import *
# endregion
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Data.Market import TradeBar
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit_aer import Aer
import numpy as np
from secure_config import config

class QuantumNeuralNetworkTrading(QCAlgorithm):
    def Initialize(self):
        # Use secure configuration instead of hardcoded values
        start_date = config.get('start_date', (2024, 1, 1))
        end_date = config.get('end_date', (2025, 1, 1))
        initial_cash = config.get('initial_cash', 100000)
        target_symbol = config.get('target_symbol', 'SPY')
        
        self.SetStartDate(*start_date)
        self.SetEndDate(*end_date)
        self.SetCash(initial_cash)
        self.symbol = self.AddEquity(target_symbol, Resolution.Daily).Symbol
        
        # Load trained parameters securely from file instead of hardcoding
        self.trained_params = config.load_trained_parameters()
        if self.trained_params is None:
            # Fallback to default parameters if file not found
            self.Debug("Warning: Using default parameters. Please ensure trained_parameters.npy is available.")
            self.trained_params = np.array([3.3926, 5.3705, 2.8713, 4.3222, 5.1231, 3.8132, 3.4503, 1.7366])
        
        self.num_qubits = config.get('num_qubits', 2)
        
        # Risk management parameters
        self.max_position_size = config.get('max_position_size', 1.0)
        self.stop_loss_pct = config.get('stop_loss_percentage', 0.05)
        self.take_profit_pct = config.get('take_profit_percentage', 0.10)
        
        # Initialize quantum circuit
        self.circuit, self.params = self._create_circuit()
        self.simulator = Aer.get_backend('aer_simulator')
        self.transpiled_circuit = transpile(self.circuit, self.simulator)
        
        # Schedule trading logic
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), 
                        self.TimeRules.AfterMarketOpen(self.symbol, 30),
                        self.Trade)

    def _create_circuit(self):
        """Recreate the QNN circuit architecture"""
        circuit = QuantumCircuit(self.num_qubits)
        params = [Parameter(f'θ{i}') for i in range(4 * self.num_qubits)]
        
        # Input encoding layer
        for i in range(self.num_qubits):
            circuit.rx(params[i], i)
            circuit.ry(params[i + self.num_qubits], i)
        
        # Entanglement layer
        for i in range(self.num_qubits-1):
            circuit.cx(i, (i+1) % self.num_qubits)
        
        # Additional layers
        for i in range(self.num_qubits):
            circuit.rx(params[i + 2 * self.num_qubits], i)
            circuit.ry(params[i + 3 * self.num_qubits], i)
        
        circuit.measure_all()
        return circuit, params

    def Trade(self):
        """Execute trades based on QNN predictions with risk management"""
        # Get historical data
        history = self.History(self.symbol, 5, Resolution.Daily)
        if history.empty:
            return
        
        # Feature engineering (example: use closing prices as inputs)
        latest_prices = history["close"].values[-2:]  # Last 2 days' closing prices
        normalized_input = (latest_prices - np.min(latest_prices)) / (np.max(latest_prices) - np.min(latest_prices)) * np.pi
        
        # Run QNN inference
        prediction = self.predict(normalized_input)
        
        # Get current holdings
        current_holdings = self.Portfolio[self.symbol].Quantity
        current_price = self.Securities[self.symbol].Price
        
        # Risk management: Check for stop loss or take profit
        if current_holdings != 0:
            entry_price = self.Portfolio[self.symbol].AveragePrice
            unrealized_pnl_pct = (current_price - entry_price) / entry_price
            
            # Stop loss check
            if unrealized_pnl_pct < -self.stop_loss_pct:
                self.Liquidate(self.symbol, "Stop Loss Triggered")
                return
            
            # Take profit check
            if unrealized_pnl_pct > self.take_profit_pct:
                self.Liquidate(self.symbol, "Take Profit Triggered")
                return
        
        # Execute trades based on prediction with position sizing
        if prediction == 1:
            self.SetHoldings(self.symbol, self.max_position_size)  # Buy with max position size
        else:
            self.Liquidate(self.symbol)  # Sell

    def predict(self, x):
        """Make predictions using the trained QNN"""
        param_values = np.concatenate([x, self.trained_params[self.num_qubits:]])
        param_dict = {p: param_values[i] for i, p in enumerate(self.params)}
        
        # Use quantum shots from configuration
        shots = config.get('quantum_shots', 1000)
        bound_qc = self.transpiled_circuit.assign_parameters(param_dict)
        result = self.simulator.run(bound_qc, shots=shots).result()
        counts = result.get_counts()
        
        prob_class0 = counts.get('00', 0) / shots
        prob_class1 = counts.get('11', 0) / shots
        return 0 if prob_class0 > prob_class1 else 1
        
