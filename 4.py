from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        # We can start now
        self.start_trade(orderId)

    def start_trade(self, orderId):
        # Define the contracts
        contracts = [
            self.create_contract("AAPL", "OPT", "SMART", "USD", '20230519', 200, "C"),
            self.create_contract("AAPL", "OPT", "SMART", "USD", '20230519', 210, "C"),
            # Add more contracts as needed...
        ]

        for contract in contracts:
            # Define the initial buy order
            buy_order = Order()
            buy_order.action = "BUY"
            buy_order.totalQuantity = 100
            buy_order.orderType = "LMT"
            buy_order.lmtPrice = 200.00
            buy_order.eTradeOnly = False
            buy_order.firmQuoteOnly = False
            self.placeOrder(orderId, contract, buy_order)

            # Define your target profit and stop loss percentages
            profit_target_percentage = 0.50
            stop_loss_percentage = 0.25

            # Calculate the take profit and stop loss prices
            take_profit_price = buy_order.lmtPrice * (1 + profit_target_percentage)
            stop_loss_price = buy_order.lmtPrice * (1 - stop_loss_percentage)

            # Create the take profit order
            take_profit_order = Order()
            take_profit_order.action = "SELL"
            take_profit_order.totalQuantity = buy_order.totalQuantity
            take_profit_order.orderType = "LMT"
            take_profit_order.lmtPrice = take_profit_price
            self.placeOrder(orderId + 1, contract, take_profit_order)

            # Create the stop loss order
            stop_loss_order = Order()
            stop_loss_order.action = "SELL"
            stop_loss_order.totalQuantity = buy_order.totalQuantity
            stop_loss_order.orderType = "STP"
            stop_loss_order.auxPrice = stop_loss_price
            self.placeOrder(orderId + 2, contract, stop_loss_order)

            # Increase the order ID for the next contract
            orderId += 3

    def create_contract(self, symbol, sec_type, exchange, currency, expiry_date, strike, option_type):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange
        contract.currency = currency
        contract.lastTradeDateOrContractMonth = expiry_date
        contract.strike = strike
        contract.right = option_type
        return contract

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, clientId=0)
    app.run()

if __name__ == "__main__":
    main()