from mastobot import Mastobot

# main

if __name__ == '__main__':

    bot = Mastobot()

    notifications = bot.mastodon.notifications()

    for notif in notifications:

        if notif.type != 'mention':

            print(f"Dismissing notification id {notif.id}")

            bot.mastodon.notifications_dismiss(notif.id)

        else:

            mention = bot.get_data(notif)

            if mention.reply:

                bot.post(mention)

            else:

                print(f"Dismissing notification id {notif.id}")

                bot.mastodon.notifications_dismiss(notif.id)

