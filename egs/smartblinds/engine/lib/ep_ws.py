from tornado.web import RequestHandler#, authenticated
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado.escape import url_escape, url_unescape, json_encode
from os.path import dirname, join as join_path

from requests.exceptions import HTTPError

import os
import json
from urllib.parse import urlparse, parse_qs

from pymfy.api.devices.blind import Blind
from pymfy.api.somfy_api import SomfyApi
from pymfy.api.devices.category import Category
from pymfy.api.error import QuotaViolationException

from paho.mqtt.publish import single as mqtt_publish

# from ppauth import PPAuth

import logging

import datetime as dt

logging.basicConfig(level=logging.DEBUG)

# class UserHandler(RequestHandler):
#     def get_current_user(self):
#         return self.get_secure_cookie("user")


# class MainHandler(UserHandler):
#     @authenticated
#     def get(self):
#         #logging.info(self.ws_somfy.site_id.id)
#         #self.write(str(self.ws_somfy.site_id.id))

#         output = ""

#         try:
#             device = self.ws_somfy.api.get_device(self.ws_somfy.cfg["somfy"]["blind_id"])
#         except QuotaViolationException:
#             self.send_error(reason="Byla překročena četnost požadavků na API. Opakujte pokus za alespoň 1 minutu.")
#         except HTTPError as e:
#             logging.warn("Get device error:" + str(e))
#             self.send_error(reason="Nastal problém při navazování spojení s API. Původní chyba: " + str(e))
#         except:
#             self.redirect("/apiauth")
#             return

#         self.ws_somfy.cover = Blind(device, self.ws_somfy.api)

#         output = "Cover {} has the following position: {}".format(self.ws_somfy.cover.device.name, self.ws_somfy.cover.get_position())
#         print(output)

#         self.render("./static/index.html")

# class LoginHandler(UserHandler):
#     def get(self):
#         if self.current_user:
#             self.redirect(self.get_argument("next", "/"))
#             return
#         self.render("./static/login.html", next=self.get_argument("next","/"))

#     def post(self):
#         username = self.get_argument("username", "")
#         password = self.get_argument("password", "")
#         auth = self.ws_somfy.auth.authenticate(username, password)
#         if auth:
#             self.set_current_user(username)
#             self.redirect(self.get_argument("next", u"/"))
#         else:
#             self.redirect(u"/login?error=1")

#     def set_current_user(self, user):
#         if user:
#             self.set_secure_cookie("user", json_encode(user))
#         else:
#             self.clear_cookie("user")

# class LogoutHandler(RequestHandler):

#     def get(self):
#         self.clear_cookie("user")
#         self.redirect(u"/login")

# class AuthHandler(UserHandler):
#     #@authenticated
#     def get(self):
#         client_id = self.ws_somfy.cfg["somfy"]["client_id"]  # Consumer Key
#         redir_url = self.ws_somfy.cfg["somfy"]["redir_url"]  # Callback URL (for testing, can be anything)
#         secret = self.ws_somfy.cfg["somfy"]["secret"]  # Consumer Secret

#         # code = self.get_query_argument("code", default=None)
#         # print(code)
#         token = self.ws_somfy.get_token()
#         self.ws_somfy.api = SomfyApi(client_id, secret, redir_url, token=token, token_updater=self.ws_somfy.set_token)
        
#         if token is None:
#             # if not code is None:
#             #     self.ws_somfy.set_token(self.ws_somfy.api.request_token(code=code))
#             # else:
#             #     authorization_url, _ = self.ws_somfy.api.get_authorization_url()
#             #     self.redirect(authorization_url)
#             self.send_error(reason="Somfy API token is not specified")
#         # self.redirect("/")


class EP_WS(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def initialize(self, ws_somfy):
        self.ws_somfy = ws_somfy
        self.ws_somfy.ws_clients.append(self)
        print('Webserver: New WS Client. Connected clients:', len(self.ws_somfy.ws_clients))

        if len(self.ws_somfy.ws_clients) == 1:
            self.ws_somfy.apiauth(self)
            try:
                device = self.ws_somfy.api.get_device(self.ws_somfy.cfg["somfy"]["blind_id"])
            except QuotaViolationException:
                self.send_error(reason="Byla překročena četnost požadavků na API. Opakujte pokus za alespoň 1 minutu.")
                logging.error("Quota violated.")
            except HTTPError as e:
                logging.error("Get device error:" + str(e))
                self.send_error(reason="Nastal problém při navazování spojení s API. Původní chyba: " + str(e))
            except Exception as e:
                logging.error("Exception occured during get_device:" + str(e))
                self.send_error(reason="Exception occured during get_device:" + str(e))
                return

            self.ws_somfy.cover = Blind(device, self.ws_somfy.api)

    def open(self):
        # if not self.current_user:
        #     self.try_send_message("Not logged in, good bye")
        #     self.close()
        #     return
        print('Webserver: Websocket opened.')
        if len(self.ws_somfy.ws_clients) == 1:
            self.ws_somfy.iol.spawn_callback(self.ws_somfy.update_device)
            self.ws_somfy.testmode(True)
        self.write_message('Server ready.')

    def try_send_message(self, content):
        try:
            self.write_message(content)
        except Exception as err:
            logging.error("E: WS error: Can't send data")
            logging.error(str(err))
            if self in self.ws_somfy.ws_clients:
                self.ws_somfy.ws_clients.remove(self)
            self.close()

    def on_message(self, msg):
        try:
            msg = json.loads(msg)
            print('Webserver: Received json WS message:', msg)
            pos = msg.get("position")
            if(not pos is None):
                self.ws_somfy.cover.set_position(value=int(pos))
            tlt = msg.get("tilt")
            if(not tlt is None):
                self.ws_somfy.cover.orientation = int(tlt)
            mode = msg.get("testing")
            if(not mode is None):
                self.ws_somfy.testmode(mode)
                self.ws_somfy.send_ws_message(json.dumps({"testing": mode}))
                logging.info("Setting test mode to %s", str(mode))
        except (ValueError):
            print('Webserver: Received WS message:', msg)

    def on_close(self):
        self.ws_somfy.ws_clients.remove(self)
        if(len(self.ws_somfy.ws_clients)==0):
            self.ws_somfy.iol.remove_timeout(self.ws_somfy.tohandle)
            self.ws_somfy.testmode(False)
        print('Webserver: Websocket client closed. Connected clients:', len(self.ws_somfy.ws_clients))

class WS_Somfy:

    def __init__(self, cfg):
        self.ws_clients = []
        self.cfg = cfg
        self.site_id = None
        self.api = None
        self.cover = None
        self.iol = None

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "GET")

    def setIOL(self, iol):
        self.iol = iol

    def apiauth(self, client):
        client_id = self.cfg["somfy"]["client_id"]  # Consumer Key
        redir_url = self.cfg["somfy"]["redir_url"]  # Callback URL (for testing, can be anything)
        secret = self.cfg["somfy"]["secret"]  # Consumer Secret

        # code = self.get_query_argument("code", default=None)
        # print(code)
        token = self.get_token()
        self.api = SomfyApi(client_id, secret, redir_url, token=token, token_updater=self.set_token)
        
        if token is None:
            # if not code is None:
            #     self.set_token(self.api.request_token(code=code))
            # else:
            #     authorization_url, _ = self.api.get_authorization_url()
            #     self.redirect(authorization_url)
            client.send_error(reason="Somfy API token is not specified")
        # self.redirect("/")

    def send_blind_state(self, message):
        if len(self.ws_clients)>0:
            self.tohandle = self.iol.add_timeout(dt.timedelta(seconds=self.cfg["somfy"]["refresh_period"]), self.update_device)
        self.send_ws_message(message)

    def send_ws_message(self, message):
        for client in self.ws_clients:
            self.iol.spawn_callback(client.write_message, json.dumps(message))

    def get_token(self):
        try:
            with open(self.cfg["somfy"]["cache_path"], "r") as cache:
                return json.loads(cache.read())
        except IOError:
            pass

    def set_token(self, token) -> None:
        with open(self.cfg["somfy"]["cache_path"], "w") as cache:
            cache.write(json.dumps(token))

    def disconnect_clients(self):
        for client in self.ws_clients:
            self.iol.spawn_callback(client.close)

    def update_device(self):
        try:
            self.cover.refresh_state()
            position = self.cover.get_position()
            tilt = self.cover.orientation

            message = {"position": position, "tilt": tilt}

            self.send_blind_state(message)
        except HTTPError as e:
            logging.warn("update device error:" + str(e))
        except AttributeError:
            self.disconnect_clients()

    def testmode(self, mode):
        mqtt_publish(self.cfg["somfy"]["mqtt"]["topic"], json.dumps({"id": "testing", "value": mode}), hostname=self.cfg["somfy"]["mqtt"]["host"], auth=self.cfg["somfy"]["mqtt"]["auth"])