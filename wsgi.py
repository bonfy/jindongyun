# -*- coding: utf-8 -*-
from flask import Flask
from flask_weixin import Weixin

app = Flask(__name__)
app.secret_key = 'secret'
app.config['WEIXIN_TOKEN'] = 'nevertellyou'

weixin = Weixin(app)
app.add_url_rule('/', view_func=weixin.view_func)


jing_music = (
    'http://cc.cdn.jing.fm/201310171130/19e715ce8223efd159559c15de175ab6/'
    '2012/0428/11/AT/2012042811ATk.m4a'
)


@weixin('*')
def reply_all(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)

    eventType = kwargs.get('event', '')

    cmd = ''

    for (key,value) in kwargs.items():
        cmd = cmd + '\nkey: ' + key
        cmd = cmd + '\nvalue:' + str(value)

    
    if content == 'event':
        WelcomeMsg = '欢迎关注Shrimp，你老婆也爱吃虾?\n回复：M 收听音乐\n回复：N 查看新闻\n用户：'+ username +'\n发送:' + sender +'\nMessage:'+eventType+cmd
        return weixin.reply(
            username, sender=sender, content=WelcomeMsg
        )

    elif content == 'M':
        return weixin.reply(
            username, type='music', sender=sender,
            title='Weixin Music',
            description='weixin description',
            music_url=jing_music,
            hq_music_url=jing_music,
        )
    elif content == 'N':
        return weixin.reply(
            username, type='news', sender=sender,
            articles=[
                {
                    'title': 'Weixin News',
                    'description': 'weixin description',
                    'picurl': '',
                    'url': 'http://blog.bonfy.im/',
                }
            ]
        )
    else:
        return weixin.reply(
            username, sender=sender, content=content
        )


if __name__ == '__main__':
    # you need a proxy to serve it on 80
    app.run()