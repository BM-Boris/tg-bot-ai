import os
import http

from flask import Flask, request
from werkzeug.wrappers import Response

from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from openai_api import generate_response, new_user, set_new_personality, delete_hist, delete_last
import config
import drive_api 

app = Flask(__name__)

updater = Updater(token=config.bot_token, use_context=True)
dispatcher = updater.dispatcher
bot = Bot(token=config.bot_token)

#check

# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):


    chat_id = update.effective_chat.id
    username = update.message.chat.username

    if(username in config.access_list):
        
        context.bot.send_message(chat_id=chat_id, text="Your Text")
    else:

        context.bot.send_message(chat_id=chat_id, text="Your Text")




def config_personality(update, context):

    context.user_data['waiting_for_message'] = True
    names_for_users = '*Your Text* \n\n'

    for i in drive_api.persona:

        names_for_users = names_for_users + f' ```{i["name"]}```\n\n'

    context.bot.send_message(chat_id=update.message.chat_id, text=names_for_users, parse_mode='markdown')

def delete_history(update, context):
    delete_hist(update.message.chat.username)
    message = '*Your Text* '
    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='markdown')

def delete_last_message(update, context):
    delete_last(update.message.chat.username)
    message = '*Your Text* '
    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='markdown')


def get_message(update, context):

    username = update.message.chat.username
    new_personality = ''

    if(username in config.access_list):

        if 'waiting_for_message' in context.user_data and context.user_data['waiting_for_message']:

            new_personality = update.message.text

            allowed_personality = [i['spelling'] for i in drive_api.persona] + [i['name'] for i in drive_api.persona]

            if(new_personality not in allowed_personality):

                context.bot.send_message(chat_id=update.message.chat_id, text='Your Text', parse_mode='markdown')

            else:
                set_new_personality(username, new_personality)
                context.bot.send_message(chat_id=update.message.chat_id, text=f"✔️")
                del context.user_data['waiting_for_message']
        
        else:

            new_user(username)

            res = generate_response(update.message.text, username)

            update.message.reply_text(res)

    else:

        update.message.reply_text('Your Text')



# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("config", config_personality))
dispatcher.add_handler(CommandHandler("delete", delete_history))
dispatcher.add_handler(CommandHandler("last", delete_last_message))

dispatcher.add_handler(MessageHandler(Filters.text, get_message))

# invoke the get_message function when the user sends a message 
@app.post("/")
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT

