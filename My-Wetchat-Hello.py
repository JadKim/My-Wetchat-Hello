from flask import Flask, request
import xmltodict
from wechatpy import WeChatClient
from wechatpy.replies import TextReply
import openai

app = Flask(__name__)

# ChatGPT模型设置
openai.api_key = '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'  # 替换为你的OpenAI API密钥
model_name = 'gpt-3.5-turbo'  # 替换为你选择的ChatGPT模型引擎


@app.route('/callback', methods=['POST'])
def callback():
    data = request.data
    xml_data = xmltodict.parse(data)
    message_type = xml_data['xml']['MsgType']
    if message_type == 'text':
        user_message = xml_data['xml']['Content']
        reply = generate_chat_response(user_message)
    else:
        reply = "无效输入，请输入纯文本内容。"

    reply_xml = send_reply(reply, xml_data['xml'])
    return reply_xml


def generate_chat_response(message):
    response = openai.Completion.create(
        engine=model_name,
        prompt=message,
        max_tokens=50
    )
    return response.choices[0].text.strip()


def send_reply(reply_text, message_data):
    client = WeChatClient("wxd030e69d3c85b0f1", "cdca2cc21d24672970ee7617e4122f3d")  # 替换为你的AppID和AppSecret
    reply = TextReply(content=reply_text, message=message_data)
    reply_xml = reply.render()
    return reply_xml


if __name__ == '__main__':
    app.run()

