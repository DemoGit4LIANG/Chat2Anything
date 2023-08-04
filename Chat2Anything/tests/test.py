import json
#
# from chains.database import SQLDatabase
#
# USER_NAME = "root"
# PASSWD = "mysql8"
# URL = "localhost"
# PORT = 3306
#
# MySQL_DB: SQLDatabase = SQLDatabase.from_uri(
#         "mysql+pymysql://"
#         + USER_NAME
#         + ":"
#         + PASSWD
#         + "@"
#         + URL
#         + ":"
#         + str(PORT),
#         engine_args={"pool_size": 10, "pool_recycle": 3600, "echo": True},
#     )


# configs = {
#   "MySQL8@locahost": {
#     "user_name": "root",
#     "password": "mysql8",
#     "url": "localhost",
#     "port": 3306
#   },
#   "MySQL57@locahost": {
#     "user_name": "root",
#     "password": "mysql57",
#     "url": "localhost",
#     "port": 3306
#   }
# }
#
# f = "/home/allen/llm_projs/enterprise_editon/Chat2Anything/chains/database/config.json"
# with open(f, "w") as w:
#   json.dump(configs, w)
#
# with open("/home/allen/llm_projs/enterprise_editon/Chat2Anything/chains/database/config.json", "r") as r:
#   db_configs = json.load(r)
#   print(db_configs)

CONFIG_PATH = "/home/allen/llm_projs/enterprise_editon/Chat2Anything/chains/database/config.json"
with open(CONFIG_PATH, "r") as json_file:
    db_configs: dict = json.load(json_file)

print(list(db_configs.keys())[0])