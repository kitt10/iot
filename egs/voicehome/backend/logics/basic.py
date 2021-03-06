from logics.voicehome_logic import VoicehomeLogic
from threading import Thread, ThreadError


class BasicLogic(VoicehomeLogic):

    def __init__(self, engine):
        VoicehomeLogic.__init__(self, engine)

    def on_command(self, command):
        for move_id, (method, list_of_calls) in self.moves.items():
            for call_tuple in list_of_calls:
                if all(call in command for call in call_tuple):
                    print('Logic: Found Match. Running', move_id)
                    try:
                        t = Thread(target=method)
                        t.setDaemon(False)
                        t.start()
                    except ThreadError:
                        print('ERR: Thread of Move', move_id)

                    break
