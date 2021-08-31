import os
import random


from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, TextSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage, FollowEvent, MessageEvent,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton)


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


@handler.add(PostbackEvent)
def make_todo(event):
    a, b, c = "none"
    todo_list = [a, b, c]

    if event.postback.data == 'No.1':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="Setting No.1!")
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="Set onemoretime")
        )


@ handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    if event.message.text == "Todo":
        select_list = ["make", "check", "finish"]

        items = [QuickReplyButton(action=MessageAction(
            label=f"{select}", text=f"I want {select} Today's todo list")) for select in select_list]

        msg1 = TextSendMessage(text="What do you want to do?",
                               quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=msg1)

    elif event.message.text == "I want make Today's todo list":
        setting_list = ["No.1", "No.2", "No.3"]

        items = [QuickReplyButton(action=PostbackAction(
            label=f"{setting}", data=f"{setting}")) for setting in setting_list]

        msg2 = TextSendMessage(text="What do you want to do?",
                               quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=msg2)

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


# 友だち追加イベント

@ handler.add(FollowEvent)
def handle_follow(event):
    buttons_template = ButtonsTemplate(
        title='Hi！', text='Set up what you\'re going to do!!', actions=[
            PostbackAction(label='No.1', data='No.1'),
            PostbackAction(label='No.2', data='No.2'),
            PostbackAction(label='No.3', data='No.3')
        ])
    template_message = TemplateSendMessage(
        alt_text='Hi！\nSet up what you\'re going to do!!。', template=buttons_template)
    line_bot_api.reply_message(event.reply_token, template_message)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
