import json
import ollama.client as client
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import (
    PromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate
)
import os
from langchain_core.messages import AIMessage,SystemMessage, HumanMessage
from langchain.schema import SystemMessage, HumanMessage

def LLMPrompt(prompt: str, metadata={}, model="zephyr:latest"):
    if model == None:
        model = "zephyr:latest"
    print("==  zephyr start  ==")
    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
        "请用中文直接地、简洁地回答以下问题,回答中不要包含任何英文："
    )


    USER_PROMPT = f"问题如下： {prompt} "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)

    return response


os.environ['OPENAI_API_BASE'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
DASHSCOPE_API_KEY= "sk-31ed7f23b2cc4ca9959e37bbf7259b64"
llm = chat_model = ChatOpenAI(model="qwen2-57b-a14b-instruct", api_key=DASHSCOPE_API_KEY,openai_api_base = os.environ['OPENAI_API_BASE'], max_tokens=2000)



conversation_history = []

def TYgraphPrompt(prompt: str, metadata={}, model="qwen2-57b-a14b-instruct"):
    # 系统提示词
    SYS_PROMPT = "你是一个提供中文简洁答案的助手。请尽量简短地回答以下问题："
    conversation_history.append(HumanMessage(content=prompt))
    # 定义聊天提示模板，包括对话历史的占位符
    prompt_template = ChatPromptTemplate(
        messages=[
            SystemMessage(content=SYS_PROMPT),
        ] + conversation_history  # 将对话历史传递给模板
    )


    # 创建一个运行序列（管道）
    chain = prompt_template | llm

    try:
        # 使用链条生成响应，并传递对话历史
        response = chain.invoke({"input": prompt})

        # 处理响应
        if isinstance(response, AIMessage):
            content = response.content
            conversation_history.append(AIMessage(content=content))  # 保存 AI 的回复到对话历史
            return content
        else:
            return None
    except Exception as e:
        print("\n\nERROR ### Here is the buggy response: ", e, "\n\n")
        return None

# 测试上下文问答功能
print(TYgraphPrompt("请介绍一下上海有什么好玩的地方"))
print(1)

# 添加后续用户问题并获取回应
print(TYgraphPrompt("能否缩短一些，只讲三点"))


print(conversation_history)










def TYgraphPrompt1(prompt: str, metadata={}, model="qwen2-57b-a14b-instruct"):
    SYS_PROMPT = (
        "你是一个提供中文简洁答案的助手,请用中文直接地、简洁地回答以下问题,回答时尽可能的短一些：{input}" 
    )

    A_prompt = PromptTemplate(
        template=SYS_PROMPT,
        input_variables=["input"],
    )

    chain = chain = A_prompt | llm  # 创建一个运行序列（管道）

    response = chain.invoke({"input": prompt})
    try:
       
        content = response.content  # 获取 AIMessage 的 content 属性
        return content
    except:
        print("\n\nERROR ### Here is the buggy response: ", "\n\n")
        result = None
        return result