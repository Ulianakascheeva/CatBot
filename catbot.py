import telebot								#Main package
from telebot import types		#For creating custom keyboard
import os 										#For listing dorectory
import sys									#For getting argument list
import random 							#For choosing random pic

# Opening directory with cat pics
if len(sys.argv) >= 2:
	media_dir = sys.argv[1]
else:
	# Default pics directory
	MEDIA_DIR_DEFAULT = 'media\\'
	media_dir = MEDIA_DIR_DEFAULT

# Getting list of pics
media_list = [] # Creating empty list of photos

try:
	item_list = os.listdir(media_dir)								# Reading files in directory
	for item in item_list:
		if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):	# Checking if file is a photo
			media_list.append(item)									# Adding photo to list
except IOError as e:
	sys.exit(str(e) + "\nError: Something is wrong with your directory") # Send error message and abort

# Checking if at least 1 photo is present
if(len(media_list) == 0):
	print("Error: No pictures found in your directory") # Send 'empty dir' message and continue work

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
	markup.resize_keyboard = True

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
	while (len(media_list) >= 1): # We go throw the list of images, looking for one we could open
		
		assert (len(media_list) >= 1), "Media list should contain at least 1 photo" # a bit of paranoia
		media_number = random.randint(0, len(media_list) - 1) # Choosing random photo out of list
		
		try:
			photo = open(media_dir + media_list[media_number], 'rb') # Attempt to open file
			
			#Send photo. No text, pure cat
			bot.send_photo(message.chat.id, photo)
		
			photo.close() # Closing file
			break # Ooooooou we finally quit loop
		
		except IOError as e:
			print(str(e) + "\nError: failed to open file") # Send error message and continue work
			media_list.pop(media_number) # Deleting bad image from the list
	else:
		print("Error: There are no more pictures in the directory") # Send 'empty dir' message and continue work
		#Out_of_cat Message
		bot.send_message(message.chat.id, "Sorry, we went out of cats. Try again later")

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

#Connecting to Telegram servers
#Starting tracking Telegram servers
bot.polling()

#cd C:\Users\Олег\source\Python\CatBot
#python catbot.py C:\Users\Олег\Pictures\