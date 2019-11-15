from dotenv import load_dotenv
from usos.usos_connection import USOSConnection

if __name__ == '__main__':
    load_dotenv()
    usos_conn = USOSConnection()
    # TODO: Setup connection with MySQL database and select all users' tokens and secrets into a list
