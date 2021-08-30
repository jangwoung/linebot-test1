from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom, ImageSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort
import os
import random
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
def handle_message(event):

    if event.message.text == "Todo":
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
        message = event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
