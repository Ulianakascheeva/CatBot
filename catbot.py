import telebot                              # Main package
from telebot import types         # For creating custom keyboard
import os                                       # For listing directory
import sys                                      # For getting argument list
import random                             # For choosing random pic
import requests                            # For downloading pictures

# Creating list of directories to take pics from
media_dir_list = sys.argv[1:]

# Setting media_saving - boolean that mean pics have to be saved
# Check if last argument is '-dontsave' (in this case pics will not be saved)
if (len(media_dir_list) >= 1 and media_dir_list[-1] == '-dontsave'):
    media_saving = False
    media_dir_list.pop()
else:
    media_saving = True

# Setting media_dir_list to default if no arguments have been passed
# (or the only one was '-dontsave')
if len(media_dir_list) == 0:
    MEDIA_DIR_DEFAULT = 'media\\'  # Default pics directory
    media_dir_list.append(MEDIA_DIR_DEFAULT)

# First media directory is directory to save media
if media_saving is True:
    assert(len(media_dir_list) >= 1)  # a bit of paranoia
    media_saving_dir = media_dir_list[0]
else:
    media_saving_dir = None

# Creating list of strings, each is path to image
media_list = []  # Empty at that time


# Function that updates media_list:
def update_media_list():
    global media_list
    media_list = []  # Clearing list to avoid duplication

    try:
        # Seek throw directories
        for media_dir in media_dir_list:
            # Reading files in directory
            items = os.listdir(media_dir)
            # Running throw all the files in directory
            for item in items:
                # Checking if file is a photo
                if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    # Adding photo to list if so
                    media_list.append(media_dir + item)
    except IOError as e:
        # Send error message and abort
        sys.exit(str(e) + "\nError: Something is wrong with your directory")


# Initial update
update_media_list()

# Checking if at least 1 photo is present
if(len(media_list) == 0):
    # Send 'empty dir' message and continue work
    print("Error: No pictures found in your directories")

# Creating 'bot' object
API_TOKEN = "1193477236:AAHAjKpC6Oc76GReNnXvDmQAoJqqsgJIvno"
bot = telebot.TeleBot(API_TOKEN)

# Here the list of handlers goes

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Inside Keyboard Creation
    markup = types.ReplyKeyboardMarkup()
    button_get_cat = types.KeyboardButton('Получить')  # GetCat Button
    markup.row(button_get_cat)
    markup.resize_keyboard = True

    # Welcoming Message
    bot.send_message(message.chat.id,
                     "Welcome to the party\n"
                     "I hope you like cats\n\n"
                     "Мы рады, что ты с нами. Всё просто: жми Получить,"
                     "и мы пришлём тебе кота.\n"
                     "/help, чтобы увидеть полный список команд",
                     reply_markup=markup)


# /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    # Help Message with list of instructions
    bot.send_message(message.chat.id,
                     "Список команд CatBot'а:\n"
                     "/start Начать диалог\n"
                     "/help Помощь\n"
                     "/cat Прислать кота (Можно также"
                     "нажать кнопку Прислать)\n\n"
                     "Вы также можете прислать свою фотографию, и"
                     "CatBot сохранит её и будет выдавать при запросе."
                     "Для этого просто пришлите фото в чат.")


# /cat command
@bot.message_handler(commands=['cat'])
@bot.message_handler(regexp='Получить')
def send_cat(message):
    # We go throw the list of images, looking for one we could open
    while (len(media_list) >= 1):

        # a bit of paranoia
        assert (len(media_list) >= 1)

        # Choosing random photo out of list
        media_number = random.randint(0, len(media_list) - 1)

        try:
            # Attempt to open file
            photo = open(media_list[media_number], 'rb')

            # Send photo. No text, pure cat
            bot.send_photo(message.chat.id, photo)

            photo.close()  # Closing file
            break  # Ooooooou we finally quit loop, as sent photo

        except IOError as e:
            # Send error message and continue work
            print(str(e) + "\nError: failed to open file")
            # Deleting bad image from the list
            media_list.pop(media_number)
    else:
        # Maybe it is a good idea to call update_media_list() here...
        # Send 'empty dir' message and continue work
        print("Error: There are no more pictures in the directory")
        # Out_of_cat Message
        bot.send_message(message.chat.id,
                         "Извините, коты закончились.\n"
                         "Sorry, we went out of cats")


# photo message
@bot.message_handler(content_types=['photo'])
def handle_pic(message):
    # Answering other cat is beautiful (because all of them are)
    bot.send_message(message.chat.id, "Это прекрасно!")

    if media_saving is True:
        try:
            # message should contain at least 1 photo_size object
            assert(len(message.photo) >= 1)

            # There are several 'photo_size' objects
            # We're interested in the last one as it has highest dimension
            pic = message.photo[-1]

            # Considering pic name
            file_info = bot.get_file(pic.file_id)
            # Getting file extension
            file_ext = '.' + file_info.file_path.split('.')[-1]
            # Image will have such path
            pic_path = media_saving_dir + pic.file_id + file_ext

            print(pic_path)

            # Check for file existance (saving photo only if there isn't same)
            if not os.path.isfile(pic_path):
                # Downloading photo
                pic = requests.get('https://api.telegram.org/file/bot{0}/{1}'.
                                   format(API_TOKEN,
                                          file_info.file_path))

                # Saving photo and closing file
                file = open(pic_path, 'wb')
                file.write(pic.content)
                file.close()

                # Add new path to media_list
                media_list.append(pic_path)

                # Tnanks Message
                bot.send_message(message.chat.id,
                                 "Изумительно. Спасибо за картинку!")
            else:
                # Duplicate_photo message
                bot.send_message(message.chat.id,
                                 "Спасибо, хотя эта картинка у меня уже есть)")
        except IOError as e:
            # Send error message and continue work
            print(str(e) + "\nError: Something went wrong during saving file")
        except requests.exceptions.RequestException as e:
            # Send error message and continue work
            print(str(e) + "\nError: Something went"
                  "wrong during downloading file")


# other messages
@bot.message_handler(func=lambda message: True)
def other(message):
    # Answering user's command doesn't fit any filter
    bot.reply_to(message,
                 """Я вас не понимаю.
                 /help, чтобы перейти к списку
                 доступных команд""")


# Connecting to Telegram servers
# Starting tracking Telegram servers
bot.polling()
