
import os


def load_vector_store_list(VECTOR_ROOT_PATH: str or os.PathLike):
    default = ["Click here to choose"]
    if not os.path.exists(VECTOR_ROOT_PATH):
        return default
    vector_store_list = os.listdir(VECTOR_ROOT_PATH)
    if not vector_store_list:
        return default
    vector_store_list.sort()
    return default + vector_store_list
