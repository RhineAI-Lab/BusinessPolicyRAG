from glm4_rag import ChatGLM, ChatGLMEmbeddings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
import base64
import os
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import NodeWithScore
import gradio as gr
import time

ZHIPU_API_KEY = 'b3589487b559e0400ced55525f26f3c2.WdVen2vc1c9f9dNC'
file_dir = '../data'


def get_file_detail(result:NodeWithScore):
    dic = {'text':result.text,
           'file':result.metadata['file_path'],
           'page':result.metadata['page_label']
           }
    return dic

# 后端处理函数，接受用户输入并返回处理后的输出
def process_input(question, two):
    # return 'Test'
    # 在这里添加你的处理逻辑
    response = query_engine.query(question)
    results = query_retriever.retrieve(question)
    results = [get_file_detail(result) for result in results]
    return '检索内容：\n'+str(results)+'\n\n回复内容：\n'+str(response)

def display_pdf(file_path):
    try:
        with open(file_path, "rb") as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode('utf-8')

        pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf">'
        return pdf_display
    except Exception as e:
        return str(e)  # 显示错误信息


def main():
    with gr.Blocks() as demo:
        with gr.Column(scale=1):
                chat = gr.ChatInterface(fn=process_input).queue()
        with gr.Column(scale=1):
                dropdown = gr.Dropdown(choices=pdf_files, label="Select a PDF file")
                html_box = gr.HTML()
                dropdown.change(display_pdf, inputs=dropdown, outputs=html_box)

    demo.launch(server_name="0.0.0.0")


# define our LLM
print('Build Up LLM')
Settings.llm = ChatGLM(model='glm-4', reuse_client=True, api_key=ZHIPU_API_KEY, )

# define embed model
print('Build Up Embed Model')
Settings.embed_model = ChatGLMEmbeddings(model='embedding-2', reuse_client=True, api_key=ZHIPU_API_KEY, )

start = time.time()
print('Build Up Directory', time.time() - start)
documents = SimpleDirectoryReader(file_dir).load_data()
print('Build Up Vectory Index', time.time() - start)
index = VectorStoreIndex.from_documents(documents)
print('Done', time.time() - start)

start = time.time()
print('Getting response ....')
query_engine = index.as_query_engine()
query_retriever = index.as_retriever()

print('Done', time.time() - start)

pdf_files = [os.path.join(file_dir, file) for file in os.listdir(file_dir)]
main()
