import torch.backends
import os
import uuid

embedding_model_dict = {
    "text2vec": "/home/allen/llm_projs/text2vec-large-chinese",
    # "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    # "ernie-base": "nghuyong/ernie-3.0-base-zh",
    # "text2vec-base": "shibing624/text2vec-base-chinese",
}
# Embedding model name
EMBEDDING_MODEL = "text2vec"
# LLM streaming reponse
STREAMING = True
# Embedding running device
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
# LLM running device
LLM_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
# Path to store the embedding vectors
VECTOR_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_stores")
UPLOAD_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "upload_files")

# 文本分句长度
SENTENCE_LEN = 100
# 匹配后单段上下文长度
CHUNK_SIZE = 250
# LLM input history length
LLM_HISTORY_LEN = 3
# return top-k text chunk from vector store
VECTOR_SEARCH_TOP_K = 5
# 知识检索内容相关度 Score, 数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
VECTOR_SEARCH_SCORE_THRESHOLD = 0

NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")
# NLTK_DATA_PATH = "/home/allen/llm_projs/langchain-ChatGLM-master/nltk_data"
print(NLTK_DATA_PATH)
FLAG_USER_NAME = uuid.uuid4().hex


import logging

LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT, filename="")

logger.info(f"""
loading model config
llm device: {LLM_DEVICE}
embedding device: {EMBEDDING_DEVICE}
dir: {os.path.dirname(os.path.dirname(__file__))}
flagging username: {FLAG_USER_NAME}
""")

# is open cross domain
OPEN_CROSS_DOMAIN = True

