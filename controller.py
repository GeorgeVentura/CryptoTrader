"""
    (thread #1)
    Works by requesting a data stream from Gdax (websocket), parsing each response into a dict and
    inserting it into a queue.

    (thread #2)
    listening on web socket.

    (thread #3)
    grabs item from the queue and updates the graph weight values.

    (thread #4)
    runs bellman-ford on the graph to find negative cost cycles.

"""


from queue import Queue
from graph import Graph
from gdaxAdapter import GdaxAdapter
import json
import threading


class Controller:

    def __init__(self):
        self.q = Queue()
        self.g = Graph()
        self.g_dax = None
        self.init_graph()

    # starting values, (this can be changed)**
    def init_graph(self):
        self.g.add_edge("BTC", "USD", 10809)
        self.g.add_edge("BCH", "USD", 1202.13)
        self.g.add_edge("BCH", "BTC", 0.11108)
        self.g.add_edge("ETH", "USD", 820.22)
        self.g.add_edge("ETH", "BTC", 0.07589)
        self.g.add_edge("LTC", "USD", 199.28)
        self.g.add_edge("LTC", "BTC", 0.01835)

    def start_data_feed(self):
        self.g_dax = GdaxAdapter(self.q)

    def start(self):
        threading.Thread(target=self.start_data_feed).start()
        threading.Thread(target=self.consume_data).start()
        threading.Thread(target=self.find_neg_cycles).start()

    def find_neg_cycles(self):
        update_flag = self.q.qsize()        # check flag, so algo is called only when graph is updated. todo:Check this
        while True:
            while self.q.not_empty:
                if update_flag == self.q.qsize():
                    continue
                paths = []
                for v in self.g.graph:      # check if asset type that is in graph. *Can be changed to only perform
                    path = None                                                    # the asset on hand
                    try:
                        path = self.g.bellman_ford(v)
                    except Exception as e:
                        None                # todo: handle the exception
                    if path not in paths and path is not None:  # todo: check this, may not filter out equivalent paths
                        paths.append(path)
                if len(paths) > 0:
                    print(paths + self.calculate_dist(paths))
                update_flag = self.q.qsize()

    def calculate_dist(self, paths):
        dist_list = []
        for path in paths:
            dist = 0
            for i in range(len(path)-1):
                dist += self.g.get_edge_weight(path[i], path[i+1])
            dist_list.append(dist)
        return dist_list

    def consume_data(self):
        while True:
            while not self.q.empty():
                try:
                    j = json.loads(self.q.get())
                    self.update_graph(j)
                except Exception as e:
                    print(e)

    def update_graph(self, tick):
        if 'type' in tick and tick['type'] == 'ticker':
            try:
                pair = tick['product_id'].split('-')
                u = pair[0]
                v = pair[1]
                w = float(tick['price'])
                self.g.set_weight(u, v, w)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    c = Controller()
    c.start()
