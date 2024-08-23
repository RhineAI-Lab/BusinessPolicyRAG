import random
import time

from openai import OpenAI


def call_gpt4(user_prompt, system_prompt='你是个语言能力和逻辑理解能力很强的AI助手', print_in_stream=False):
  time.sleep(5)
  client = OpenAI(
    api_key="sk-oBLj3xZQyhEnmWgS2eDc0991Df0341D5AdF235E6Ba22BbBd",
    base_url="https://api.pumpkinaigc.online/v1",
    timeout=120,
  )
  messages = [
    {'role': 'system', 'content': system_prompt},
    {'role': 'user', 'content': user_prompt}
  ]
  try:
    stream = client.chat.completions.create(
      model="gpt-4o",
      # model="gpt-3.5-turbo",
      messages=messages,
      stream=True,
      timeout=120,
      top_p=0.2,
      temperature=0.2,
    )
    text = ''
    for chunk in stream:
      if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        text += content
        if print_in_stream:
          print(content, end="")
    if print_in_stream:
      print('')
    if len(text) > 0:
      return text
    else:
      print('Empty response.')
  except Exception as e:
    print(e)
  client.close()
  return 'ERROR'


if __name__ == '__main__':
  content = open('../../data/split/city/内蒙古.txt', 'r', encoding='utf-8').read()
  prompt = content + '\n\n阅读上方营商政策汇总文件，严格根据文件回答用户问题。\n\n内蒙古政策有提到一网通办的相关信息吗？详细列出来，给出页码。'
  call_gpt4(prompt, print_in_stream=True)

