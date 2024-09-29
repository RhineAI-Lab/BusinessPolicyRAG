import gradio as gr


def process_input(history, html_box):
  return history, f'<embed src="http://localhost:7880/business.pdf#page={0}" type="application/pdf">'


def add_message(history, message):
  return history, gr.MultimodalTextbox(value=None, interactive=False, file_types=None, placeholder="Processing...", show_label=False)


def main():
  with gr.Blocks(css=open('./main.css', mode='r', encoding='utf-8').read()) as demo:
    with gr.Row():
      with gr.Column(scale=1):
        chatbot = gr.Chatbot()
        chat_input = gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False)
      with gr.Column(scale=1):
        html_box = gr.HTML(value=f'<embed src="http://localhost:7880/business.pdf#page=1" type="application/pdf">')
      chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
      bot_msg = chat_msg.then(process_input, [chatbot, html_box], [chatbot, html_box])
      bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False), None, [chat_input])
  demo.queue()
  demo.launch(server_port=7868)


if __name__ == '__main__':
  main()
