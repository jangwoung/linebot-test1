from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage
import os
import random

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage, FollowEvent, FlexSendMessage)

app = Flask(__name__)
num = 0

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def response_message(event):

    if event.message.text == "Todo":
        with open('./saisyohaguu_message.json') as f:
            aisyohaguu_message = json.load(f)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message)
        )

    elif event.message.text == "Go":
        buttons_template = ButtonsTemplate(
            title='友達追加ありがとう！', text='まず、あなたの性別を教えてください!', actions=[
                PostbackAction(label='男', data='male'),
                PostbackAction(label='女', data='female'),
            ])
        template_message = TemplateSendMessage(
            alt_text='友達追加ありがとう！\nまず、あなたの性別を教えてください。', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif event.message.text == "I want make Today's todo list":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please enter what you want to do Today!"))
        a = event.message.text
        make_todo(a)

    elif event.message.text == "I want check Today's todo list":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Todo"))

    elif event.message.text == "I want finish Today's todo list":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Todo"))

    else:
        message = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please enter\"Todo\""))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
