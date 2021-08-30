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
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    UserｓのActivityによって条件分岐。
    noneQuestionがデフォルト→メニューを表示。
    waitQestionが質問待ち状態→次に入力されたテキストが質問になる。
    """
    UserID = event.source.user_id
    text = event.message.text
    activity = users_DB.checkActivity(UserID)

    if activity == "noneQuestion":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='メニュー',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                label="異性に質問してみる", data="異性に質問してみる")
                        ),
                        QuickReplyButton(
                            action=PostbackAction(
                                label="誰かの質問に答える", data="誰かの質問に答える")
                        ),
                    ])))
    else:
        QuestionKey = activity
        questions.putAnswer(UserID, text, QuestionKey)
        users_DB.changeActivity(UserID, "waitAnswer")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=text + "をあなたの回答として投稿しました",
                quick_reply=QuickReply(
                    items=[
                            QuickReplyButton(
                                action=PostbackAction(
                                    label="自分への回答を確認する", data="回答を確認する")
                            ),
                        QuickReplyButton(
                                action=PostbackAction(
                                    label="誰かの質問に答える", data="誰かの質問に答える")
                            ),
                        QuickReplyButton(
                                action=PostbackAction(
                                    label="質問をする", data="異性に質問してみる")
                            ),
                    ])))

    return "ok"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
