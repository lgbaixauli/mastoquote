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

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_translator()


    def run(self, botname: str = BOT_NAME) -> None:

        notifications = self.mastodon.notifications()

        for notif in notifications:

            action   = self._actions["Quote_HAL"]   
            replay, dismiss1 = self.process_notif(notif, "mention", action["keyword"])
            if replay:
                self.replay_toot(self.find_text(notif, action), notif)
     
            action   = self._actions["Quote_Terry"]
            replay, dismiss2 = self.process_notif(notif, "mention", action["keyword"])
            if replay: 
                self.replay_toot(self.find_text(notif, action), notif)

            if dismiss1 and dismiss2:
                self.mastodon.notifications_dismiss(notif.id)

        super().run(botname = botname)


    def find_text(self, notif, action):        

        language = notif.status.language
        username = notif.account.acct
        name     = action["name"]
        keyword  = action["keyword"]
        quotes   = action["quotes"]
        quote    = random.choice(quotes)
 
        self._logger.debug("notif language: " + language)                    
        self._logger.debug("notif name    : " + name)                    
        self._logger.debug("notif keyword : " + keyword)                    

        self._translator.fix_language (language)
        _text     = self._translator.get_text
    
        self._logger.debug ("quote id: " + str(quote["id"]))

        post_text  = "@" + username + ":\n\n" + quote["text"] + "\n"

        if "comments" in quote:
            if quote["comments"] != "":
                post_text = post_text + quote["comments"] + "\n"

        if "source" in quote:
            if quote["source"] != "":
                post_text = post_text + quote["source"] + "\n"

        post_text += "\n"
        post_text += "(" + _text("mencion") + " \"" + keyword + "\" " + _text("respuesta") + " " + name + ")"
        post_text  = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answering text\n" + post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
