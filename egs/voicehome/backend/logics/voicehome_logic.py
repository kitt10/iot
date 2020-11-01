from abc import abstractmethod


class VoicehomeLogic:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg
        self.moves = {}

    @abstractmethod
    def on_command(self, command):
        pass
