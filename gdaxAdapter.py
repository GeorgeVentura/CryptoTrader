import websocket
import json
try:
    import thread
except ImportError:
    import _thread as thread
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
        self.q.put(message)
        #print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        self.initMessage(ws)

        def run(*args):
            while True:
                None

        thread.start_new_thread(run, ())

    # Process the data
    def process_q(self):
        while True:
            while not self.q.empty():
                j = json.loads(q.get())
                try:
                    print(j)
                except Exception as e:
                    print(e)
                #self.write_to_txt_file(self.q.get())

    def write_to_txt_file(self, msg):
        with open('orderbook.txt', 'a') as f:
            f.write(msg)


if __name__ == "__main__":
    q = Queue()
    gdax = GdaxAdapter(q)
