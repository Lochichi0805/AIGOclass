from line_bot_api import *
from urllib.parse import parse_qsl
import datetime

from extensions import db
from models.user import User
from models.reservation import Reservation


# 預約相關的功能都會寫在這裡
# 增加多個服務項目
services = {
    1:{
        'category': '威士忌',
        'img_url': 'https://twthedalmore.com/assets/img/products/classic/img_product_classic-11.webp',
        'title': '大摩12年',
        'duration': '12y',
        'description': '表現出富含多變細緻的香氣與口感，是一支超越年份的經典酒款',
        'price':2300,
        'post_url': 'https://linecorp.com'
    },
    2:{
        'category': '威士忌',
        'img_url': 'https://twthedalmore.com/assets/img/products/classic/img_product_classic-09.webp',
        'title': '大摩15年',
        'duration': '15y',
        'description': '代表滑順、豐富以及美好，完美呈現典型的大摩家族風格',
        'price':4600,
        'post_url': 'https://linecorp.com'
    },
}

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
        content = {
            "type": "carousel",
            "contents": bubbles
        }
    )

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message]
    )


def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text = '請選擇想服務類別 ',
        template = ImageCarouselTemplate(
            columns = [
                ImageCarouselColumn(
                    image_url = 'https://cdn.pixabay.com/photo/2022/12/15/14/21/generated-7657832_1280.jpg',
                    action = PostbackAction(
                        label = '威士忌',
                        display_text = '想了解威士忌',
                        data = 'action=service&category=威士忌'
                    )
                
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message]
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
        quick_reply_buttons = QuickReplyButton(
            action = PostbackAction(
                label=time,
                text=f'{time} 這個時段',
                data=f'action=confirm&service_id={data["service_id"]}&data={data["data"]}&time={time}'
            )
        )
        quick_reply_buttons.append(quick_reply_buttons)

    text_message = TextSendMessage(
        text = "請問要預約哪個時段?",
        quick_reply = QuickReply(item=quick_reply_buttons)
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message]
    )

