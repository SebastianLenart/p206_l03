from connect_sql import GetConnection
import database


def show_list_users():
    with GetConnection() as connection:
        return [element[0] for element in database.get_list_nicks(connection)]

if __name__ == "__main__":
    print(show_list_users())