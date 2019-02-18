from linebot import LineBotApi, WebhookHandler
from django.http import HttpResponseForbidden, HttpResponse
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent, TextSendMessage
)
import os
line_bot_api = LineBotApi(channel_access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(channel_secret=os.environ['CHANNEL_SECRET'])

def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'こんにちはようこそ！{event}')
    )