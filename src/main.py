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
pdf_url = 'http://10.177.47.31:3330/business.pdf'


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


def get_file_detail(result: NodeWithScore):
    dic = {
        'text': result.text,
        'file': result.metadata['file_path'],
        'page': result.metadata['page_label']
    }
    return dic


page_label = 1


def process_input(history, html_box):
    print('a')
    question = history[-1][0]
    response = query_engine.query(question)
    
    global page_label
    info_list = []
    results = query_retriever.retrieve(question)
    for result in results:
        detail = get_file_detail(result)
        print(detail)
        info_list.append(f'Page {detail["page"]}\n{detail["text"]}')
        if detail['page']:
            page_label = detail['page']
    if history[-1][1]:
        history.append([None, None])
    history[-1][1] = '\n\n'.join(info_list)
    history.append([None, str(response)])
    
    return history, f'<embed src="{pdf_url}#page={page_label}" width="700" height="900" type="application/pdf">'


def add_message(history, message):
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False, file_types=None, placeholder="Processing...",
                                         show_label=False)


def main():
    with gr.Blocks(css=open('./main.css', mode='r', encoding='utf-8').read()) as demo:
        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(scale=1)
                chat_input = gr.MultimodalTextbox(interactive=True, file_types=["image"],
                                                  placeholder="Enter message or upload file...", show_label=False)
            with gr.Column(scale=1):
                html_box = gr.HTML(
                    value=f'<embed src="{pdf_url}#page=1" type="application/pdf">')
            chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
            bot_msg = chat_msg.then(process_input, [chatbot, html_box], [chatbot, html_box])
            bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True, file_types=["image"],
                                                      placeholder="Enter message or upload file...", show_label=False),
                         None, [chat_input])
    demo.launch(server_name='0.0.0.0', server_port=7873)


if __name__ == '__main__':
    main()
