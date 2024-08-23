from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

class TestApp(EWrapper, EClient):
    def __init__(self, profit_target=0.50, stop_loss=0.25):
        EClient.__init__(self, self)
        self.orderId = 0
        self.profit_target = profit_target
        self.stop_loss = stop_loss

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.orderId = orderId
        self.start_trade()

    def start_trade(self):
        contracts = [
            self.create_contract("AAPL", "OPT", "SMART", "USD", '20230519', 200, "C"),
            # Add more contracts as needed...
        ]

        for contract in contracts:
            self.place_initial_order(contract)

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

    def place_initial_order(self, contract):
        buy_order = Order()
        buy_order.action = "BUY"
        buy_order.totalQuantity = 100
        buy_order.orderType = "MKT" 
        buy_order.transmit = False
        parentOrderId = self.orderId
        self.placeOrder(self.orderId, contract, buy_order)
        self.orderId += 1

        self.place_take_profit_order(contract, parentOrderId)
        self.place_stop_loss_order(contract, parentOrderId)

    def place_take_profit_order(self, contract, parentOrderId):
        take_profit_order = Order()
        take_profit_order.action = "SELL"
        take_profit_order.totalQuantity = 100
        take_profit_order.orderType = "TRAIL"
        take_profit_order.auxPrice = self.profit_target
        take_profit_order.parentId = parentOrderId
        self.placeOrder(self.orderId, contract, take_profit_order)
        self.orderId += 1

    def place_stop_loss_order(self, contract, parentOrderId):
        stop_loss_order = Order()
        stop_loss_order.action = "SELL"
        stop_loss_order.totalQuantity = 100
        stop_loss_order.orderType = "TRAIL"
        stop_loss_order.auxPrice = self.stop_loss
        stop_loss_order.parentId = parentOrderId
        self.placeOrder(self.orderId, contract, stop_loss_order)
        self.orderId += 1


def main():
    app = TestApp(profit_target=0.50, stop_loss=0.25)
    app.connect("127.0.0.1", 7496, clientId=0)
    app.run()

if __name__ == "__main__":
    main()