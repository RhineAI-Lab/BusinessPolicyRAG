import gradio as gr

def display_pdf(file_path):
    try:
        pdf_display = f'<embed src="http://localhost:3330/bussiness.pdf" width="700" height="1000" type="application/pdf">'
        return pdf_display
    except Exception as e:
        return str(e)

with gr.Blocks() as demo:
  pdf_files = ['../data/business.pdf']
  with gr.Column(scale=1):
    dropdown = gr.Dropdown(choices=pdf_files, label="Select a PDF file")
    html_box = gr.HTML()
    dropdown.change(display_pdf, inputs=dropdown, outputs=html_box)

demo.launch()