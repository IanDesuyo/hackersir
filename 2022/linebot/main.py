from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    StickerMessage,
    ImageMessage,
    TextSendMessage,
    ImageSendMessage,
    StickerSendMessage,
)
import random

# 定義金鑰
CHANNEL_SECRET = ""
CHANNEL_ACCESS_TOKEN = ""

# 建立 Flask 及 LineBot instance
app = Flask("LineBot")
line_bot = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 定義路由
@app.get("/")
def index():
    return "Hello World"


@app.post("/callback")
def callback():
    # 獲取簽章
    signature: str = request.headers["X-Line-Signature"]

    # 獲取請求內容
    body: str = request.get_data(as_text=True)
    print(body)

    # 處理事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 若請求內的簽章與計算結果不符則報錯
        return "Invalid signature.", 400

    return "OK"


# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    # 獲取使用者發送的訊息
    msg: str = event.message.text

    if msg == "你好":
        # 回覆訊息
        line_bot.reply_message(event.reply_token, TextSendMessage(text="Hello"))

    elif "吃什麼" in msg:
        # 記得 import random
        choice = random.choice(
            ["蒔樂咖哩", "咖啡熊", "六堆伙房", "九湯屋", "香港極品燒臘快餐", "鐵拳", "新揚州炒飯", "喜園食堂", "司覓達(便當)", "餃餃者", "豐成麵館", "麻塔"]
        )
        line_bot.reply_message(event.reply_token, TextSendMessage(text=choice))

    else:
        # 回覆原訊息
        line_bot.reply_message(event.reply_token, TextSendMessage(text=msg))

    return "OK"


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event: MessageEvent):
    # 獲取使用者資訊
    user_id: str = event.source.user_id

    user = line_bot.get_profile(user_id)

    # 回覆訊息
    line_bot.reply_message(
        event.reply_token,
        [
            TextSendMessage(text=f"你好 {user.display_name}"),
            ImageSendMessage(f"{user.picture_url}/large", f"{user.picture_url}/small"),
            StickerSendMessage(package_id=11537, sticker_id=52002734),
        ],
    )

    return "OK"


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event: MessageEvent):
    # 獲取訊息 ID
    message_id: str = event.message.id

    # 透過 API 獲取圖片
    image = line_bot.get_message_content(message_id).content

    # 保存到電腦
    with open(f"{message_id}.png", "wb+") as f:
        f.write(image)

    line_bot.reply_message(event.reply_token, TextSendMessage(text=f"以儲存至 {message_id}.png"))

    return "OK"


# 程式執行時啟動伺服器
if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)
