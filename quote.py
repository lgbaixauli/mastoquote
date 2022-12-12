###
# Mastoquote, bot para publicar citas en Mastodon
# Inspirado en el bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from bundle.mastobot import Mastobot
from bundle.config import Config
from bundle.logger import Logger
from bundle.translator import Translator

import random

BOT_NAME = "Quotebot"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        self._translator = Translator("es")

        super().__init__(botname = botname)


    def init_test_options (self):

        self._dismiss_disable = self._config.get("testing.disable_dismiss")
        self._test_word       = self._config.get("testing.text_word")

        self._logger.debug ("test_word: "   + self._test_word)
        self._logger.debug ("ignore test: " + str(self._config.get("testing.ignore_test_toot")))

        if self._test_word != "" and self._config.get("testing.ignore_test_toot"):
            self._ignore_test = True
        else:
            self._ignore_test = False 

        super().init_test_options()
 

    def run(self, botname: str = BOT_NAME) -> None:

        notifications = self.mastodon.notifications()

        for notif in notifications:

            dismiss = True

            if notif.type == 'mention':

                if self._dismiss_disable:
                    dismiss = False
                    self._logger.debug("dismissing disabled notification id " + str(notif.id))                    
    
                if self._ignore_test and self.check_keyword_in_nofit(notif, self._test_word):
                    dismiss = False
                    self._logger.info("ignoring test notification id " + str(notif.id))
                else: 

                    for key in self._actions:

                        action = self._actions[key]

                        if self.check_keyword_in_nofit(notif, action["keyword"]):
                            text_post = self.find_text(notif.status.language, action["name"], action["keyword"], action["quotes"])

                            if self._push_disable:
                                self._logger.info("pushing answer disabled notification id " + str(notif.id))                     
                            else:
                                self._logger.info("answering notification id " + str(notif.id))
                                self.replay(notif, text_post)

            if dismiss:
                self._logger.debug("dismissing notification id " + str(notif.id))
                self.mastodon.notifications_dismiss(notif.id)

        super().run(botname = botname)


    def find_text(self, language, name, keyword, quotes):        

        self._logger.debug("notif language: " + language)                    
        self._logger.debug("notif name    : " + name)                    
        self._logger.debug("notif keyword : " + keyword)                    

        self._translator.fix_language (language)
        _text     = self._translator.get_text
    
        quote = random.choice(quotes)
        self._logger.debug ("quote id: " + str(quote["id"]))

        post_text  = ", " +_text("cita") + ": \n\n" + quote["text"] + "\n"

        if "comments" in quote:
            if quote["comments"] != "":
                post_text = post_text + quote["comments"] + "\n"

        if "source" in quote:
            if quote["source"] != "":
                post_text = post_text + quote["source"] + "\n"

        post_text += "\n"
        post_text += "(" + _text("mencion") + " " + keyword + " " + _text("respuesta") + " " + name + ")"
        post_text  = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answering text\n" + post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
