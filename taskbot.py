# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 12:35:03 2017
@author: Ignasi Dev
"""

# VERSION WITH THE EVERIS-API PROCESSING
from __future__ import print_function # Import Everis stuff

import json

# Requests needed for web requests with the Telegram API:
import requests

# To force a small delay between requests:
import time

# To accept special characters:
import urllib

from dbhelper import DBHelper
from random import randint

db = DBHelper()
TOKEN = "insertTokenHere"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# Everis headers:
headers = {
    'x-api-key': '9CAfxmC4WB10tnS9RY9oG92Io0M4trVp7HpTUEjR', # key NOT CLASSIFIED
    'Content-Type': 'application/json',
}

# Everis functions:
def get_language(text_in):
    data = {"textIn": text_in}
    r = requests.post('https://jmlk74oovf.execute-api.eu-west-1.amazonaws.com/dev/language?wait=true', headers=headers, data=json.dumps(data))
    content = r.json()
    return content['results']['language']

def get_sentiment(text_in, language='English'):
    data = {"textIn": text_in,  "language": language}
    r = requests.post('https://jmlk74oovf.execute-api.eu-west-1.amazonaws.com/dev/sentiment?wait=true', headers=headers, data=json.dumps(data))
    content = r.json()
    return content['results']['prediction']

""" Useful to check connection with Everis API
print(get_language("?"))
print(get_sentiment("Bad and sad", "English")) # To get a negative response
"""

# Download the content from an url and returns a string:
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# Parse the string response into the py library:
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# Use Long Polling: keep the connection open until there are updates, when
# sends it down the open pipe. Also, specify the time the connection
# stays opened with timeout:
def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# How to react given the user text entry:
def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)
        if text == "/delete" or text == "delete":
            keyboard = build_keyboard(items)
            send_message("Delete mode entered.\nSelect an item to be deleted. If you want to add something instead, just type the new task anytime", chat, keyboard)
        elif text == "/help" or text == "help" or text == "Help" or text == "HELP":
            send_message("HELP INFORMATION: \n- To see the whole task list, send '\list'\n- To enter delete mode, send me '\delete', and I will erase whatever task you then select. From this mode, if you want to add more tasks just type'em!\n- To restart but with the same list, type '/start'\n- For further info just hit up my creator at Slack! (@ignasi)", chat)
            send_message("So, what is something you want to add to the task list?", chat)
        elif text == "/list" or text == "list" or text == "List" or text == "LIST":
            send_message("Task List (updated):", chat)
            message = "\n".join(items)
            send_message(message, chat)
        elif text == "/start" or text == "start" or text == "Start" or text == "START":
            send_message("Hi! I am your task manager. Add items and remove them via /delete. Type /help anytime you want.", chat)
        elif text == "/list" or text == "list":
            message = "\n".join(items)
            send_message(message, chat)
        elif text.startswith("/"):
            continue
        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to be deleted", chat, keyboard)
            message = "\n".join(items)
            send_message(message, chat)
        else:
            if get_language(text) == "Unknown":
              send_message("I don't quite get it, but hey, that's your list!", chat)
            elif get_language(text) != "English":
              send_message("I see you are bilingual! How cool is that!", chat)
              send_message("I am sorry I am not, although I can still take note of your plurilingual tasks.", chat)
            db.add_item(text, chat)
            items = db.get_items(chat)
            sentiment = get_sentiment(text, language='English')
            counter = randint(1, 4)
            if counter == 1:
              if sentiment == "neutral":
                send_message("I see, a pretty rudimentary task.", chat)
              elif sentiment == "positive":
                send_message("Awesome!", chat)
              elif sentiment == "negative":
                send_message("Oh, that doesn't seem fun.", chat)
            elif counter == 2:
              if sentiment == "neutral":
                send_message("Ok, I just added it in.", chat)
              elif sentiment == "positive":
                send_message("That looks incredible!", chat)
              elif sentiment == "negative":
                send_message("Damn human, I'm sorry for you.", chat)
            elif counter == 3:
              if sentiment == "neutral":
                send_message("Note taken.", chat)
              elif sentiment == "positive":
                send_message("I'm pretty sure you're gonna have a blast with that.", chat)
              elif sentiment == "negative":
                send_message("It's important to keep going thru hard times.", chat)
            else:
              if sentiment == "neutral":
                send_message("Alright.", chat)
              elif sentiment == "positive":
                send_message("Fantastic, glad you get to do those things!", chat)
              elif sentiment == "negative":
                send_message("Not funny. I see you.", chat)
            send_message("Task List (updated):", chat)
            message = "\n".join(items)
            send_message(message, chat)
            question = randint(1, 9)
            if question == 1:
              send_message("What else?", chat)
            if question == 2:
              send_message("Anything else?", chat)
            if question == 3:
              send_message("Any other task?", chat)
            if question == 4:
              send_message("What else do you want to add?", chat)
            if question == 5:
              send_message("Tell me more tasks!", chat)
            if question == 6:
              send_message("Keep telling me tasks!", chat)
            if question == 7:
              send_message("Anything you would like to add?", chat)
            if question == 8:
              send_message("What else do you have for me?", chat)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

# Pass the special keyboard and let it open when called:
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
# "reply_markup" does not only reference the Keyboard: it is indeed an object
# that includes various features of the keyboard.

def send_message(text, chat_id, reply_markup = None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text = {}&chat_id = {}&parse_mode = Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup = {}".format(reply_markup)
    get_url(url)

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
