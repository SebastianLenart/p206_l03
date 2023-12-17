import time
from queue import Empty, Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv
import psycopg2


class ConnectionPool:
    def __int__(self, time_check = 10, standard_amount_of_connections=10):
        load_dotenv()
        self.database_uri = os.environ["DATABASE_URL"]
        self.time_check = time_check
        self.standard_amount_of_connections = standard_amount_of_connections
        self.max_connections = 100
        self.queue = Queue(maxsize=self.max_connections)
        self.init_connections()

    def init_connections(self):
        for i in range(10):
            self.queue.put(psycopg2.connect(dsn=self.database_uri))


    # start when serwer started
    def check_amount_of_conections(self):
        i = 0
        while True:
            i += 1
            print(i)
            time.sleep(self.time_check)

    def get_connection(self):
        pass


if __name__ == '__main__':
    conn = ConnectionPool()
    check_connections = Thread(target=conn.check_amount_of_conections, daemon=True)
    check_connections.start()

    input("something: ")
    print("END")





























