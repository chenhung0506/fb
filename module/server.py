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
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, jsonify
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
      log.info(data)
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      log.info(text)
      log.info(sender)
      payload = {'recipient': {'id': sender}, 'message': json.loads(const.PAYLOAD)}
    #   payload = {'recipient': {'id': sender}, 'message': {'text': "Hello World"}}
      log.info(payload)
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
    except Exception as e:
      log.info(e)
  elif request.method == 'GET': # For the initial verification
    log.info(request.args.get('hub.verify_token'))
    log.info(const.VERIFY_TOKEN_HERE)
    if request.args.get('hub.verify_token') == const.VERIFY_TOKEN_HERE:
      log.info(request.args.get('hub.challenge'))
      return request.args.get('hub.challenge')
    log.info('Wrong Verify Token')
    return "Wrong Verify Token"
  log.info('Hello World')
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