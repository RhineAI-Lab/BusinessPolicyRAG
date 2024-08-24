import time
import re
import os

from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex, StorageContext, Settings, load_index_from_storage
from llama_index.core.schema import NodeWithScore

import gradio as gr

from glm4_rag import ChatGLM, ChatGLMEmbeddings
from src.main.prompt_make import process_prompt

# %%
ZHIPU_API_KEY = 'b3589487b559e0400ced55525f26f3c2.WdVen2vc1c9f9dNC'  # API_KEY
FILE_DIR = '../../data/rag'  # 知识库目录
STORAGE_DIR = '../../storage'  # RAG Index缓存
PDF_URL = 'http://10.177.47.31:3330/business.pdf'  # 展示PDF地址

page_label = 1


# print('Build Up LLM')
# Settings.llm = ChatGLM(model='glm-4', reuse_client=True, api_key=ZHIPU_API_KEY, )
# # define embed model
# print('Build Up Embed Model')
# Settings.embed_model = ChatGLMEmbeddings(model='embedding-2', reuse_client=True, api_key=ZHIPU_API_KEY)
# print()
#
# if not os.path.exists(STORAGE_DIR):
#   start = time.time()
#   print('Build Up Directory', time.time() - start)
#   documents = SimpleDirectoryReader(FILE_DIR).load_data()
#   print('Build Up Vectory Index', time.time() - start)
#   index = VectorStoreIndex.from_documents(documents)
#   print('Done', time.time() - start)
#   print()
#   index.storage_context.persist(persist_dir=STORAGE_DIR)
# else:
#   print('Loading Index From Storage')
#   # load the existing index
#   storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
#   index = load_index_from_storage(storage_context)
#
# start = time.time()
# print('Getting response...')
# query_engine = index.as_query_engine()
# query_retriever = index.as_retriever()
# print('Done', time.time() - start)


def get_file_detail(result: NodeWithScore):
  dic = {
    'text': result.text,
    'file': result.metadata['file_path'],
    'page': result.metadata['page_label']
  }
  return dic


def process_input(history, html_box):
  # question = history[-1][0]
  # response = query_engine.query(question)
  # global page_label
  # info_list = []
  # results = query_retriever.retrieve(question)
  #
  # if history[-1][1]:
  #   history.append([None, None])
  # history[-1][1] = '\n\n'.join(info_list)
  # history.append([None, str(response)])
  
  return history, f'<embed src="{PDF_URL}#page={page_label}" width="700" height="900" type="application/pdf">'
  
  
def extract_first_page_number_specific_title(text, title):
  pattern = rf"{re.escape(title)}[^页]*?(\d+页)"
  match = re.search(pattern, text)
  if match:
    return int(match.group(1)[0:-1])
  return -1


def process(history, html_box):
  global page_label
  for result in process_prompt(history):
    last: str = result[-1][1]
    i = extract_first_page_number_specific_title(last, '《国家及各省市营商环境政策汇编（2023年）》')
    if i > 0:
      page_label = i
    yield result, f'<embed src="{PDF_URL}#page={page_label}" width="700" style="height: 100%;" type="application/pdf">'


def add_message(history, message):
  for x in message["files"]:
    history.append(((x,), None))
  if message["text"] is not None:
    history.append((message["text"], None))
  return history, gr.MultimodalTextbox(
    value=None, interactive=False, file_types=None, placeholder="Processing...", show_label=False)


def main():
  with gr.Blocks(
    css=open('./main.css', mode='r', encoding='utf-8').read(),
    js=open('./main.js', mode='r', encoding='utf-8').read(),
    title='营商政策AI问答',
  ) as demo:
    with gr.Row():
      with gr.Column(scale=1, elem_id='rag_chat'):
        chatbot = gr.Chatbot(value=[[None, '我可以回答您各种中国及各省市营商环境政策相关的问题，请问有什么可以帮您？']], scale=1)
        chat_input = gr.MultimodalTextbox(
            interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False)
      with gr.Column(scale=1, elem_id='rag_web'):
        html_box = gr.HTML(value=f'<embed src="{PDF_URL}#page=1" width="700" height="100%" type="application/pdf">')
      chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
      bot_msg = chat_msg.then(process, [chatbot, html_box], [chatbot, html_box])
      bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False), None, [chat_input])
  demo.launch(server_name='0.0.0.0')


if __name__ == '__main__':
  main()
  # 吉林对创业者有什么优势政策
  # 在杭州适合开互联网公司吗？
  # 苏州和上海比起来，有什么政策上的优势？
  
  