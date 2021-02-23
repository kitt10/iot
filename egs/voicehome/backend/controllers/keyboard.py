from voicehome_controller import VoicehomeController


class KeyboardController(VoicehomeController):

    def __init__(self):
        VoicehomeController.__init__(self)
        self.controller_id = 'keyboard'

    @staticmethod
    def got_reply(reply):
        print('\n< '+reply+'\n> ', end='')


if __name__ == '__main__':
    controller = KeyboardController()
    while not controller.disconnected:
        command = input('> ')
        controller.new_command(command)
