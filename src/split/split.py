import fitz
import re

# 打开PDF文件
pdf_document = "../../data/business.pdf"
doc = fitz.open(pdf_document)

# 提取文本
text = ""
for page_num in range(len(doc)):
    page = doc.load_page(page_num)  # 加载页
    page_text = page.get_text()  # 提取文本page_
    print(page_text)
    text += page_text
    if page_num > 22:
        break

catalog_str = text

# 正则表达式匹配省市标题和页码
pattern = re.compile(r"（[一二三四五六七八九十]+）([\u4e00-\u9fa5]+).*?(\d+)", re.S)

# 使用 findall 提取所有匹配的内容
matches = pattern.findall(catalog_str)

# 构建字典
result = {}
for match in matches:
    region = match[0].strip()
    page = int(match[1])
    result[region] = page

print(result)

result = {'北京': 102, '天津': 140, '河北': 157, '山西': 185, '内蒙古': 226, '上海': 302, '江苏': 464, '浙江': 530, '安徽': 604, '山东': 676, '福建': 758, '广东': 833, '广西': 979, '海南': 1001, '湖北': 1038, '湖南': 1078, '河南': 1102, '江西': 1153, '吉林': 1230, '黑龙江': 1283, '辽宁省': 1295, '四川': 1316, '重庆': 1376, '贵州': 1409, '云南': 1432, '西藏': 1479, '陕西': 1479, '宁夏': 1558, '甘肃': 1599, '青海': 1704, '新疆': 1704}



