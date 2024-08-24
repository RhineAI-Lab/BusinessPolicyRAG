import time
import re
import os

import gradio as gr

def add_message():
  return ''

PDF_URL = 'http://10.177.47.31:3330/business.pdf'  # 展示PDF地址

def process():
  return ''

def main():
  with gr.Blocks(
    css=open('./main.css', mode='r', encoding='utf-8').read(),
    js=open('./main.js', mode='r', encoding='utf-8').read(),
  ) as demo:
    with gr.Row():
      with gr.Column(scale=1, elem_id='rag_chat'):
        chatbot = gr.Chatbot(scale=1)
        chat_input = gr.MultimodalTextbox(
            interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False)
      with gr.Column(scale=1, elem_id='rag_web'):
        html_box = gr.HTML(value=f'<embed src="{PDF_URL}#page=1" width="700" height="900" type="application/pdf">')
      chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
      bot_msg = chat_msg.then(process, [chatbot, html_box], [chatbot, html_box])
      bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False), None, [chat_input])
  demo.launch(server_name='0.0.0.0')


if __name__ == '__main__':
  main()
  
  