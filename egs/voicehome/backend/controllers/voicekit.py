from voicehome_controller import VoicehomeController


class VoiceKitController(VoicehomeController):

    def __init__(self):
        VoicehomeController.__init__(self)

    @staticmethod
    def got_reply(reply):
        print('Reply:', reply)
