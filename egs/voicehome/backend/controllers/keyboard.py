from voicehome_controller import VoicehomeController


class KeyboardController(VoicehomeController):

    def __init__(self):
        VoicehomeController.__init__(self)

    @staticmethod
    def got_reply(reply):
        print('\nReply:', reply)


if __name__ == '__main__':
    controller = KeyboardController()
    while not controller.disconnected:
        command = input('Enter your command: ')
        controller.new_command(command)
