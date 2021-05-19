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
from flask import Flask, request
from flask_restful import Api
from flask_restful import Resource
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
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
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      payload = {'recipient': {'id': sender}, 'message': {'text': "Hello World"}} # We're going to send this back
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
    except Exception as e:
      log.info(e)
  elif request.method == 'GET': # For the initial verification
    log.indo(request.args.get('hub.verify_token'))
    log.indo(const.VERIFY_TOKEN_HERE)
    if request.args.get('hub.verify_token') == const.VERIFY_TOKEN_HERE:
      log.info(request.args.get('hub.challenge'))
      return request.args.get('hub.challenge')
    log.info('Wrong Verify Token')
    return "Wrong Verify Token"
  log.info('Hello World')
  return "Hello World" #Not Really Necessary

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=const.PORT, debug=True)