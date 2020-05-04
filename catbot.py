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


# Keyboard creation functions

def simple_keyboard():
    # Keyboard Creation
    markup = types.ReplyKeyboardMarkup()

    # Buttons
    button_cat = types.KeyboardButton('Получить')  # GetCat Button
    markup.row(button_cat)
    markup.resize_keyboard = True

    return markup


def advanced_keyboard():
    # Keyboard Creation
    markup = types.ReplyKeyboardMarkup()

    # Buttons
    button_cat = types.KeyboardButton('/cat')
    markup.row(button_cat)  # GetCat Button
    button_cats5 = types.KeyboardButton('/cats5')
    button_cats10 = types.KeyboardButton('/cats10')
    button_cats1000 = types.KeyboardButton('/cats1000')
    markup.row(button_cats5, button_cats10, button_cats1000)  # GetCats Buttons

    markup.resize_keyboard = True

    return markup


# Here the list of handlers goes

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Welcoming Message
    bot.send_message(message.chat.id,
                     "Welcome to the party\n"
                     "I hope you like cats\n\n"
                     "Мы рады, что ты с нами. Всё просто: жми Получить,"
                     "и мы пришлём тебе кота.\n"
                     "/help, чтобы увидеть полный список команд",
                     reply_markup=simple_keyboard())


# /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    # Help Message with list of instructions
    bot.send_message(message.chat.id,
                     "Список команд CatBot'а:\n"
                     "/start Начать диалог\n"
                     "/help Помощь\n"
                     "/cat Прислать кота (Можно также "
                     "нажать кнопку Прислать)\n\n"
                     "Вы также можете прислать свою фотографию, и "
                     "CatBot сохранит её и будет выдавать при запросе. "
                     "Для этого просто пришлите фото в чат.\n\n"
                     "CatBot также поддерживает функцию /cats, позволяющую "
                     "получить 10 котов сразу. Функция также работает в "
                     "пользовательском режиме:\n"
                     "/cats - прислать 10 котов\n"
                     "/cats5 - прислать 5 котов\n"
                     "/cats10000 - прислать 10 тысяч котов (к сожалению, "
                     "наши ресурсы ограничены - велика вероятность, что "
                     "некоторые коты будут присланы дважды.\n\n"
                     "Функция для CatGeek'ов:\n"
                     "/enable_cats_keyboard - включить cats клавиатуру\n"
                     "/disable_cats_keyboard - отключить cats "
                     "клавиатуру\n\n"
                     "Желаем приятного времяпровождения!")


# send_one cat (the main function in that file)
def send_random_cat(chat_id):
    # We go throw the list of images, looking for one we could open
    while (len(media_list) >= 1):

        # a bit of paranoia
        assert (len(media_list) >= 1)

        # Choosing random photo out of list
        media_number = random.randrange(0, len(media_list))

        try:
            # Attempt to open file
            photo = open(media_list[media_number], 'rb')

            # Send photo. No text, pure cat
            bot.send_photo(chat_id, photo)

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
        bot.send_message(chat_id,
                         "Извините, коты закончились.\n"
                         "Sorry, we went out of cats")


# /cat command
@bot.message_handler(commands=['cat'])
@bot.message_handler(regexp='Получить')
def send_cat(message):
    send_random_cat(message.chat.id)


def check_if_startswith_cats(message):
    if(message.text is not None):
        return message.text.startswith('/cats')
    else:
        return False


# /catsN command, where N is number (e.g. /cats15)
@bot.message_handler(func=check_if_startswith_cats)
def send_cats(message):
    assert(len(message.text) >= len('/cats'))  # a bit of paranoia
    AMOUNT_DEFAULT = 10  # Default value for N

    rest = message.text[len('/cats'):]  # Getting string representing N
    if(len(rest) > 0):
        # Attempt to convert to int
        try:
            amount = int(rest)
            if(amount < 0):
                amount = AMOUNT_DEFAULT
        # In case convertion failed
        except ValueError as e:
            print(str(e) + "\nUser tried to use /cats{1} func".format(rest))
            # Failed_to_convert message
            bot.send_message(message.chat.id,
                             "К сожалению, мы не поняли команду /cats{1}."
                             "Used default command /cats10")
            amount = AMOUNT_DEFAULT
    else:
        amount = AMOUNT_DEFAULT

    # Now we have to send 'amount' cats
    assert(amount >= 0)
    for i in range(amount):
        send_random_cat(message.chat.id)


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


# /enable_cats_keyboard command
@bot.message_handler(commands=['enable_cats_keyboard'])
def enable_cats_keyboard(message):
    bot.send_message(message.chat.id, "Enjoy!",
                     reply_markup=advanced_keyboard())


# /disable_cats_keyboard command
@bot.message_handler(commands=['disable_cats_keyboard'])
def disable_cats_keyboard(message):
    bot.send_message(message.chat.id, "Here you are!",
                     reply_markup=simple_keyboard())


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
bot.polling(interval=10, timeout=40)
