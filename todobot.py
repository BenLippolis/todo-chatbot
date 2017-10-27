# Parse JSON telegram responses 
import json 
# Make web requests using python 
import requests

import time 

import urllib 

import config 
from dbhelper import DBHelper

db = DBHelper()

# Telegram token 
TOKEN = config.token
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
def send_message(text, chat_id, reply_markup=None):
	# Utilize urllib to encode message text 
	text =  urllib.pathname2url(text)
	url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
	if reply_markup:
		url += "&reply_markup={}".format(reply_markup)
	get_url(url)

# Get the highest ID of all updates returned by getUpdates
def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

# Create a keyboard from a list of items 
def build_keyboard(items):
	keyboard = [[item] for item in items]
	reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
	return json.dumps(reply_markup)

def handle_updates(updates):
    for update in updates["result"]:
		text = update["message"]["text"]
		chat = update["message"]["chat"]["id"]
		items = db.get_items()
		if text == "/done":
			keyboard = build_keyboard(items)
			send_message("Select an item to delete", chat, keyboard)
		elif text in items: 
			db.delete_item(text)
			items = db.get_items()
			keyboard = build_keyboard(items)
			send_message("Select an item to delete", chat, keyboard)
		else:
			db.add_item(text)
			items = db.get_items()
			message = "\n".join(items)
			send_message(message, chat)

def main():
	db.setup()
	last_update_id = None
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			handle_updates(updates)
		time.sleep(0.5)

if __name__ == '__main__':
	main()