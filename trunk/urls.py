# -*- coding: utf-8 -*-
import webapp2

routes = [
    webapp2.Route(r'/', 'pixmicat-gae.main.MainPage', name='main'),
    #webapp2.Route(r'/<page_num:\d+>/', 'main.MainPage'),
    #webapp2.Route(r'/reply/', 'reply.ReplyPage'),
    #webapp2.Route(r'/reply/<res:\d+>/', 'reply.ReplyPage'),
    #webapp2.Route(r'/reply/<res:\d+>/<page_num>/', 'reply.ReplyPage'),
]