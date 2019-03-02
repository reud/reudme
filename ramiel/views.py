import datetime
import json
import os
import random
from socket import gethostname

import PyLineNotify
import requests
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
    docomo_api_key = setting_local.DOCOMO_API_KEY
    notifer = PyLineNotify.Notifer(notify_token=setting_local.LINE_NOTIFY_TOKEN)
else:
    line_bot_api = LineBotApi(channel_access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
    handler = WebhookHandler(channel_secret=os.environ['CHANNEL_SECRET'])
    docomo_api_key = os.environ['DOCOMO_API_KEY']
    notifer = PyLineNotify.Notifer(notify_token=os.environ['LINE_NOTIFY_TOKEN'])

# docomo api setting
docomo_communication_api_url = f'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY={docomo_api_key}'
docomo_user_register_api_url = f'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/registration?APIKEY={docomo_api_key}'
docomo_api_headers = {'Content-type': 'application/json', 'charset': 'UTF-8'}


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
    payload = {'botId': "Chatting", 'appKind': 'ramiel_project'}
    req = requests.post(docomo_user_register_api_url, data=json.dumps(payload), headers=docomo_api_headers)
    notifer.send_message(req)
    response = req.json()
    LINEUser.objects.create(username=profile.display_name, line_id=profile.user_id, app_id=response['appId'])
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'ようこそ！{profile.display_name}さん！')
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_object = LINEUser.objects.filter(line_id=profile.user_id).first()
    if user_object:
        payload = {'language': 'ja-JP',
                   'botId': 'Chatting',
                   'appId': user_object.app_id,
                   'voiceText': event.message.text,
                   'clientData': {
                       'option': {
                           "nickname": profile.display_name
                       }
                   },
                   "appRecvTime": "2019-03-02 22:22:22",
                   "appSendTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                   }
        # error point
        req = requests.post(docomo_communication_api_url, data=json.dumps(payload), headers=docomo_api_headers)
        notifer.send_message(req)
        res = req.json()
        print(res)
        make_vocabulary(line_id=profile.user_id, text=res['systemText']['expression'],
                        date_time=datetime.datetime.now() + datetime.timedelta(minutes=int(random.random() * 30)))
        return
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='DataBaseにあなたの名前がありません。友達追加をお手数ですが再度行って下さい。よろしくお願い致します。'))


def push_message_from_model(request):
    objects = Vocabulary.objects.filter(use_time__lte=timezone.now()).filter(state='WAITING').order_by(
        'use_time').first()
    if objects:
        post = objects
        check = post.serif.split('\n')
        if '<tag>' in check[0]:
            target = [check[0].replace('<tag>', '')]
            serifs = [check[i] for i in range(1, len(check))]
            serif = '\n'.join(serifs)
        elif post.author_line_id:
            target = [post.author_line_id]
            serif = post.serif
        else:
            target = [i.line_id for i in LINEUser.objects.all()]
            serif = post.serif
        message = TextSendMessage(text=serif)
        for i in target:
            print(f'{i} to {serif}')

            line_bot_api.push_message(i, messages=message)
        post.state = 'SENDED'
        post.save()

    return HttpResponse('OK', status=200)


def make_vocabulary(line_id: str, text: str, date_time: datetime.datetime):
    vocab_object = Vocabulary.objects.create(author_line_id=line_id, serif=text, use_time=date_time,
                                             state='WAITING')
    vocab_object.save()
