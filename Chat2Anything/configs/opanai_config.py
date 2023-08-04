import os


def init_openai():
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.com/v1"
