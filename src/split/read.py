import fitz

# page_list = {
#   '国家': 1, '北京': 102, '天津': 140, '河北': 157, '山西': 185, '内蒙古': 226, '上海': 302, '江苏': 464, '浙江': 530,
#   '安徽': 604, '山东': 676, '福建': 758, '广东': 833, '广西': 979, '海南': 1001, '湖北': 1038, '湖南': 1078,
#   '河南': 1102, '江西': 1153, '吉林': 1230, '黑龙江': 1283, '辽宁': 1295, '四川': 1316, '重庆': 1376,
#   '贵州': 1409, '云南': 1432, '西藏': 1479, '陕西': 1479, '宁夏': 1558, '甘肃': 1599, '青海': 1704, '新疆': 1704
# }
# page_list = {
#   '国家': 1, '华北': 102, '华东': 302, '华南': 833, '华中': 1038, '东北': 1230, '西南': 1316, '西北': 1479
# }
page_list = {
  '全国': 1,
}
keys = list(page_list.keys())

pdf_document = '../../data/business.rag'
doc = fitz.open(pdf_document)
for city in page_list.keys():
    target_file = f'../../data/split/all/{city}.txt'
    start = page_list.get(city)
    end_i = keys.index(city) + 1
    end = page_list[keys[end_i]] if end_i < len(keys) else doc.page_count
    print(f'Start analysis {city}.txt     From {start}~{end}')
    
    text = ''
    for page_num in range(start - 1, end):
        text += f'\n# Page {page_num + 1}:\n'
        blocks = doc[page_num].get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span['size'] > 9.1 and span['font'] != 'TimesNewRomanPSMT':
                            text += span['text'] + '\n'
    open(target_file, 'w', encoding='utf-8').write(text)
    
print('Finished')
