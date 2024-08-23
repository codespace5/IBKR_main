from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        # we can start now
        self.start_trade(orderId)

    def start_trade(self, orderId):
        # Define a contract
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Define initial buy order
        buy_order = LimitOrder("BUY", 100, 200.00)
        self.placeOrder(orderId, contract, buy_order)

        # Define your target profit and stop loss percentages
        profit_target_percentage = 0.50
        stop_loss_percentage = 0.25

        # Calculate the take profit and stop loss prices
        take_profit_price = buy_order.lmtPrice * (1 + profit_target_percentage)
        stop_loss_price = buy_order.lmtPrice * (1 - stop_loss_percentage)

        # Create the take profit order
        take_profit_order = LimitOrder('SELL', buy_order.totalQuantity, take_profit_price)
        self.placeOrder(orderId + 1, contract, take_profit_order)

        # Create the stop loss order
        stop_loss_order = StopOrder('SELL', buy_order.totalQuantity, stop_loss_price)
        self.placeOrder(orderId + 2, contract, stop_loss_order)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7496, clientId=0)

    app.run()


if __name__ == "__main__":
    main()