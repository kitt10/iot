from dialog import SpeechCloudWS, Dialog
import logging


class SmartLightsDefaultDialog(Dialog):

    async def main(self):
        pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s',level=logging.DEBUG)

    SpeechCloudWS.run(SmartLightsDefaultDialog,
                      address="0.0.0.0",
                      port=4000,
                      static_path="./static")
