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
# Uses long polling to limit requests (timeout=100)
def get_updates(offset=None):
	url = URL + "getUpdates?timeout=100"
	if offset:
		url += "&offset={}".format(offset)
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

# Get the highest ID of all updates returned by getUpdates
def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

# Send an echo reply for each message we receive 
def echo_all(updates):
	for update in updates["result"]:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			send_message(text, chat)
		except Exception as e:
			print(e)

def main():
	last_update_id = None
	while True:
		print("getting updates biatch")
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			echo_all(updates)
		time.sleep(0.5)

if __name__ == '__main__':
	main()