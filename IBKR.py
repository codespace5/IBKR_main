# Import the necessary modules from ibapi
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import Execution
from ibapi.order import Order
from ibapi.wrapper import EWrapper
import threading



# Define a class that inherits from EClient and EWrapper
class TestApp(EWrapper, EClient):



    # Initialize the class
    def init(self):
        EClient.__init__(self, self)
        self.nextOrderId = None # To store the next valid order id
        self.nextOrderIdEvent = threading.Event() # To create an event object



    # Define a method to get the next valid order id
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        print("Next valid order id:", orderId)
        self.nextOrderIdEvent.set() # To set the event



    # Define a method to request account updates
    def reqAccountUpdates(self, subscribe: bool, acctCode: str):
        super().reqAccountUpdates(subscribe, acctCode)
        print("Requesting account updates for", acctCode)



# Define a method to place orders
    def placeOrder(self, orderId: int, contract: Contract, order: Order):
        super().placeOrder(orderId, contract, order)
        print("Placing order for", contract.symbol)



# Define a method to handle order status events
    def orderStatus(self, orderId: int, status: str, filled: float,
        remaining: float, avgFillPrice: float, permId: int,
        parentId: int, lastFillPrice: float, clientId: int,
        whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
        avgFillPrice, permId, parentId,
        lastFillPrice, clientId, whyHeld,
        mktCapPrice)
        # Call the checkOrderStatus function with the order id and status
        self.checkOrderStatus(orderId, status)



    # Define a method to handle execution details events
    def execDetails(self, reqId: int, contract: Contract,
    execution: Execution):
        super().execDetails(reqId, contract, execution)
        print("Execution details:", reqId, contract.symbol,
        execution.execId, execution.orderId,
        execution.shares, execution.lastLiquidity)



# Define a function that takes an order id and a status as parameters
    def checkOrderStatus(self, orderId: int, status: str):
        # Check if the status is "Submitted" or "Filled"
        if status in ["Submitted", "Filled"]:
        # Print "Success", the order id and the status
            print("Success:", orderId, status)
        else:
        # Print "Failure" and the order id
            print("Failure:", orderId)



# Create an instance of the TestApp class
app = TestApp()



# Connect to the IB Gateway or TWS
app.connect("127.0.0.1", 7497, clientId=1) # Change the port number as needed



# Start a thread to process messages from IB
app.run()



# Request account updates for your paper trading account
# app.reqAccountUpdates(True, "DU3934117") # Change the account code as needed



# Create a list of options contracts you want to trade
contracts = []



# PARAMETERS
contract1 = Contract()
contract1.symbol = "AAPL"
contract1.secType = "OPT" #SET FOR OPTIONS
contract1.exchange = "SMART" #IBKR Smart Routing
contract1.currency = "USD"
contract1.lastTradeDateOrContractMonth = "20230623" #Expiration
contract1.strike = 185
contract1.right = "C"
contract1.multiplier = "100"



# Add the contract to the list
contracts.append(contract1)



# You can add more contracts to the list as needed



# Create a list of market orders for each contract
orders = []



# For example, you want to buy 1 contract of AAPL 150 call
order1 = Order()
order1.action = "BUY"
order1.orderType = "MKT"
order1.totalQuantity = 1
order1.outsideRth = False # Set this to False to execute only during regular trading hours



# Add the order to the list
orders.append(order1)



# You can add more orders to the list as needed



# Wait for the next valid order id event
app.nextOrderIdEvent.wait()



# Loop through the contracts and orders lists and place them using the next valid order id
for i in range(len(contracts)):
    app.placeOrder(app.nextOrderId, contracts[i], orders[i])
    app.nextOrderId += 1 # Increment the next valid order id by 1



# Disconnect from the IB Gateway or TWS when done
app.disconnect()