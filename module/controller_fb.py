# coding=UTF-8
import requests
import json
import time
import logging 
import threading
from datetime import datetime
from flask import Flask, Response, render_template, request, redirect, jsonify, send_from_directory, url_for, make_response
from threading import Timer,Thread,Event
from flask_restful import Resource
import const
import utils
import log as logpy
from urllib.parse import urlencode
from urllib.request import urlopen
from pymessenger import Bot

log = logpy.logging.getLogger(__name__)
PAGE_ACCESS_TOKEN = "EAAFNM3mDiKcBADHgSM1pE9iK8SElLsjwffYu4dahFs8EYTXI4lYKFx7s9zyIuQTEFHeG2a6vLdzBRZAzegp7AtSFD61iVVSzjPMyimqmzTSWLH2R3fOglZCyh7DG8IccP8l98ZAdX3yuZCtiZCRZAQ18Cph7PilwxQ2FweLXS1Bzr2LRHKFb1q"
bot = Bot(PAGE_ACCESS_TOKEN)


# https://stackoverflow.com/questions/46393162/how-to-validate-a-recaptcha-response-server-side-with-python
# https://codesandbox.io/s/n3p4y?file=/src/App.vue

def setup_route(api):
    api.add_resource(Verify, '/')

class Verify(Resource):
    def post(self):
        try:
            data = request.get_json()
            log.info(data)
            if data['object'] == 'page':
                for entry in data['entry']:
                    for messaging_event in entry['messaging']:
                        sender_id = messaging_event['sender']['id']
                        recipient_id = messaging_event['recipient']['id']
            if messaging_event.get('message'):
                if 'text' in messaging_event['message']:
                    messaging_text = messaging_event['message']['text']
            else:
                messaging_text = 'no text'
                response = messaging_text
                bot.send_text_message(sender_id, messaging_text)
            return "ok", 200
        except Exception as e:
            log.error("Recaptcha error: "+utils.except_raise(e))

    def get(self):
        try:
            # Webhook verification
            if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
                if not request.args.get("hub.verify_token") == "EAAFNM3mDiKcBADHgSM1pE9iK8SElLsjwffYu4dahFs8EYTXI4lYKFx7s9zyIuQTEFHeG2a6vLdzBRZAzegp7AtSFD61iVVSzjPMyimqmzTSWLH2R3fOglZCyh7DG8IccP8l98ZAdX3yuZCtiZCRZAQ18Cph7PilwxQ2FweLXS1Bzr2LRHKFb1q":
                    return "Verification token mismatch", 403
                return request.args["hub.challenge"], 200
            return "Hello world", 200

        except Exception as e:
            log.error("Recaptcha error: "+utils.except_raise(e))
      