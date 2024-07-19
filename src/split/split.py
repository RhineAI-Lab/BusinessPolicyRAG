import fitz  # PyMuPDz

# 打开PDF文件
pdf_document = "../../data/business.pdf"
doc = fitz.open(pdf_document)

# 提取文本
text = ""
for page_num in range(len(doc)):
    page = doc.load_page(page_num)  # 加载页
    text += page.get_text()  # 提取文本
    break

# 打印提取的文本
print(text)
