import time
from queue import Empty, Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


class ConnectionPool:
    def __int__(self):
        self.queue = Queue()

    # start when serwer started
    def check_amount_of_conections(self):
        i = 0
        while True:
            i += 1
            print(i)
            time.sleep(10)


if __name__ == '__main__':
    conn = ConnectionPool()
    check_connections = Thread(target=conn.check_amount_of_conections, daemon=True)
    check_connections.start()

    input("something: ")
    print("END")





























