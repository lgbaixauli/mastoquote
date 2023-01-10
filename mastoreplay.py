"""
Mastoreplay, bot para contestar notificaciones, en este caso con citas, en Mastodon
Inspirado (pero a cada refactorización más lejos) en el bot "info" original de @spla@mastodont.cat
En https://git.mastodont.cat/spla/info
"""

import random
from pybot.mastobot import Mastobot

BOT_NAME = "Replaybot"
MAX_LENGHT = 490

class Bot(Mastobot):
    """ Main class of a Mastodon bot """

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_translator()


    def run(self, botname: str = BOT_NAME) -> None:

        notifications = self.mastodon.notifications()
        for notif in notifications:

            content = self.check_notif(notif, "mention")

            if content != "":
                content_list = content.split()
                if self._actions.get("Quote_HAL.keyword").lower() in content_list: 
                    self.replay_toot (self.find_text(notif, self._actions.get("Quote_HAL")), notif)
                elif self._actions.get("Quote_Terry.keyword").lower() in content_list: 
                    self.replay_toot (self.find_text(notif, self._actions.get("Quote_Terry")), notif)

        super().run(botname = botname)


    def find_text(self, notif, action):
        """ find the text to post """

        language = notif.status.language
        username = notif.account.acct
        name     = action["name"]
        keyword  = action["keyword"]
        quote    = random.choice(action["quotes"])

        self._logger.debug("notif language: %s", language)
        self._logger.debug("notif name    : %s", name)
        self._logger.debug("notif keyword : %s", keyword)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        self._logger.debug ("quote id: %i", quote[0])

        post_text  = "@" + username + ":\n\n" + quote[1] + "\n"

        # comments
        if quote[2] != "":
            post_text = post_text + quote[2] + "\n"
        
        # source
        if quote[3] != "":
            post_text = post_text + quote[3] + "\n"

        post_text += "\n"
        post_text += "(" + _text("mencion") + " \"" + keyword + "\" " + \
            _text("respuesta") + " " + name + ")"
        post_text  = (post_text[:MAX_LENGHT] + '... ') if len(post_text) > MAX_LENGHT else post_text

        self._logger.debug ("answering text\n %s", post_text)

        return post_text



# main

if __name__ == '__main__':
    Bot().run()
