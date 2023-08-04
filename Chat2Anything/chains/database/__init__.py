import json
from .sql_database import SQLDatabase


CONFIG_PATH = "/home/allen/llm_projs/enterprise_editon/Chat2Anything/chains/database/config.json"
with open(CONFIG_PATH, "r") as json_file:
    db_configs: dict = json.load(json_file)


def _connect_all(configs):
    collections = {}
    for db_ident, config in configs.items():
        db: SQLDatabase = SQLDatabase.from_uri(
            "mysql+pymysql://"
            + config["user_name"]
            + ":"
            + config["password"]
            + "@"
            + config["url"]
            + ":"
            + str(config["port"]),
            engine_args={"pool_size": 10, "pool_recycle": 3600, "echo": True},
        )
        collections[db_ident] = db

    return collections


def get_conn_collections(config_path=CONFIG_PATH):
    with open(CONFIG_PATH, "r") as json_file:
        db_configs: dict = json.load(json_file)

    return _connect_all(configs=db_configs)

DB_CONNECTS = get_conn_collections()

db_list = list(db_configs.keys())
# db_collections = for db in db_list
default_config = db_configs[db_list[0]]
DEFAULT_DB = SQLDatabase.from_uri(
        "mysql+pymysql://"
        + default_config["user_name"]
        + ":"
        + default_config["password"]
        + "@"
        + default_config["url"]
        + ":"
        + str(default_config["port"]),
        engine_args={"pool_size": 10, "pool_recycle": 3600, "echo": True},
    )
