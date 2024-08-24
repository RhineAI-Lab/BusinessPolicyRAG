from src.temp.gpt4 import call_gpt4

ECONOMIZE_LIST = [
  '北京', '天津', '河北', '山西', '内蒙古', '上海', '江苏', '浙江', '安徽', '山东', '福建', '广东', '广西', '海南',
  '湖北', '湖南', '河南', '江西', '吉林', '黑龙江', '辽宁', '四川', '重庆', '贵州', '云南', '西藏', '陕西', '宁夏', '甘肃', '青海', '新疆'
]
CITIES_MAP = [
    ['深圳', '广东'],
    ['广州', '广东'],
    ['苏州', '江苏'],
    ['成都', '四川'],
    ['武汉', '湖北'],
    ['杭州', '浙江'],
    ['南京', '江苏'],
    ['宁波', '浙江'],
    ['青岛', '山东'],
    ['长沙', '湖南'],
    ['无锡', '江苏'],
    ['佛山', '广东'],
    ['郑州', '河南'],
    ['东莞', '广东'],
    ['济南', '山东'],
    ['合肥', '安徽'],
    ['南通', '江苏'],
    ['常州', '江苏'],
    ['泉州', '福建'],
    ['西安', '陕西'],
    ['福州', '福建'],
    ['厦门', '福建'],
    ['唐山', '河北'],
    ['烟台', '山东'],
    ['大连', '辽宁'],
    ['温州', '浙江'],
    ['徐州', '江苏'],
    ['沈阳', '辽宁'],
    ['南宁', '广西'],
    ['哈尔滨', '黑龙江'],
    ['贵阳', '贵州'],
    ['佛山', '广东'],
    ['合肥', '安徽'],
    ['潍坊', '山东'],
    ['南昌', '江西'],
    ['东莞', '广东'],
    ['济宁', '山东'],
    ['嘉兴', '浙江'],
    ['邯郸', '河北'],
    ['台州', '浙江'],
    ['潍坊', '山东'],
    ['中山', '广东'],
    ['绍兴', '浙江'],
    ['兰州', '甘肃'],
    ['临沂', '山东'],
    ['岳阳', '湖南'],
    ['邢台', '河北'],
    ['淄博', '山东'],
    ['宜昌', '湖北'],
    ['宁德', '福建'],
    ['包头', '内蒙古'],
    ['信阳', '河南'],
    ['衡阳', '湖南'],
    ['张家口', '河北'],
    ['洛阳', '河南'],
    ['茂名', '广东'],
    ['长春', '吉林'],
    ['江门', '广东'],
    ['株洲', '湖南'],
    ['抚顺', '辽宁'],
    ['威海', '山东'],
    ['襄阳', '湖北'],
    ['新乡', '河南'],
    ['衡水', '河北'],
    ['宿迁', '江苏'],
    ['咸阳', '陕西'],
    ['岳阳', '湖南'],
    ['邵阳', '湖南'],
    ['许昌', '河南'],
    ['漳州', '福建'],
    ['梅州', '广东'],
    ['鹰潭', '江西'],
    ['宝鸡', '陕西'],
    ['北海', '广西'],
    ['丹东', '辽宁'],
    ['铁岭', '辽宁'],
    ['鞍山', '辽宁'],
    ['信阳', '河南'],
    ['赤峰', '内蒙古'],
    ['宿州', '安徽'],
    ['六盘水', '贵州'],
    ['宣城', '安徽'],
    ['丽水', '浙江'],
    ['南阳', '河南'],
    ['滨州', '山东'],
    ['宜春', '江西'],
    ['湖州', '浙江'],
    ['铜陵', '安徽'],
    ['黄石', '湖北'],
    ['周口', '河南'],
    ['邯郸', '河北'],
    ['景德镇', '江西'],
    ['德阳', '四川'],
    ['长治', '山西'],
    ['濮阳', '河南'],
    ['秦皇岛', '河北']
]

CHINA_KEYS = ['国家', '中国', 'China', '我国', '全国']
PART_LIST = ['国家', '华北', '华东', '华南', '华中', '东北', '西南', '西北']

BASE_PROMPT = '''
[REFERENCE]

你是一个精通中国所有政策的强大资深顾问。
你的主要职责是回答用户营商环境政策相关的问题，或与用户聊天也行。
上方是你可能需要参考的文献，当回答地区或政策相关问题时，请严格根据参考文献的原文回答,并一定要说出出处和页码位置，用户需要看原文。如果上方没提供参考文献则不用 。
在回答时，请不要让用户知道你有参考的上文。但要说出信息来源出处，上方文件中有每一段的页码，请说：”根据《国家及各省市营商环境政策汇编（2023年）》中xxx页的内容...“ 即可，参考了多处时，请在每一处标注参考的页码，这个很重要。
回答多条内容时，且每条信息来自不同的地方时，请在每条内容后面，分别说信息来自于第几页。说页码的时候要说 xx页 不能说 页xx。
没有参考文献时，请勿编造，合理回答没有相关政策这类话即可。
'''

PROMPT_LIMIT = 100000


def get_cities(history):
  cities = []
  first_line = True
  for line in history[::-1]:
    if len(line) > 1 and line[0] is not None:
      text = line[0]
      for item in ECONOMIZE_LIST:
        if item in text:
          cities.append(item)
      for item in CITIES_MAP:
        if item[0] in text:
          cities.append(item[1])
      if not first_line and len(cities) >= 3:
        break
      if first_line:
        print('\n\n' + text + '\n')
        for item in CHINA_KEYS:
          if len(cities) > 0:
            break
          if item in text:
            cities.append(CHINA_KEYS[0])
        first_line = False
  if len(cities) == 0:
    for line in history[::-1]:
      if len(line) > 1 and line[0] is not None:
        text = line[0]
        for item in CHINA_KEYS:
          if len(cities) > 0:
            break
          if item in text:
            cities.append(CHINA_KEYS[0])
  return cities


def get_content(city):
  return open(f'../../data/split/city/{city}.txt', 'r', encoding='utf-8').read()
    
  
def history_to_messages(history, system=None):
  messages = []
  if system:
    messages.append({'role': 'system', 'content': system})
  for line in history:
    if line[0]:
      messages.append({'role': 'user', 'content': line[0]})
    if line[1]:
      messages.append({'role': 'assistant', 'content': line[1]})
  return messages
  
  
def process_prompt(history):
  cities = get_cities(history)
  print('Mention Cities:', cities)
  references = [get_content(city) for city in cities]
  
  reference_length = 0
  for item in references:
    reference_length += len(item)
  
  reference = ''
  if reference_length == 0:
    reference = '[用户未提及城市信息，暂无可参考文献。]'
  else:
    scale = PROMPT_LIMIT / reference_length
    if scale < 1:
      print('\nBefore Reference Length:', reference_length)
      pr = 0.75  # Middle Point Rate
      for i, item in enumerate(references):
        l = len(item)
        p1, p2 = int(l * pr * scale), int(l * pr + l * (1 - pr) * (1 - scale))
        references[i] = item[:p1] + item[p2:]
        print(f'# {i} {cities[i]}: {0}~{p1} And {p2}~{l}')
    for item in references:
      reference += item
    print('Final Reference Length:', len(reference))
  
  prompt = BASE_PROMPT.replace('[REFERENCE]', reference)
  print('\nPrompt Length:', len(prompt))
  print('\n')
  
  messages = history_to_messages(history, prompt)
  history.append([None, None])
  for text in call_gpt4(messages, True):
    history[-1][1] = text
    yield history
    
  
if __name__ == '__main__':
  process_prompt([['', '对比上海和江西，江西有哪些政策优势？']])
