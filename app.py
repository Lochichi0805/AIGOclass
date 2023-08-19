from flask import Flask, request, abort

from events.basic import *
from events.service import *
from line_bot_api import *
import os
from extensions import db,migrate
from events.admin import *
from models.user import User

app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTING','config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:zWHtLA4ywiKaUSLjSLPlo6mG2o4n62hq@dpg-cjg2seb6fquc73amcjs0-a.singapore-postgres.render.com/aigodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    message_text = str(event.message.text).lower()

    user = User.query.filter(User.line_id == event.source.user_id).first()

    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)
        print(profile.display_name)
        print(profile.user_id)
        print(profile.picture_url)

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    print(user.line_id)
    print(user.display_name)

    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)

    elif message_text == '@預約服務':
        service_category_event(event)
    
    elif message_text.startswith('*'):
        if event.source.user_id not in ["U72a5bfd4648cece9e05d94fd3227bc8f"]:
            return
        if message_text in ["*data","*d"]:
            list_reservation_event(event)


@handler.add(PostbackEvent)
def handler_postback(event):
    data = dict(parse_qsl(event.postback.data))
    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_data':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
        

@handler.add(PostbackAction)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))
    if data.get('action') == 'service':
        service_event(event)


@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """Hello! 您好，歡迎您成為 Master SPA 的好友！

我是Master SPA的小幫手 

-想預約按摩/臉部淨化護理服務都可以直接跟我互動喔~
-直接點選下方【歡迎光臨專屬您的SPA】選單功能

-期待您的光臨！"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)



if __name__ == "__main__":
    app.run()
