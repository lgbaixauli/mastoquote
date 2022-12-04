from mastodon import Mastodon
from mastodon.Mastodon import MastodonMalformedEventError, MastodonNetworkError, MastodonReadTimeout, MastodonAPIError, MastodonIllegalArgumentError
import getpass
import unidecode
import fileinput,re
import os
import sys
import os.path
import random

###
# Dict helper class.
# Defined at top level so it can be pickled.
###
class AttribAccessDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("Attribute not found: " + str(attr))

    def __setattr__(self, attr, val):
        if attr in self:
            raise AttributeError("Attribute-style access is read only")
        super(AttribAccessDict, self).__setattr__(attr, val)

class Mastobot:

    name = 'Mastobot'

    def __init__(self, mastodon=None, mastodon_hostname=None):

        file_path = "secrets/secrets.txt"
        
        is_setup = self.check_setup(file_path)

        if is_setup:

            self.uc_client_id     = self.get_parameter("uc_client_id",     file_path)
            self.uc_client_secret = self.get_parameter("uc_client_secret", file_path)
            self.uc_access_token  = self.get_parameter("uc_access_token",  file_path)
            
            self.mastodon, self.mastodon_hostname = self.log_in(self)

        else:

            while(True):

                logged_in, self.mastodon, self.mastodon_hostname = self.setup()

                if not logged_in:

                    print("\nLog in failed! Try again.\n")

                else:

                    break

    def get_data(self, notif):

        id = notif.id

        account_id = notif.account.id

        username = notif.account.acct

        status_id = notif.status.id

        text  = notif.status.content

        visibility = notif.status.visibility

        reply, question = self.get_question(self, text)

        mention_dict = {'reply': reply, 'question': question, 'id': id, 'account_id': account_id, 'username': username, 'status_id': status_id, 'text': text, 'visibility': visibility}

        mention = self.__json_allow_dict_attrs(mention_dict)

        return mention

    def post(self, mention):

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

        post_text  = f"Quote: '{aleatorio}' \n\n"
        post_text += f"(Mencióname con la palabra 'quote' y te iluminaré con la sabiduría de HAL 9000)."

        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self.mastodon.status_post(post_text, in_reply_to_id=mention.status_id,visibility=mention.visibility)

        print(f'Replied notification {mention.id}')

        self.mastodon.notifications_dismiss(mention.id)

    @staticmethod
    def __json_allow_dict_attrs(json_object):
        """
        Makes it possible to use attribute notation to access a dicts
        elements, while still allowing the dict to act as a dict.
        """
        if isinstance(json_object, dict):
            return AttribAccessDict(json_object)
        return json_object

    @staticmethod
    def get_question(self, text):

        reply = False

        keyword = '' 

        content = self.cleanhtml(self, text)

        content = self.unescape(self, content)

        try:

            start = content.index("@")
            end = content.index(" ")
            if len(content) > end:

                content = content[0: start:] + content[end +1::]

            cleanit = content.count('@')

            i = 0
            while i < cleanit :

                start = content.rfind("@")
                end = len(content)
                content = content[0: start:] + content[end +1::]
                i += 1

            content = content.lower()
            question = content

            keyword_length = 5
            keyword = 'quote'

            if unidecode.unidecode(question)[0:keyword_length] == keyword:

                reply = True

        except:

            pass

        return (reply, question)

    @staticmethod
    def log_in(self):

        file_path = "secrets/secrets.txt"
        uc_client_id     = self.get_parameter("uc_client_id",     file_path)
        uc_client_secret = self.get_parameter("uc_client_secret", file_path)
        uc_access_token  = self.get_parameter("uc_access_token",  file_path)

        file_path = "config/config.txt"
        self.mastodon_hostname = self.get_parameter("mastodon_hostname", file_path)

        self.mastodon = Mastodon(
            client_id = uc_client_id,
            client_secret = uc_client_secret,
            access_token = uc_access_token,
            api_base_url = 'https://' + self.mastodon_hostname,
        )

        headers={ 'Authorization': 'Bearer %s'%uc_access_token }

        return (self.mastodon, self.mastodon_hostname)

    @staticmethod
    def check_setup(file_path):

        is_setup = False

        if not os.path.isfile(file_path):
            print(f"File {file_path} not found, running setup.")
            return
        else:
            is_setup = True
            return is_setup

    @staticmethod
    def get_parameter(parameter, file_path ):

        with open( file_path ) as f:
            for line in f:
                if line.startswith( parameter ):
                    return line.replace(parameter + ":", "").strip()

        print(f'{file_path} Missing parameter {parameter}')
        sys.exit(0)

    @staticmethod
    def cleanhtml(self, raw_html):

        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    @staticmethod
    def unescape(self, s):

        s = s.replace("&apos;", "'")
        return s

    @staticmethod
    def modify_file(self, file_name, pattern,value=""):

        fh=fileinput.input(file_name,inplace=True)

        for line in fh:

            replacement=pattern + value
            line=re.sub(pattern,replacement,line)
            sys.stdout.write(line)

        fh.close()

    def setup(self):

        logged_in = False

        try:

            self.mastodon_hostname = input("Enter Mastodon hostname (or 'q' to exit): ")

            if self.mastodon_hostname == 'q':

                sys.exit("Bye")

            user_name = input("User email, ex. user@" + self.mastodon_hostname +"? ")
            user_password = getpass.getpass("User password? ")
            app_name = input("App name? ")

            Mastodon.create_app(app_name, scopes=["read","write"],

                    to_file="app_clientcred.txt", api_base_url=self.mastodon_hostname)

            mastodon = Mastodon(client_id = "app_clientcred.txt", api_base_url = self.mastodon_hostname)

            mastodon.log_in(
                user_name,
                user_password,
                scopes = ["read", "write"],
                to_file = "app_usercred.txt"
            )

            if os.path.isfile("app_usercred.txt"):

                print(f"Log in succesful!")
                logged_in = True

            if not os.path.exists('secrets'):
                os.makedirs('secrets')

            secrets_filepath = 'secrets/secrets.txt'

            if not os.path.exists(secrets_filepath):
                with open(secrets_filepath, 'w'): pass
                print(f"{secrets_filepath} created!")

            with open(secrets_filepath, 'a') as the_file:
                print("Writing secrets parameter names to " + secrets_filepath)
                the_file.write('uc_client_id: \n'+'uc_client_secret: \n'+'uc_access_token: \n')

            client_path = 'app_clientcred.txt'

            with open(client_path) as fp:

                line = fp.readline()
                cnt = 1

                while line:

                    if cnt == 1:

                        print("Writing client id to " + secrets_filepath)
                        self.modify_file(self, secrets_filepath, "uc_client_id: ", value=line.rstrip())

                    elif cnt == 2:

                        print("Writing client secret to " + secrets_filepath)
                        self.modify_file(self, secrets_filepath, "uc_client_secret: ", value=line.rstrip())

                    line = fp.readline()
                    cnt += 1

            token_path = 'app_usercred.txt'

            with open(token_path) as fp:

                line = fp.readline()
                print("Writing access token to " + secrets_filepath)
                self.modify_file(self, secrets_filepath, "uc_access_token: ", value=line.rstrip())

            if os.path.exists("app_clientcred.txt"):

                print("Removing app_clientcred.txt temp file..")
                os.remove("app_clientcred.txt")

            if os.path.exists("app_usercred.txt"):

                print("Removing app_usercred.txt temp file..")
                os.remove("app_usercred.txt")

            config_filepath = 'config/config.txt'

            if not os.path.exists('config'):
                os.makedirs('config')

            if not os.path.exists(config_filepath):
                with open('config/config.txt', 'w'): pass
                print(config_filepath + " created!")
      
            with open(config_filepath, 'a') as the_file:
                the_file.write('mastodon_hostname: \n')
                print(f"adding parameter 'mastodon_hostname' to {config_filepath}")
   
            self.modify_file(self, config_filepath, "mastodon_hostname: ", value=self.mastodon_hostname)
    
            print("Secrets setup done!\n")

        except MastodonIllegalArgumentError as i_error:

            sys.stdout.write(f'\n{str(i_error)}\n')

        except MastodonNetworkError as n_error:

            sys.stdout.write(f'\n{str(n_error)}\n')

        except MastodonReadTimeout as r_error:

            sys.stdout.write(f'\n{str(r_error)}\n')

        except MastodonAPIError as a_error:

            sys.stdout.write(f'\n{str(a_error)}\n')

        return (logged_in, mastodon, self.mastodon_hostname)

