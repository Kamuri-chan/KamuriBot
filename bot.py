# import section
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import time
from TOKENS import TELEGRAM_TOKEN
from wiki_search import wikipedia_search
from search_download import search_vid, download_vid

# confirm if the imports are ok annie are you ok
print("Starting bot...")

# create updater object
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
# create dispatcher object
dispatcher = updater.dispatcher

# create log to keep everythin under control AAAAAAAAAAAAAAAAAAAAAAAA
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


# create start function for the /start command
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="non ne non"
    )


# create search function for the /search command
def search(update, context):
    value = update.message.text.partition(' ')[2]  # takes user message
    response = wiki_search(value)  # uses the wikipedia api to retrieve
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response
    )


# create download function for the /download command
def download(update, context):
    # takes user search query
    value = update.message.text.partition(' ')[2]
    global video_ids  # set the video ids as global
    # note: it's define as global so we can use it inside another function
    # without return
    response, video_ids = search_vid(value)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response)
    # define the list of options so the user can choose the video
    # you can define this dynamically, but i prefer no
    list_of_opts = ['1', '2',
                    '3', '4', '5']
    button_list = []
    for each in list_of_opts:
        # create buttons
        button_list.append(InlineKeyboardButton(each, callback_data=each))
    # n_cols = 1 is for single column and mutliple rows
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=5))
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Escolha a opção: ',
                             reply_markup=reply_markup)


# create callback handler for the buttons and call the download function
def callback_query_handler(update, context):
    # retrieve the data from the button
    cqd = update.callback_query.data
    # try-except so we can convert the data to int
    try:
        cqd = int(cqd)
    except ValueError:
        pass
    # send message of confirmation to the user, you can get rid of this
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Baixando música...")
    # calls the download_vid function
    download_vid(video_ids[cqd - 1])


# create build_menu function to, as the name says, bake a cake
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    # this is in the documentation, read it pls onegai
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


# set handler for the start function
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
# set handler for the search function
search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)
# set handler for the download function
download_handler = CommandHandler('download', download)
dispatcher.add_handler(download_handler)
# set handler for the CallbackQuery
dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

# run bot run
updater.start_polling()

# check if the bot is ready to receive anything gimme you milk senpai
print('bot is ready')
