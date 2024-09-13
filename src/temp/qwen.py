import random
import time

from openai import OpenAI

client = OpenAI(
  api_key="sk-oBLj3xZQyhEnmWgS2eDc0991Df0341D5AdF235E6Ba22BbBd",
  base_url="https://api.pumpkinaigc.online/v1",
  timeout=120,
)

def call_gpt4(messages, print_in_stream=False, model='gpt-4o'):
  try:
    stream = client.chat.completions.create(
      model=model,
      messages=messages,
      stream=True,
      timeout=120,
    )
    text = ''
    for chunk in stream:
      if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        text += content
        yield text
        if print_in_stream:
          print(content, end="")
    if print_in_stream:
      print('')
    if len(text) > 0:
      yield text
    else:
      yield 'EMPTY RESPONSE'
  except Exception as e:
    print(e)
    yield 'NETWORK ERROR'


if __name__ == '__main__':
  messages = [{"role": "user", "content": "你好"}]
  for item in call_gpt4(messages, print_in_stream=True):
    pass

