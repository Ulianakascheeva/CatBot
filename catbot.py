import telebot								#Main package
from telebot import types		#For creating custom keyboard
import os 										#For listing dorectory
import random 							#For choosing random pic

# Creating 'bot' object
API_TOKEN = "1193477236:AAHAjKpC6Oc76GReNnXvDmQAoJqqsgJIvno"
bot = telebot.TeleBot(API_TOKEN)

## Here the list of handlers goes

#/start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
	#Inside Keyboard Creation
	markup = types.ReplyKeyboardMarkup()
	button_get_cat = types.KeyboardButton('/get_cat') # GetCat Button
	markup.row(button_get_cat)

	#Welcoming Message
	bot.send_message(message.chat.id, "Congretulations! How are you doing, cat lover?)\nPress /get_cat and fly to heaven", reply_markup = markup)

#/help command
@bot.message_handler(commands=['help'])
def send_help(message):
	#Help Message with list of instructions
	bot.send_message(message.chat.id, "Here are the instructions. Programmer Uliana forgot to write them, Oops")

#/get_cat command
@bot.message_handler(commands=['get_cat'])
def send_cat(message):
	#Opening current directory "media\"
	media_list = os.listdir('media\\')
	#Choosing random photo out of those
	photo = open('media\\' + media_list[random.randint(0, len(media_list) - 1)], 'rb')
	#Send photo. No text, pure cat
	bot.send_photo(message.chat.id, photo)

#photo sent
@bot.message_handler(content_types=['photo'])
def handle_pics(message):
	#Answering other cat is beautiful (because all of them are)
	bot.send_message(message.chat.id, "Beautiful!")

#other commands
@bot.message_handler(func=lambda message: True)
def other(message):
	#Answering user's command doesn't fit any filter
	bot.reply_to(message, "Sorry, didn't catch the idea, please try again.\n/help for list of commands")

#Connecting to Telegram server
#Starting tracking Telegram servers
bot.polling()