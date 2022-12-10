###
# Mastoquote, bot para publicar citas en Mastodon
# Inspirado en el bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from bundle.mastobot import Mastobot
from bundle.config import Config
from bundle.logger import Logger
from bundle.translator import Translator

import yaml
import random

class Runner:
    '''
    Main runner of the app
    '''
    def init(self):
        self._config     = Config()
        self._logger     = Logger(self._config).getLogger()

        self._translator = Translator("es")
        self._bot        = Mastobot(self._config)

        self.init_app_options()
        self.init_test_options()

        self._logger.info("init app")

        return self


    def init_app_options(self):

        quotes_file_name = self._config.get("app.quotes_file_name") 
        with open(quotes_file_name, 'r') as stream:
            self._authors  = yaml.safe_load(stream)
        
        self._logger.debug ("len authors: "   + str(len(self._authors)))
        

    def init_test_options (self):

        self._dismiss_disable = self._config.get("testing.disable_dismiss_notification")
        self._push_disable    = self._config.get("testing.disable_push_answer")
        self._test_word       = self._config.get("testing.text_word")

        self._logger.debug ("test_word: "   + self._test_word)
        self._logger.debug ("ignore test: " + str(self._config.get("testing.ignore_test_toot")))

        if self._test_word != "" and self._config.get("testing.ignore_test_toot"):
            self._ignore_test = True
        else:
            self._ignore_test = False 

    def run(self):

        self._logger.debug ("runing app")

        notifications = self._bot.mastodon.notifications()

        for notif in notifications:

            dismiss = True

            if notif.type == 'mention':

                if self._dismiss_disable:
                    dismiss = False
                    self._logger.debug("dismissing disabled notification id" + str(notif.id))                    
    
                if self._ignore_test and self._bot.check_keyword_in_nofit(self._bot, notif, self._test_word):
                    dismiss = False
                    self._logger.info("ignoring test notification id" + str(notif.id))
                else: 

                    for author in self._authors:

                        if self._bot.check_keyword_in_nofit(self._bot, notif, author["keyword"]):
                            text_post = self.replay_text(notif.status.language, author)

                            if self._push_disable:
                                self._logger.info("pushing answer disabled notification id" + str(notif.id))                     
                            else:
                                self._logger.info("answering notification id" + str(notif.id))
                                self._bot.replay(notif, text_post)

            if dismiss:
                self._logger.debug("dismissing notification id" + str(notif.id))
                self._bot.mastodon.notifications_dismiss(notif.id)

        self._logger.info("end app")


    def replay_text(self, language, author):        

        name    = author["name"]
        keyword = author["keyword"]
        quotes  = author["quotes"]

        self._logger.debug("notif language: " + language)                    
        self._logger.debug("notif name    : " + name)                    
        self._logger.debug("notif kewword : " + keyword)                    

        self._translator.fix_language (language)
        _text     = self._translator.get_text
    
        aleatorio = random.choice(quotes)

        post_text  = ", " +_text("cita") + ": " + aleatorio + "\n\n"
        post_text += "(" + _text("mencion") + " " + keyword + " " + _text("respuesta") + " " + name + ")"
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answering text\n" + post_text)
        return post_text

# main

if __name__ == '__main__':
    Runner().init().run()
