
from chains.loader.image_loader import UnstructuredPaddleImageLoader
from chains.loader.pdf_loader import UnstructuredPaddlePDFLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredFileLoader, TextLoader
from configs.model_config import *
from chains.textsplitter.chinese_text_splitter import ChineseTextSplitter
from typing import List, Tuple
import numpy as np
from utils import torch_gc
from tqdm import tqdm
from langchain.docstore.document import Document


PROMPT_TEMPLATE = """已知信息：
{context}

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}"""


def load_file(file_path, sentence_len=SENTENCE_LEN):
    if file_path.lower().endswith(".md"):
        loader = UnstructuredFileLoader(file_path, mode="elements")
        docs = loader.load()
    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path, autodetect_encoding=True)
        textsplitter = ChineseTextSplitter(pdf=False, sentence_len=sentence_len)
        docs = loader.load_and_split(textsplitter)
    elif file_path.lower().endswith(".pdf"):
        loader = UnstructuredPaddlePDFLoader(file_path)
        textsplitter = ChineseTextSplitter(pdf=True, sentence_len=sentence_len)
        docs = loader.load_and_split(textsplitter)
    elif file_path.lower().endswith(".jpg") or file_path.lower().endswith(".png"):
        loader = UnstructuredPaddleImageLoader(file_path, mode="elements")
        textsplitter = ChineseTextSplitter(pdf=False, sentence_len=sentence_len)
        docs = loader.load_and_split(text_splitter=textsplitter)
    else:
        loader = UnstructuredFileLoader(file_path, mode="elements")
        textsplitter = ChineseTextSplitter(pdf=False, sentence_len=sentence_len)
        docs = loader.load_and_split(text_splitter=textsplitter)

    write_check_file(file_path, docs)

    return docs


def write_check_file(filepath, docs):
    folder_path = os.path.join(os.path.dirname(filepath), "tmp_files")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    fp = os.path.join(folder_path, 'load_file.txt')
    with open(fp, 'a+', encoding='utf-8') as fout:
        fout.write("filepath=%s,len=%s" % (filepath, len(docs)))
        fout.write('\n')
        for i in docs:
            fout.write(str(i))
            fout.write('\n')
        fout.close()


def generate_prompt(related_docs: List[str],
                    query: str,
                    prompt_template: str = PROMPT_TEMPLATE, ) -> str:
    context = "\n".join([doc.page_content for doc in related_docs])
    # prompt = prompt_template.replace("{user_input}", query).replace("{context}", context)
    prompt = prompt_template.replace("{question}", query).replace("{context}", context)

    return prompt


def seperate_list(ls: List[int]) -> List[List[int]]:
    lists = []
    ls1 = [ls[0]]
    for i in range(1, len(ls)):
        if ls[i - 1] + 1 == ls[i]:
            ls1.append(ls[i])
        else:
            lists.append(ls1)
            ls1 = [ls[i]]
    lists.append(ls1)
    return lists


def similarity_search_with_score_by_vector(
        self, embedding: List[float], k: int = 4
) -> List[Tuple[Document, float]]:
    scores, indices = self.index.search(np.array([embedding], dtype=np.float32), k)
    docs = []
    id_set = set()
    store_len = len(self.index_to_docstore_id)

    for j, i in enumerate(indices[0]):
        if i == -1 or 0 < self.score_threshold < scores[0][j]:
            # This happens when not enough docs are returned.
            continue
        _id = self.index_to_docstore_id[i]
        doc = self.docstore.search(_id)
        if not self.chunk_conent:
            if not isinstance(doc, Document):
                raise ValueError(f"Could not find document for id {_id}, got {doc}")
            doc.metadata["score"] = int(scores[0][j])
            docs.append(doc)
            continue

        id_set.add(i)
        docs_len = len(doc.page_content)
        for k in range(1, max(i, store_len - i)):
            break_flag = False
            for l in [i + k, i - k]:
                if 0 <= l < len(self.index_to_docstore_id):
                    _id0 = self.index_to_docstore_id[l]
                    doc0 = self.docstore.search(_id0)
                    if docs_len + len(doc0.page_content) > self.chunk_size:
                        break_flag = True
                        break
                    elif doc0.metadata["source"] == doc.metadata["source"]:
                        docs_len += len(doc0.page_content)
                        id_set.add(l)
            if break_flag:
                break

    if not self.chunk_conent:
        return docs
    if len(id_set) == 0 and self.score_threshold > 0:
        return []

    id_list = sorted(list(id_set))
    id_lists = seperate_list(id_list)

    for id_seq in id_lists:
        for id in id_seq:
            if id == id_seq[0]:
                _id = self.index_to_docstore_id[id]
                doc = self.docstore.search(_id)
            else:
                _id0 = self.index_to_docstore_id[id]
                doc0 = self.docstore.search(_id0)
                doc.page_content += " " + doc0.page_content
        if not isinstance(doc, Document):
            raise ValueError(f"Could not find document for id {_id}, got {doc}")
        doc_score = min([scores[0][id] for id in [indices[0].tolist().index(i) for i in id_seq if i in indices[0]]])
        doc.metadata["score"] = int(doc_score)
        docs.append(doc)

    torch_gc()

    return docs


def search_result2docs(search_results):
    docs = []
    for result in search_results:
        doc = Document(page_content=result["snippet"] if "snippet" in result.keys() else "",
                       metadata={"source": result["link"] if "link" in result.keys() else "",
                                 "filename": result["title"] if "title" in result.keys() else ""})
        docs.append(doc)
    return docs


class LocalVectorStore:
    # llm: BaseAnswer = None
    embeddings: object = None
    top_k: int = VECTOR_SEARCH_TOP_K
    chunk_size: int = CHUNK_SIZE
    chunk_conent: bool = True
    score_threshold: int = VECTOR_SEARCH_SCORE_THRESHOLD

    def init_cfg(self,
                 embedding_model: str = EMBEDDING_MODEL,
                 embedding_device = EMBEDDING_DEVICE,
                 # llm_model: BaseAnswer = None,
                 top_k=VECTOR_SEARCH_TOP_K,
                 ):
        # self.llm = llm_model
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dict[embedding_model], model_kwargs={'device': embedding_device})
        self.top_k = top_k

    # initialize vector store
    def init_vector_store(self, file_path: str or List[str], vector_store_path: str or os.PathLike = None, sentence_len=SENTENCE_LEN):
        loaded_files = []
        failed_files = []

        if isinstance(file_path, str):
            # file_path: os.path.join(UPLOAD_ROOT_PATH, vs_id, filename)
            if not os.path.exists(file_path):
                print("target path does not exist")
                return None
            elif os.path.isfile(file_path):
                file = os.path.split(file_path)[-1]
                try:
                    docs = load_file(file_path, sentence_len)
                    logger.info(f"{file} has been loaded")
                    loaded_files.append(file_path)
                except Exception as e:
                    logger.error(e)
                    logger.info(f"{file} fails to load")
                    return None
            elif os.path.isdir(file_path):
                docs = []
                for file in tqdm(os.listdir(file_path), desc="loading file"):
                    fullfilepath = os.path.join(file_path, file)
                    try:
                        docs += load_file(fullfilepath, sentence_len)
                        loaded_files.append(fullfilepath)
                    except Exception as e:
                        logger.error(e)
                        failed_files.append(file)

                if len(failed_files) > 0:
                    logger.info("Fail to load the files:")
                    for file in failed_files:
                        logger.info(f"{file}\n")
        else:
            docs = []
            for file in file_path:
                try:
                    docs += load_file(file)
                    logger.info(f"{file} has been loaded")
                    loaded_files.append(file)
                except Exception as e:
                    logger.error(e)
                    logger.info(f"{file} fails to load")

        if len(docs) > 0:
            logger.info("files loaded，generating the embedding vectors")
            try:
                vector_store = FAISS.load_local(vector_store_path, self.embeddings)
                vector_store.add_documents(docs)
                torch_gc()
            except Exception as _:
                vector_store = FAISS.from_documents(docs, self.embeddings)  # docs 为Document列表
                torch_gc()

            # save the sentence embedding vectors
            vector_store.save_local(vector_store_path)

            return vector_store_path, loaded_files
        else:
            logger.info("Fail to load all files，please check the errors and re-upload")
            return None, loaded_files

    def gen_prompt_with_vector(self, query, vector_store_path):
        vector_store = FAISS.load_local(vector_store_path, self.embeddings)
        FAISS.similarity_search_with_score_by_vector = similarity_search_with_score_by_vector
        vector_store.chunk_size = self.chunk_size
        vector_store.chunk_conent = self.chunk_conent
        vector_store.score_threshold = self.score_threshold
        related_docs_with_score = vector_store.similarity_search_with_score(query, k=self.top_k)
        torch_gc()
        prompt = generate_prompt(related_docs_with_score, query)

        return prompt
