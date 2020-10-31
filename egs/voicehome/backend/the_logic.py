from threading import Thread, ThreadError


class VoicehomeLogic:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg
        self.actions = {}

    def on_command(self, command):
        for action_id, (method, list_of_calls) in self.actions.items():
            for call_tuple in list_of_calls:
                if all(call in command for call in call_tuple):
                    print('Logic: Found Match. Running', action_id)
                    try:
                        t = Thread(target=method)
                        t.setDaemon(False)
                        t.start()
                    except ThreadError:
                        print('ERR: Thread of Action', action_id)
