from dialog import SpeechCloudWS, Dialog, ABNF_INLINE
import random
import asyncio
import logging
from pprint import pprint, pformat
from collections import Counter

from threading import Thread, ThreadError
from abc import abstractmethod
import socket


class VoicehomeController:

    def __init__(self):

        # Parse args and load config
        self.host = '192.168.10.8'
        self.port = 7010

        self.sock = None
        self.disconnected = False
        self.replies = []
        self.commands = []

        self.controller_id = ''

        try:
            t = Thread(target=self.connect_and_listen)
            t.setDaemon(False)
            t.start()
        except ThreadError:
            print('ERR: Thread Controller Listener.')

    def connect_and_listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        # handshake - log self
        self.sock.sendall(str.encode('controller_handshake_id_' + self.controller_id))

        while not self.disconnected:
            try:
                self.replies.append(self.sock.recv(1024).decode())
                self.new_reply()
            except OSError:
                pass

    def last_reply(self):
        return self.replies[-1]

    def last_command(self):
        return self.commands[-1]

    def new_reply(self):
        if self.last_reply():
            if self.last_reply() == 'exit':
                self.disconnect_controller()

            self.got_reply(self.last_reply())
        else:
            self.disconnect_controller()

    def new_command(self, command):
        self.commands.append(command)
        self.sock.sendall(str.encode(command))
        if self.last_command() == 'exit':
            self.disconnect_controller()

    def disconnect_controller(self):
        self.disconnected = True
        self.sock.close()
        print('Controller disconnected.')
        os._exit(0)

    @abstractmethod
    def got_reply(self, reply):
        pass


class VoiceKitController(VoicehomeController):

    def __init__(self, sc_dialog):
        VoicehomeController.__init__(self)
        self.controller_id = 'voicekit'

        self.sc = sc_dialog
        self.loop = asyncio.get_event_loop()

        self.voice = 'Katerina210'
        self.current_reply = ''

    def got_reply(self, reply):
        self.current_reply = reply
        self.loop.call_soon_threadsafe(self.reply)

    def reply(self):
        self.loop.create_task(self.sc.say(self.current_reply, self.voice))


class SpeechCloudDialog(Dialog):

    async def say(self, reply, voice):
        logging.info(f'TTS: {reply}')
        await self.synthesize_and_wait(text=reply, voice=voice)

    async def main(self):
        controller = VoiceKitController(sc_dialog=self)

        await self.synthesize_and_wait(text='VojsKit kontroler připraven.', voice=controller.voice)
        while True:
            self.sc.led_breath_slow()
            await self.sc.button_released()
            self.sc.led_off()
            result = await self.synthesize_and_wait_for_asr_result(text='Ano?', voice=controller.voice, timeout=10)

            while result is None:
                logging.info('Žádný výsledek nerozpoznán')
                result = await self.synthesize_and_wait_for_asr_result(text='Co?', voice=controller.voice, timeout=10)

            asr_result = result['result']
            logging.info(f'Rozpoznáno: {asr_result}')

            controller.new_command(asr_result)
