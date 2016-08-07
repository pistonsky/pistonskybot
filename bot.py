import json
import logging

from tornado.httpclient import HTTPClient

from settings import *


def fast_urlencode(_dict):
    return '&'.join([k + '=' + str(v) for k, v in _dict.items()])

class Bot:
    BASE_URL = 'https://api.telegram.org/bot{}'.format(API_TOKEN)

    def __init__(self):
        self.http_client = HTTPClient()
        self.last_update_id = 0
        self.users = []

    def broadcast_new_messages(self, new_messages):
        """Sends all new audio messages from ALL users to ALL users.

        It doesn't send you the messages that you spoke yourself.
        `new_messages` is a list of (user_id, audio_id) tuples."""
        for user_id in self.users:
            for (sender_id, voice_id, ) in new_messages:
                if sender_id != user_id:
                    self.http_client.fetch("{}/sendVoice".format(self.BASE_URL),
                        method='POST', body=fast_urlencode({
                                'chat_id': user_id,
                                'voice': voice_id
                            }))

    def _run_once(self):
        new_messages = []
        response = self.http_client.fetch("{}/getUpdates".format(self.BASE_URL),
            method='POST', body=fast_urlencode({
                    'offset': self.last_update_id+1
                }))
        data = json.loads(response.body.decode('utf-8'))
        if data['ok']:
            for update in data['result']:
                if update['update_id'] > self.last_update_id:
                    self.last_update_id = update['update_id']
                message = update['message']
                sender_id = message['from']['id']
                if sender_id not in self.users:
                    logging.info("NEW USER: {} ({} {})".format(sender_id, message['from']['first_name'], message['from']['last_name']))
                    self.users.append(sender_id) # new user
                if 'voice' in message: # we only care about voice messages
                    voice_id = message['voice']['file_id']
                    new_messages.append((sender_id, voice_id, ))
            if len(new_messages) > 0:
                logging.info("Broadcasting {} new audio messages...".format(len(new_messages)))
                self.broadcast_new_messages(new_messages)
        else:
            logging.error("Telegram says that it's not okay...")

    def run(self):
        logging.info("Starting bot...")

        while True:
            self._run_once()


bot = Bot()
bot.run()
