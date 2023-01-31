from mongoengine import connect
from configparser import ConfigParser
import pathlib


file_config = pathlib.Path(__file__).parent.parent.joinpath('config/config.ini')
print(f'file_config: {file_config}')
config = ConfigParser()
config.read(file_config)

user = config.get("DB-MONGO", "user")
password = config.get("DB-MONGO", "password")
domain = config.get("DB-MONGO", "domain")
db_name = config.get("DB-MONGO", "db_name")


def conn_to_db ():
    connect(host=f"""mongodb+srv://{user}:{password}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)


if __name__ == '__main__':
    conn_to_db()
