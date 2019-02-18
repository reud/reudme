from linebot import LineBotApi, WebhookHandler
from django.http import HttpResponseForbidden, HttpResponse
from linebot.exceptions import InvalidSignatureError
import os
# 各クライアントライブラリのインスタンス作成
line_bot_api = LineBotApi(channel_access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(channel_secret=os.environ['CHANNEL_SECRET'])

def callback(request):
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    # リクエストボディを取得
    body = request.body.decode('utf-8')
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名検証で失敗したときは例外をあげる
        HttpResponseForbidden()
    # handleの処理を終えればOK
    return HttpResponse('OK', status=200)