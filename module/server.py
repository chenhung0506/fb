# -*- coding: utf-8 -*-
from flask import Flask
# from flask_cors import CORS
import log as logpy
import re
import os, sys
import const
import controller
import random
import controller_recaptcha
import controller_message
import controller_fb
#import controller_ccui
import flask_restful
import utils
import json
import service
import requests
import prometheus_client
from prometheus_client import Counter
from flask import Flask, request
from flask_restful import Api
from flask_restful import Resource
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, jsonify, Response
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pymessenger import Bot

utils.setLogFileName()
log = logpy.logging.getLogger(__name__)
app = Flask(__name__)

token = const.ACCESS_TOKEN_HERE

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)
      # log.info(data)
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      payload = {}
      if data['entry'][0]['messaging'][0].get('postback'):
        log.info(data['entry'][0]['messaging'][0]['postback'])
        payload = {'recipient': {'id': sender}, 'message': {'text': "請稍等客服將立即與您聯絡"}}
        # log.info(payload)
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
      elif data['entry'][0]['messaging'][0].get('message'):
        text = data['entry'][0]['messaging'][0]['message']['text'] 
        log.info(text)
        log.info(sender)


        reqUrl = "https://graph.facebook.com/v2.6/{USER_ID}?fields=name&access_token={PAGE_ACCESS_TOKEN}".format(USER_ID=sender, PAGE_ACCESS_TOKEN=const.ACCESS_TOKEN_HERE)
        log.info(reqUrl)
        r=requests.post(reqUrl)
        # 32215da1449203f95965a4bf6e26aa06
        log.info(r)

        payload = {'recipient': {'id': sender}, 'message': {'text': "您好,感謝您與我們聯繫!如有問題請您先參考下方智慧櫃檯功能選項："}}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        payload = {'recipient': {'id': sender}, 'message': json.loads(const.PAYLOAD)}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        payload = {'recipient': {'id': sender}, 'message': {"attachment":{"type":"template","payload":{"template_type":"button","text":"還有其他問題需要幫忙嗎？請點選下方按鈕由小幫手嗶寶協助您","buttons":[{"type":"web_url","url":"https://www.messenger.com","title":"小幫手嗶寶"}]}}}}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        # <img src="https://i.postimg.cc/y8zszNpM/bibo-icon.jpg">
        payload = {'recipient': {'id': sender}, 'message': {'text': "或是您可以撥打本公司客服中心：412-8880按1後再按7轉接專員(手機及金馬地區請加02)。"}}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)

    except Exception as e:
      log.error("post webhook error: "+utils.except_raise(e))
  elif request.method == 'GET': # For the initial verification
    log.info(request.args.get('hub.verify_token'))
    log.info(const.VERIFY_TOKEN_HERE)
    if request.args.get('hub.verify_token') == const.VERIFY_TOKEN_HERE:
      log.info(request.args.get('hub.challenge'))
      return request.args.get('hub.challenge')
    log.info('Wrong Verify Token')
    return "Wrong Verify Token"
  log.info('check token valid')
  return "Hello World" #Not Really Necessary


total_requests = Counter('request_count', 'Total webapp request count')

@app.route('/metrics')
def requests_count():
    total_requests.inc()
    return Response(prometheus_client.generate_latest(total_requests), mimetype='text/plain')

@app.route('/')
def index():
    total_requests.inc()
    return jsonify({
        'status': 'ok'
    })

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=const.PORT, debug=True)