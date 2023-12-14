from connect_sql import GetConnection
import database
from threading import Thread
from time import perf_counter



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
        pass

    end_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')

    main()