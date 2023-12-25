import threading
import time
from queue import Empty, Queue, Full
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from os import getenv, environ
from dotenv import load_dotenv
import psycopg2


# SELECT * FROM pg_stat_activity;

class ConnectionPool:
    db_params = {
        "dbname": getenv("DB_NAME", "postgres"),
        "user": getenv("DB_USER", "postgres"),
        "password": getenv("DB_PASSWORD", "1234"),
        "host": getenv("DB_HOST", "localhost")
    }

    def __init__(self, time_check=3, standard_amount_of_connections=10):
        load_dotenv()
        self.read_db_param()
        self.database_uri = environ["DATABASE_URL"]
        self.time_check = time_check
        self.standard_amount_of_connections = standard_amount_of_connections
        self.max_connections = 90
        self.active_connections = 0
        self.queue = Queue(maxsize=self.max_connections)
        self.semaphore = threading.Semaphore(2)
        self.init_connections()

    def read_db_param(self):
        self.db_params = {
            "dbname": getenv("DB_NAME", "postgres"),
            "user": getenv("DB_USER", "postgres"),
            "password": getenv("DB_PASSWORD", "1234"),
            "host": getenv("DB_HOST", "localhost")
        }

    def init_connections(self):
        while self.queue.qsize() < 20:
            self.add_connection_to_queue(self.db_params)

    # start when serwer started
    def check_amount_of_conections(self):
        while True:
            if self.queue.qsize() > 10:
                for _ in range(self.queue.qsize() - 10):
                    # conn = self.queue.get()
                    # conn.release_connection(conn)
                    # print("active:", self.active_connections)
                    # print("queuesieze:", self.queue.qsize())
                    pass
            time.sleep(5)

    def get_connection(self):
        with self.semaphore:
            conn = None
            try:
                conn = self.queue.get(block=False)
                self.active_connections += 1
            except Empty:
                if self.add_connection_to_queue(self.db_params):
                    conn = self.queue.get()
                    self.active_connections += 1
            print("active:", self.active_connections)
            print("queuesieze:", self.queue.qsize())
            return conn

    def add_connection_to_queue(self, param_db):
            if self.active_connections < self.max_connections:
                if isinstance(param_db, dict):
                    self.queue.put(psycopg2.connect(**param_db))
                else:
                    self.queue.put(param_db)
                return True
            else:
                # raise TooMuchConnections
                return False

    def release_connection(self, conn):
        print("release")
        with self.semaphore:
            try:
                if conn is not None:
                    self.add_connection_to_queue(conn)
                    self.active_connections -= 1
                    print("Relactive:", self.active_connections)
                    print("Relqueuesieze:", self.queue.qsize())
            except:
                print("except release")
                pass


if __name__ == '__main__':
    conn = ConnectionPool()
    conn.init_connections()
    # check_connections = Thread(target=conn.check_amount_of_conections, daemon=True)
    # check_connections.start()

    input("something: ")
    print("END")

class TooMuchConnections(Exception):
    pass
