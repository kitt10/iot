from controller import VoicehomeController


class KeyboardController(VoicehomeController):

    def __init__(self):
        VoicehomeController.__init__(self)

    def new_reply(self):
        print('Reply:', self.last_reply())


if __name__ == '__main__':
    controller = KeyboardController()
    while not controller.disconnected:
        command = input('Enter your command: ')
        controller.new_command(command)
