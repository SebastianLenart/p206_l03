from connect_sql import GetConnection
import database
from threading import Thread
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor



def show_list_users():
    with GetConnection() as connection:
        return [element[0] for element in database.get_list_nicks(connection)]


def main():
    pass




if __name__ == "__main__":

    start_time = perf_counter()

    # without thread:
    for _ in range(10):
        show_list_users()

    # with thread
    for _ in range(10):
        with ThreadPoolExecutor() as executor:
            executor.map(show_list_users())

    end_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')

    main()