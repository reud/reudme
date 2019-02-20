import os

from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent, TextSendMessage, MessageEvent, TextMessage
)
from socket import gethostname

if 'charlotte.local' in gethostname():
    from ramiel import setting_local

    line_bot_api = LineBotApi(channel_access_token=setting_local.CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(channel_secret=setting_local.CHANNEL_SECRET)

else:
    line_bot_api = LineBotApi(channel_access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
    handler = WebhookHandler(channel_secret=os.environ['CHANNEL_SECRET'])



@csrf_exempt
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
