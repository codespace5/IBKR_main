option_contract = Contract()
option_contract.symbol = "AAPL"
option_contract.secType = "OPT"
option_contract.exchange = "SMART"
option_contract.currency = "USD"
option_contract.lastTradeDateOrContractMonth = '20230519'  # Format is YYYYMMDD
option_contract.strike = 200
option_contract.right = "C"


def start_trade(self, orderId):
    contracts = [
        self.create_contract("AAPL", "OPT", "SMART", "USD", '20230519', 200, "C"),
        self.create_contract("AAPL", "OPT", "SMART", "USD", '20230519', 210, "C"),
        # Add more contracts as needed...
    ]

    for contract in contracts:
        # Place the initial buy order
        buy_order = self.create_order("BUY", 100, "LMT", 200.00)
        self.placeOrder(orderId, contract, buy_order)

        # Calculate take profit and stop loss prices
        take_profit_price = buy_order.lmtPrice * (1 + profit_target_percentage)
        stop_loss_price = buy_order.lmtPrice * (1 - stop_loss_percentage)

        # Place the take profit order
        take_profit_order = self.create_order("SELL", buy_order.totalQuantity, "LMT", take_profit_price)
        self.placeOrder(orderId + 1, contract, take_profit_order)

        # Place the stop loss order
        stop_loss_order = self.create_order("SELL", buy_order.totalQuantity, "STP", stop_loss_price)
        self.placeOrder(orderId + 2, contract, stop_loss_order)

        # Increase the order ID for the next contract
        orderId += 3