# Mastoquote

This code publish quotes, if requested.  
Based in the 'info' bot of @spla@mastodont.cat (https://git.mastodont.cat/spla/info)

The bot listen to a keyword:

@bot_username keyword

and then reply with a quote.

There are some config options in the config.yaml file

### Dependencies

-   **Python 3**
-   Mastodon account

### Usage:

Within Python Virtual Environment:

1. Optionally, create a new user for running the bot: `adduser --disabled-login user_name`

2. Clone the repository `git clone https://github.com/lgbaixauli/mastoquote.git` 

3. Crate a virtual environment `python3 -m venv .venv` and activate it `source .venv/bin/activate`

4. Run `pip install -r requirements.txt` to install needed libraries.  

5. Modify options in the `config.yaml` file. Fer exemple, the keyword or directories and files names.

6. Run `python3 quote.py` manually once to bot setup and get its access token to Mastodon instance.

7. Use your favourite scheduling method to set `quote.sh` to run every minute. For example, 
   add  `* * * * * /home/user_name/mastoquote/quote.sh 2>&1 | /usr/bin/logger -t MASTOSTATUS` in 
   `crontab -e`. The system and error log will be in `/var/log/syslog`. 
   Don't forgot the execution privilegies `chmod +x quote.sh`. 
   Don't forgot update the user_name in `quote.sh`