from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time

# Trading configuration
SYMBOL = 'OSS'
DIRECTION = 'SELL'  # 'BUY' or 'SELL'
QUANTITY = 1000
ENTRY_PRICE = 2.42
STOP_LOSS = 2.59
TAKE_PROFIT = 1.88

# Connection configuration
PAPER_PORT = 7497
LIVE_PORT = 7496
IS_PAPER_TRADING = True  # Set to False for live trading

class TradeApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.order_placed = False
        self.order_event = threading.Event()

    def error(self, reqId, errorCode, errorString):
        if errorCode not in (2104, 2106, 2158):
            print(f"❌ Error {errorCode}: {errorString}")

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId
        print(f"Next valid order ID: {orderId}")

    def openOrder(self, orderId, contract, order, orderState):
        # Fires as soon as TWS knows about your order leg
        print(f"📂 openOrder: id={orderId}, status={orderState.status}")
        if orderState.status in ("PreSubmitted", "PendingSubmit"):
            self.order_placed = True
            self.order_event.set()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"🔖 Order {orderId} status: {status}")
        # Treat any PreSubmitted / Submitted / Filled as confirmation
        if status in ("PreSubmitted", "Submitted", "Filled"):
            if status == "Filled":
                print(f"✨ Order {orderId} filled at ${avgFillPrice}")
            self.order_placed = True
            self.order_event.set()

def run_loop():
    app.run()

def get_contract(symbol, sec_type="STK", currency="USD", exchange="SMART"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    contract.primaryExchange = "SMART"
    return contract

def create_bracket_order(order_id, direction, quantity, entry_price,
                          stop_loss_price, take_profit_price):
    # Parent limit order
    parent = Order()
    parent.orderId = order_id
    parent.action = direction
    parent.orderType = "LMT"
    parent.totalQuantity = quantity
    parent.lmtPrice = entry_price
    parent.tif = "GTC"
    parent.transmit = False
    # Disable unsupported attributes
    parent.eTradeOnly = False
    parent.firmQuoteOnly = False
    parent.optOutSmartRouting = False

    # Stop-loss order
    stop = Order()
    stop.orderId = order_id + 1
    stop.action = "SELL" if direction == "BUY" else "BUY"
    stop.orderType = "STP"
    stop.auxPrice = stop_loss_price
    stop.totalQuantity = quantity
    stop.parentId = order_id
    stop.tif = "GTC"
    stop.transmit = False
    # Disable unsupported attributes
    stop.eTradeOnly = False
    stop.firmQuoteOnly = False
    stop.optOutSmartRouting = False

    # Take-profit order
    take = Order()
    take.orderId = order_id + 2
    take.action = "SELL" if direction == "BUY" else "BUY"
    take.orderType = "LMT"
    take.lmtPrice = take_profit_price
    take.totalQuantity = quantity
    take.parentId = order_id
    take.tif = "GTC"
    take.transmit = True
    # Disable unsupported attributes
    take.eTradeOnly = False
    take.firmQuoteOnly = False
    take.optOutSmartRouting = False

    return [parent, stop, take]

if __name__ == "__main__":
    app = TradeApp()
    port = PAPER_PORT if IS_PAPER_TRADING else LIVE_PORT
    print(f"Connecting to {'Paper' if IS_PAPER_TRADING else 'Live'} trading on port {port}")
    app.connect("127.0.0.1", port, clientId=1)

    # Start the socket communication thread
    socket_thread = threading.Thread(target=run_loop, daemon=True)
    socket_thread.start()
    time.sleep(1)

    # Wait for the next valid order ID
    start = time.time()
    while app.nextValidOrderId is None and time.time() - start < 5:
        time.sleep(0.1)

    if app.nextValidOrderId is None:
        print("❌ Failed to obtain valid order ID, exiting.")
        app.disconnect()
        exit(1)

    print(f"⚡️ Placing bracket order for {SYMBOL}: Entry {ENTRY_PRICE}, SL {STOP_LOSS}, TP {TAKE_PROFIT}")
    orders = create_bracket_order(
        app.nextValidOrderId,
        DIRECTION,
        QUANTITY,
        ENTRY_PRICE,
        STOP_LOSS,
        TAKE_PROFIT
    )

    contract = get_contract(SYMBOL)
    # Submit orders
    for order in orders:
        app.placeOrder(order.orderId, contract, order)
        time.sleep(0.1)

    # Wait for submission/fill confirmation
    if app.order_event.wait(5):
        if app.order_placed:
            rr = (TAKE_PROFIT - ENTRY_PRICE) / (ENTRY_PRICE - STOP_LOSS)
            print(f"🎉 Bracket order placed! Risk-Reward: 1:{rr:.2f}")
        else:
            print("❌ Bracket order not confirmed.")
    else:
        print("❌ Timeout waiting for order confirmation.")

    time.sleep(1)
    app.disconnect()
    print("👋 Disconnected")
