import websocket
import json
from queue import Queue


class GdaxAdapter:

    def __init__(self, q: Queue):
        self.q = q
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://ws-feed.gdax.com",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def initMessage(self, ws):
        message_data = {
            "type": "subscribe",
            "product_ids": ["BTC-USD", "BCH-USD", "BCH-BTC",
                            "ETH-USD", "ETH-BTC", "LTC-USD", "LTC-BTC"],
            "channels": ["ticker"]        # channel: full -> for order book
        }                                 # ticker -> for the ticker

        message_json = json.dumps(message_data)
        self.ws.send(message_json)

    def on_message(self, ws, message):
        self.q.put(message, block=False)
        #print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        self.initMessage(ws)


if __name__ == "__main__":
    q = Queue()
    gdax = GdaxAdapter(q)
