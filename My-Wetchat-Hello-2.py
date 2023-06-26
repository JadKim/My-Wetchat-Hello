from flask import Flask, request
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
import openai

# 设置你的Token、AppID和AppSecret
TOKEN = "JadKim"
APPID = "wxd030e69d3c85b0f1"
APPSECRET = "cdca2cc21d24672970ee7617e4122f3d"

# 设置ChatGPT的API密钥和模型引擎
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
MODEL_ENGINE = "gpt-3.5-turbo"  # 替换为你选择的ChatGPT模型引擎

app = Flask(__name__)

# 定义路由用于接收和处理微信消息
@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证消息的签名，用于验证身份
        try:
            check_signature(TOKEN, request.args.get('signature', ''),
                            request.args.get('timestamp', ''),
                            request.args.get('nonce', ''))
        except InvalidSignatureException:
            return 'Invalid signature', 400
        return request.args.get('echostr', '')
    elif request.method == 'POST':
        # 处理接收到的微信消息
        xml = request.data
        msg = parse_message(xml)

        # 仅处理文本消息类型
        if msg.type == 'text':
            # 获取用户发送的文本消息内容
            user_message = msg.content.strip()

            # 判断用户输入是否为空
            if user_message:
                # 使用ChatGPT获取回答
                response = openai.Completion.create(
                    engine=MODEL_ENGINE,
                    prompt=user_message,
                    max_tokens=50  # 设置生成回答的最大长度
                )
                answer = response.choices[0].text.strip()

                # 构建回复消息
                reply = create_reply(answer, msg)
            else:
                # 用户输入为空时的提示
                reply = create_reply('输入信息无效，请重新输入。', msg)
        else:
            # 非文本消息类型的处理
            reply = create_reply('输入信息无效，请重新输入。', msg)

        return reply.render()

    return 'OK'

if __name__ == '__main__':
    app.run()
