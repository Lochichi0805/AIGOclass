from line_bot_api import *
from urllib.parse import parse_qsl
import datetime

from extensions import db
from models.user import User
from models.reservation import Reservation


# 預約相關的功能都會寫在這裡
# 增加多個服務項目
# services = {
#     1:{
#         'category': '威士忌',
#         'img_url': 'https://twthedalmore.com/assets/img/products/classic/img_product_classic-11.webp',
#         'title': '大摩12年',
#         'duration': '12y',
#         'description': '表現出富含多變細緻的香氣與口感，是一支超越年份的經典酒款',
#         'price':2300,
#         'post_url': 'https://linecorp.com'
#     },
#     2:{
#         'category': '威士忌',
#         'img_url': 'https://twthedalmore.com/assets/img/products/classic/img_product_classic-09.webp',
#         'title': '大摩15年',
#         'duration': '15y',
#         'description': '代表滑順、豐富以及美好，完美呈現典型的大摩家族風格',
#         'price':4600,
#         'post_url': 'https://linecorp.com'
#     }
# }

# def service_category_event(event):
#     image_carousel_template_message = TemplateSendMessage(
#         alt_text = '請選擇想服務類別 ',
#         template = ImageCarouselTemplate(
#             columns = [
#                 ImageCarouselColumn(
#                     image_url = 'https://cdn.pixabay.com/photo/2022/12/15/14/21/generated-7657832_1280.jpg',
#                     action = PostbackAction(
#                         label = '威士忌',
#                         display_text = '想了解威士忌',
#                         data = 'action=service&category=威士忌'
#                     )
                
#                 )
#             ]
#         )
#     )
#     line_bot_api.reply_message(
#         event.reply_token,
#         [image_carousel_template_message]
#     )

services = {
    1: {
        'category': '按摩調理',
        'img_url': 'https://drive.google.com/uc?export=download&id=15ftd3m_rOX3Op_js9B5OCiz2a4KyQfXi',
        'title': '按摩調理（指壓／精油）',
        'duration': '90min',
        'description': '深層肌肉緊繃痠痛、工作壓力和緊繃情緒、身體疲勞者，想解除肌肉緊繃僵硬不適感',
        'price': 2000,
        'post_url': 'https://linecorp.com'
    },
    2: {
        'category': '按摩調理',
        'img_url': 'https://drive.google.com/uc?export=download&id=1naYV7ySDy1PBTR9_smzchSu3xPfuKRYO',
        'title': '運動按摩（按摩與伸展）',
        'duration': '90min',
        'description': '全身肌肉按摩放鬆與伸展，能夠改善運動後引發的延遲性痠痛，血液循環流通順暢',
        'price': 1500,
        'post_url': 'https://linecorp.com'
    },
    3: {
        'category': '按摩調理',
        'img_url': 'https://drive.google.com/uc?export=download&id=1dOiR8rnSski88B7s8tEClN6bR4OXP2VY',
        'title': '熱石精油紓壓',
        'duration': '90min',
        'description': '「火山石」成份含有豐富礦物質及獨特的自然能量，溫熱觸感能活絡循環，鬆解疲勞感，舒緩肌肉緊繃',
        'price': 2000,
        'post_url': 'https://linecorp.com'
    },
    4: {
        'category': '臉部護理',
        'img_url': 'https://drive.google.com/uc?export=download&id=1j9k2ivv1D3DwthQABmiI-PLsn6pN7sIZ',
        'title': '粉刺淨化 + 深層保濕',
        'duration': '90min',
        'description': '臉部淨化李，粉刺淨化 + 深層保濕繃',
        'price': 1500,
        'post_url': 'https://linecorp.com'
    },
}

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想服務類別',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://drive.google.com/uc?export=download&id=1UbeFJNmNF3PfPYDdoEEWPxZma5M82x-T',
                    action=PostbackAction(
                        label='按摩調理',
                        display_text='想了解按摩調理',
                        data='action=service&category=按摩調理'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://drive.google.com/uc?export=download&id=1-n-1HqfSsCJQmUhlYhPgWMowE6NTBDUR',
                    action=PostbackAction(
                        label='臉部護理',
                        display_text='想了解臉部護理',
                        data='action=service&category=臉部護理'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])
    


def service_event(event):

    data = dict(parse_qsl(event.postback.data))
    bubbles = []


    for service_id in services:
        if services[service_id]['category'] == data['category']:
            service = services[service_id]
            bubble = {
                "type": "bubble",
                "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": service['img_url']
                },
                "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": service['title'],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                    },
                    {
                    "type": "text",
                    "text": service['duration'],
                    "size": "md",
                    "weight": "bold"
                    },
                    {
                    "type": "text",
                    "text": service['description'],
                    "margin": "lg",
                    "wrap": True
                    },
                    {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                        "type": "text",
                        "text": f"NT$ {service['price']}",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0
                        }
                    ],
                    "margin": "xl"
                    }
                ]
                },
                "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "預約",
                        "data": f"action=select_date&service_id={service_id}",
                        "displayText": f"我想預約【{service['title']} {service['duration']}】"
                    },
                    "color": "#b28530"
                    },
                    {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "了解詳情",
                        "uri": service['post_url']
                    }
                    }
                ]
                }
            }

            bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text = '請選擇預約項目',
        contents = {
            "type": "carousel",
            "contents": bubbles
        }
    )

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message]
    )




def service_select_date_event(event):
    
    data = dict(parse_qsl(event.postback.data))

    weekday_string = {
        0:'一',
        1:'二',
        2:'三',
        3:'四',
        4:'五',
        5:'六',
        6:'日',
    }

    business_day = [1, 2, 3, 4, 5, 6]

    quick_reply_buttons = []

    today = datetime.datetime.today().date()

    for x in range(1,11):
        day = today + datetime.timedelta(days=x)

        if day.weekday() in business_day:
            quick_reply_button = QuickReplyButton(
                action = PostbackAction(label=f"{day}({weekday_string[day.weekday()]})",
                                        text=f"我要預約{day}({weekday_string[day.weekday()]})這天",
                                        data=f"action=select_time&service_id={data['service_id']}&date{day}")
            )
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(
        text = "請問要預約哪一天?",
        quick_reply = QuickReply(item=quick_reply_buttons)
      )
    
    line_bot_api.reply_message(
        event.reply_token,
        [text_message]
      )

def service_select_time_event(event):
    
    data = dict(parse_qsl(event.postback.data))

    available_time = ['11:00','14:00','17:00','20:00']

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_button = QuickReplyButton(
            action = PostbackAction(
                label=time,
                text=f'{time} 這個時段',
                data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'
            )
        )
        quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(
        text = "請問要預約哪個時段?",
        quick_reply = QuickReply(items=quick_reply_buttons)
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message]
    )

def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),#代表沒有被取消
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           #需要大於當下的時間.first()是會回傳第一筆資料
    if reservation:#text顯示預約項目名稱和服務時段
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False

def service_confirm_event(event):
    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])]

    confirm_template_message = TemplateSendMessage(
        alt_text="請確認預約項目",
        template=ConfirmTemplate(
                text=f'您即將預約\n\n{booking_service["title"]} {booking_service["duration"]}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',            actions=[
                PostbackAction(
                    label="確定",
                    display_text="確認沒問題!",
                    data=f"action=confirmed&service_id={data['service_id']}&data={data['data']}&time={'time'}"
                ),
                MessageAction(
                    label="重新預約",
                    text="我想重新預約",
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message]
    )



def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))

    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f"{data['date']}{data['time']}","%Y-%m-%d %H:%M")

    user = User.query.filter(User.line_id == event.source.user_id).first()
    if is_booked(event,user):
        return
    
    reservation = Reservation(
        user_id=user.id,
        booking_service_category=f"{booking_service['category']}",
        booking_service=f"{booking_service['title']}{booking_service['duration']}",
        booking_datetime=booking_datetime
    )

    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text="沒問題! 感謝您的預約，我已經幫您預約成功了喔，到時候見!")]
    )