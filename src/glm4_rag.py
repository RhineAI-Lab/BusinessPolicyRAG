import sys
import time
from typing import Optional, List, Any, Sequence, Dict
from llama_index.core.bridge.pydantic import Field, PrivateAttr
from llama_index.core.constants import DEFAULT_CONTEXT_WINDOW, DEFAULT_NUM_OUTPUTS
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
    ChatMessage,
    ChatResponse,
)
from llama_index.core.llms.callbacks import llm_completion_callback, llm_chat_callback

from zhipuai import ZhipuAI

DEFAULT_MODEL = 'glm-4'

def to_message_dicts(messages: Sequence[ChatMessage])->List:
    return [
        {"role": message.role.value, "content": message.content,}
                for message in messages if all([value is not None for value in message.values()])
    ]

def get_additional_kwargs(response) -> Dict:
    return {
        "token_counts":response.usage.total_tokens,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
    }

class ChatGLM(CustomLLM):
    num_output: int = DEFAULT_NUM_OUTPUTS
    context_window: int = Field(default=DEFAULT_CONTEXT_WINDOW,description="The maximum number of context tokens for the model.",gt=0,)
    model: str = Field(default=DEFAULT_MODEL, description="The ChatGlM model to use. glm-4 or glm-3-turbo")
    api_key: str = Field(default=None, description="The ChatGLM API key.")
    reuse_client: bool = Field(default=True, description=(
            "Reuse the client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )
    _client: Optional[Any] = PrivateAttr()
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        reuse_client: bool = True,
        api_key: Optional[str] = None,
        **kwargs: Any,
    )-> None:
        super().__init__(
            model=model,
            api_key=api_key,
            reuse_client=reuse_client,
            **kwargs,
        )
        self._client = None

    def _get_client(self) -> ZhipuAI:
        if not self.reuse_client :
            return ZhipuAI(api_key=self.api_key)

        if self._client is None:
            self._client = ZhipuAI(api_key=self.api_key)
        return self._client

    @classmethod
    def class_name(cls) -> str:
        return "chatglm_llm"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model,
        )

    def _chat(self, messages:List, stream=False) -> Any:
        #print("--------------------------------------------")
        #import traceback
        #s=traceback.extract_stack()
        # print("%s %s invoke _chat" % (s[-2],s[-2][2]))
        # print(messages)
        # print("--------------------------------------------")
        response = self._get_client().chat.completions.create(
            model=self.model,  # 填写需要调用的模型名称
            messages=messages,
        )
        # print(f"_chat, response: {response}")
        return response

    #@llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        message_dicts: List = to_message_dicts(messages)
        response = self._chat(message_dicts, stream=False)
        # print(f"chat: {response} ")
        rsp = ChatResponse(
            message=ChatMessage(content=response.choices[0].message.content, role=MessageRole(response.choices[0].message.role),
                additional_kwargs= {}),
            raw=response, additional_kwargs= get_additional_kwargs(response),
        )
        print(f"chat: {rsp} ")

        return rsp

    #@llm_chat_callback()
    def stream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> CompletionResponseGen:
        response_txt = ""
        message_dicts: List = to_message_dicts(messages)
        response = self._chat(message_dicts, stream=True)
        # print(f"stream_chat: {response} ")
        for chunk in response:
            # chunk.choices[0].delta # content='```' role='assistant' tool_calls=None
            token = chunk.choices[0].delta.content
            response_txt += token
            yield ChatResponse(message=ChatMessage(content=response_txt,role=MessageRole(message.get("role")),
                                additional_kwargs={},), delta=token, raw=chunk,)

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        time.sleep(1)
        messages = [{"role": "user", "content": prompt}]
        # print(f"complete: messages {messages} ")
        try:
            response = self._chat(messages, stream=False)

            rsp = CompletionResponse(text=str(response.choices[0].message.content),
                                     raw=response,
                                     additional_kwargs=get_additional_kwargs(response),)
            # print(f"complete: {rsp} ")
        except Exception as e:
            print(f"complete: exception {e}")

        return rsp

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response_txt = ""
        messages = [{"role": "user", "content": prompt}]
        response = self._chat(messages, stream=True)
        # print(f"stream_complete: {response} ")
        for chunk in response:
            # chunk.choices[0].delta # content='```' role='assistant' tool_calls=None
            token = chunk.choices[0].delta.content
            response_txt += token
            yield CompletionResponse(text=response_txt, delta=token)
from typing import Any, List
from llama_index.core.embeddings import BaseEmbedding


class ChatGLMEmbeddings(BaseEmbedding):
    model: str = Field(default='embedding-2', description="The ChatGlM model to use. embedding-2")
    api_key: str = Field(default=None, description="The ChatGLM API key.")
    reuse_client: bool = Field(default=True, description=(
            "Reuse the client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    _client: Optional[Any] = PrivateAttr()
    def __init__(
        self,
        model: str = 'embedding-2',
        reuse_client: bool = True,
        api_key: Optional[str] = None,
        **kwargs: Any,
    )-> None:
        super().__init__(
            model=model,
            api_key=api_key,
            reuse_client=reuse_client,
            **kwargs,
        )
        self._client = None

    def _get_client(self) -> ZhipuAI:
        if not self.reuse_client :
            return ZhipuAI(api_key=self.api_key)

        if self._client is None:
            self._client = ZhipuAI(api_key=self.api_key)
        return self._client

    @classmethod
    def class_name(cls) -> str:
        return "ChatGLMEmbedding"

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        return self.get_general_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """The asynchronous version of _get_query_embedding."""
        return self.get_general_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        return self.get_general_text_embedding(text)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Asynchronously get text embedding."""
        return self.get_general_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get text embeddings."""
        embeddings_list: List[List[float]] = []
        for text in texts:
            embeddings = self.get_general_text_embedding(text)
            embeddings_list.append(embeddings)

        return embeddings_list

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Asynchronously get text embeddings."""
        return self._get_text_embeddings(texts)

    def get_general_text_embedding(self, prompt: str) -> List[float]:
        time.sleep(0.1)
        response = self._get_client().embeddings.create(
            model=self.model,  # 填写需要调用的模型名称
            input=prompt,
        )
        return response.data[0].embedding


if __name__ == '__main__':
    import gradio as gr
    import time

    # 后端处理函数，接受用户输入并返回处理后的输出
    def process_input(question, two):
        # return 'Test'
        # 在这里添加你的处理逻辑
        response = query_engine.query(question)
        return str(response)


    start = time.time()
    from llama_index.core import SimpleDirectoryReader
    from llama_index.core.llms import (
        CustomLLM,
        CompletionResponse,
        CompletionResponseGen,
        LLMMetadata,
    )
    from llama_index.core.llms.callbacks import llm_completion_callback
    from llama_index.core import Settings
    from llama_index.core import VectorStoreIndex

    ZHIPU_API_KEY = 'b3589487b559e0400ced55525f26f3c2.WdVen2vc1c9f9dNC'
    questions = ['各地关于优化政务服务有什么举措']
    # define our LLM
    print('Build Up LLM', time.time() - start)
    Settings.llm = ChatGLM(model='glm-4', reuse_client=True, api_key=ZHIPU_API_KEY, )

    # define embed model
    print('Build Up Embed Model', time.time() - start)
    Settings.embed_model = ChatGLMEmbeddings(model='embedding-2', reuse_client=True, api_key=ZHIPU_API_KEY, )

    # Load the your data
    # documents = SimpleDirectoryReader("./data").load_data()
    file_dir = '../data'
    print('Build Up Directory', time.time() - start)
    documents = SimpleDirectoryReader(file_dir).load_data()
    print('Build Up Vectory Index', time.time() - start)
    index = VectorStoreIndex.from_documents(documents)
    print('Getting response ....', time.time() - start)
    query_engine = index.as_query_engine()

    demo = gr.ChatInterface(process_input).queue()
    print('Gradio Launched:', time.time() - start)
    demo.launch()
    