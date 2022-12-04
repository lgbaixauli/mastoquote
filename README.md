# Info
This code publish quotes, if requested.  
Based in the info bot of @spla@mastodont.cat (https://git.mastodont.cat/spla/info)

The bot listen to 'quote' word key:

@bot_username quote

and then reply with a quote.

### Dependencies

-   **Python 3**
-   Mastodon account

### Usage:

Within Python Virtual Environment:

1. Run `pip install -r requirements.txt` to install needed libraries.  

2. Run `python3 quote.py` manually once to bot setup and get its access token to Mastodon instance.

3. Use your favourite scheduling method to set `quote.sh` to run every minute. For example, 
   add  `* * * * * /home/mastoquote/code/quote.sh 2>&1 | /usr/bin/logger -t MASTOQUOTE` in 
   `crontab -e`. The system and error log will be in `/var/log/syslog`. Don't forgot the execution 
   privilegies `chmod +x quote.sh`.