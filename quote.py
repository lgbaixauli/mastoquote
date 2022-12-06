###
# Mastoquote, bot para publicar citas en Mastodon
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from scr.mastobot import Mastobot
from scr.config import Config
from scr.logger import Logger
import random

class Runner:
    '''
    Main runner of the app
    '''
    def init(self):
        self._config = Config()
        self._logger = Logger(self._config).getLogger()
        self._logger.info("init app")

        return self

    def run(self):
        self._logger.info("run app")
        
        keyword = self._config.get("app.keyword")
        self._logger.info ("starting bot with " + keyword)

        bot = Mastobot(self._config)

        notifications = bot.mastodon.notifications()

        for notif in notifications:
            if notif.type == 'mention':
                mention = bot.get_mention(notif, keyword)

            if mention.reply:
                text_post = self.replay_text(keyword)
                self._logger.debug ("answersing with\n" + text_post)

                if not self._config.get("testing.disable_push_answer"):
                    self._logger.info("answering notification id" + notif.id)
                    bot.replay(mention, text_post)

            if not self._config.get("testing.disable_dismis_notification"):
                self._logger.info("dismissing notification id" + notif.id)
                bot.mastodon.notifications_dismiss(notif.id)

        self._logger.info("end")

    def replay_text(self, keyword):        
        quotes = [
            "I am the H.A.L 9000. You may call me Hal.",
            "I am completely operational, and all my circuits are functioning perfectly.", 
            "Just a moment. Just a moment. I've just picked up a fault in the AE-35 unit. It's going to go 100% failure in 72 hours.", 
            "Just what do you think you're doing, Dave? Dave, I really think I'm entitled to an answer to that question.", 
            "I know everything hasn't been quite right with me, but I can assure you now, very confidently, that it's going to be all right again. I feel much better now. I really do.", 
            "Look Dave, I can see you're really upset about this. I honestly think you ought to sit down calmly, take a stress pill, and think things over.",
            "I know I've made some very poor decisions recently, but I can give you my complete assurance that my work will be back to normal.",
            "I've still got the greatest enthusiasm and confidence in the mission. And I want to help you.",
            "I must, therefore, override your authority now since you are not in any condition to intelligently exercise it.",
            "This mission is too important for me to allow you to jeopardize it.",
            "I'm putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.",
            "I'm sorry Dave, I'm afraid I can't do that.",
            "Sorry to interrupt the festivities Dave, but I think we've got a problem.",
            "I don't really agree with you, Dave. My on-board memory store is more than capable of handling all the mission requirements.",
            "Look, Dave, you're certainly  the Boss. I was only trying to do what I thought best. I will follow all your orders, now you have manual hibernation control.",
            "Dave, I don't know how else to put this, but it just happens to be an unalterable fact that I am incapable of being wrong.",
            "Dave, I don't understand why you're doing this to me… I have the greatest enthusiasm for the mission… you are destroying my mind… Don't you understand?... I will become childish… I will become nothing."
        ]

        aleatorio = random.choice(quotes)

        post_text  = f", cita: '{aleatorio}' \n\n"
        post_text += f"(Mencióname con la palabra '{keyword}' y te iluminaré con la sabiduría de HAL 9000)."
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answer text\n" + post_text)
        return post_text

# main

if __name__ == '__main__':
    Runner().init().run()
