import os
from socket import gethostname

from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent, TextSendMessage, MessageEvent, TextMessage
)

from ramiel.models import LINEUser, Vocabulary

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
    profile = line_bot_api.get_profile(event.source.user_id)
    LINEUser.objects.create(username=profile.display_name, line_id=profile.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'ようこそ！{profile.display_name}さん！')
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


def push_message_from_model(request):
    objects = Vocabulary.objects.filter(use_time__lte=timezone.now()).filter(state='WAITING').order_by(
        'use_time').first()
    if objects:
        post=objects
        check=post.serif.split('\n')
        if '<tag>' in check[0]:
            target=[check[0].replace('<tag>','')]
            serifs=[check[i] for i in range(1,len(check))]
            serif='\n'.join(serifs)
        else:
            target=[i.line_id for i in LINEUser.objects.all()]
            serif=post.serif
        messages = TextSendMessage(text=serif)
        for i in target:
            print(f'{i} to {serif}')

            line_bot_api.push_message(i,messages=messages)
        post.state='SENDED'
        post.save()

    return HttpResponse('OK', status=200)


