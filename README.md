# CatBot
HSE task
I've chosen task 50
>>Напишите бот для телеграмма, отправляющий случайные фотографии котиков из списка по запросу. Папка с фотографиями задается как параметр командной строки.
>>В интерфейсе должна быть одна кнопка: "получить".
>>Используйте библиотеку https://github.com/eternnoir/pyTelegramBotAPI

To run bot call:
$ python catbot.py

To choose directories with cat images call:
$ python catbot.py C:\Users\Uliana\Pictures\folder1\ C:\Users\Uliana\Favorites\ media\
( If omited, used default folder media\ )

To proxibit saving photos users send to bot call:
$ python catbot.py -dontsave
Or, to choose custom directories:
$ python catbot.py C:\Users\Uliana\Pictures\folder1\ C:\Users\Uliana\Favorites\ media\ -dontsave