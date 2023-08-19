# pip install line-bot-sdk
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, StickerSendMessage, ImageSendMessage, LocationSendMessage,
    FlexSendMessage,TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,PostbackAction,QuickReplyButton,QuickReply,PostbackEvent,
    ConfirmTemplate,MessageAction,ButtonsTemplate
)

line_bot_api = LineBotApi('AXAFsb6qiU4YdzrJt8wJYbCUbw15nA7hH4TPAbYokGse1isE2WelFQ8Wbae3azf8ZF1CwSUKkLNbA/A8CfSQzUVjzvwv/09T5U9XaKv+tqk084NxVgomnqmyr/PYNdXnbeYlJp/NVkcvREuYQHtgQAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('14850b57fa56d80e8ff6ef777a9b11e2')