import os
import telebot
from telebot import types
import shutil

total_b, used_b, free_b = shutil.disk_usage('.')
gb = 10**9
bot = telebot.TeleBot("")
torrentName = ''
downloadPlace = 'downloads/'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    findTorrent = types.KeyboardButton("поиск торрента")
    countcap = types.KeyboardButton("gb")
    markup.add(findTorrent, countcap)
    bot.send_message(message.chat.id, "значит ситуация следующая: кидаешь сюда торент файл - скачивает его, скинешь ссылку на магнит линк качает по нему. кайфуй будь пусей.", parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    global downloadPlace
    if message.text == "поиск торрента":
        bot.send_message(message.chat.id, "из-за роскомнадзора поисковик находиться в другом боте - @searchformov_bot")
    elif message.text == "gb":
        total_b, used_b, free_b = shutil.disk_usage('.')                        
        bot.send_message(message.chat.id, "На диске осталось места в гб: {:6.2f}".format(free_b/gb)) 
    else:
        bot.send_message(message.chat.id, "загрузка началась")
        os.system(f'aria2c.exe --seed-time=0   {message.text} -d {downloadPlace}')
        total_b, used_b, free_b = shutil.disk_usage('.')
        bot.send_message(message.chat.id, "На диске осталось места в гб: {:6.2f}".format(free_b/gb))
        bot.send_message(message.chat.id, "готово")


@bot.message_handler(content_types=['document'])
def handle_file(message):
    global downloadPlace
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = '' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "файл принял, начал скачивать,чиииль, я напишу как закончу")
        torrentName = ''
        for f in os.listdir():
	        if f.endswith('.torrent'):
		        torrentName = f
		        break
        os.system(f'aria2c.exe --seed-time=0  {f} -d {downloadPlace}')
        bot.send_message(message.chat.id, 'файл скачался')
        os.system('del *.torrent')
        total_b, used_b, free_b = shutil.disk_usage('.')
        bot.send_message(message.chat.id, "На диске осталось места в гб: {:6.2f}".format(free_b/gb))
    except Exception as e:
        bot.reply_to(message, e)

bot.polling(none_stop=True, interval=2)
