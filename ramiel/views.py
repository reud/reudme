from linebot import LineBotApi, WebhookHandler
from django.http import HttpResponseForbidden, HttpResponse
from linebot.exceptions import InvalidSignatureError
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