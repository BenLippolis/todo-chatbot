# Parse JSON telegram responses 
import json 
# Make web requests using python 
import requests

import time  

# Telegram token 
TOKEN = "405620811:AAEYygXLGGdhhAnUNaYkYo3G7LwDDRMAOuQ"
# Basic url for API requests 
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# Downloads url content and returns a string 
def get_url(url):
	response = requests.get(url)
	content = response.content.decode("utf8")
	return content

# Parses string response into python dictionary 
def get_json_from_url(url):
	content = get_url(url)
	js = json.loads(content)
	return js

# Returns list of messages sent to our bot 
def get_updates():
	url = URL + "getUpdates"
	js = get_json_from_url(url)
	return js

# Returns the chat ID and message text of the latest message 
def get_last_chat_id_and_text(updates):
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	text = updates["result"][last_update]["message"]["text"]
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	return (text, chat_id)

# Takes text of the message we want to send and the chat id of the chat where the message should be sent 
# Calls sendMessage command and passes passes text and chat id via params 
def send_message(text, chat_id):
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	get_url(url)

def main():
	last_textchat = (None, None)
	while True:
		text, chat = get_last_chat_id_and_text(get_updates())
		if (text, chat) != last_textchat:
			send_message(text, chat)
			last_textchat = (text, chat)
		time.sleep(0.5)

if __name__ == '__main__':
	main()