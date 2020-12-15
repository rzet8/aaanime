import config
import threading
import ast

import telebot
import pymysql

from telebot import TeleBot

bot = TeleBot(config.TOKEN)

db = pymysql.connect("us-cdbr-east-02.cleardb.com", "bed556e7305b73", "df0e3315", "heroku_80ac70680d841f5")
c = db.cursor()
lock = threading.Lock()

def to_smile(num):
    num = str(num).replace("0", "0️⃣").replace("1", "1️⃣").replace("2", "2️⃣").replace("3", "3️⃣").replace("4", "4️⃣").replace("5", "5️⃣").replace("6", "6️⃣").replace("7", "7️⃣").replace("8", "8️⃣").replace("9", "9️⃣")
    return num

def off_command(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAKEG1_ZI27kTQOjykiao66bI_BinjibAAJ8AAMn9rADzjQEaIklvjMeBA")
    bot.send_message(message.chat.id, "Упс!\nКажется комманда отключена")

def error(message, error):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAKDq1_ZDUmG0cRQf6t6OuvHhX9tQYsOAAKCAAMn9rADBItqVKbyvpMeBA")
    bot.send_message(message.chat.id, error+"\n\nПодробная инфа про комманду - /help")

@bot.message_handler(commands=['start', 'list', 'add', 'set', 'del', 'info', 'help'])
def start_message(message):
    if message.text == "/start":
        try:
            with lock:
                c.execute(f"""INSERT INTO 
                `user`(`id`, `anime`) 
                VALUES ('{message.chat.id}','[["test", "test"], ["test", "test"]]')""")
                db.commit()
        except:
            pass
        
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAKDnF_ZC45cP7-nwVs8pYosf8I0OLv6AAJcAAMn9rADLh2BmECmiaEeBA')
        bot.send_message(message.chat.id, f'Привет {message.chat.first_name} !')
        bot.send_message(message.chat.id, f'Мои команды /help !')

    elif message.text == "/info":
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAKEBF_ZHCFMSsNGsYpsGC0witNXXmxwAAJYAAMn9rADd7S8n2OEelQeBA")
        bot.send_message(message.chat.id, "🌸 Контакты\ninst: @rzet.tk\nTelegram: @rzet8\nVk: @rzet8\n\nБот написан на 🐍 Python3\nGithub - github.com/rzet8/aaanime")
    
    elif message.text == "/list":
        with lock:
            c.execute(f"SELECT * FROM `user` WHERE `id`= '{message.chat.id}'")
            anime = ast.literal_eval(c.fetchone()[1])

        len_anime = to_smile(len(anime))

        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAKDz1_ZEn08jP0AAQXXo8SoHI4aNOWN0QACSgADJ_awA-HVfXIqK2CoHgQ")
        bot.send_message(message.chat.id, f"🌸 В вашем списке {len_anime} аниме !")

        for i in range(len(anime)):
            bot.send_message(message.chat.id, f"◽️ {i+1}. {anime[i][0]} - {anime[i][1]}")
    
    elif "/add" in message.text:
        name = message.text.replace("/add ", "")
        if name != "/add":

            with lock:
                c.execute(f"SELECT * FROM `user` WHERE `id`= '{message.chat.id}'")
                anime = ast.literal_eval(c.fetchone()[1])

            anime = anime + [[name, "непросмотрено"]]
            anime = str(anime).replace("'", '"')

            with lock:
                c.execute(f"""UPDATE `user` SET `anime`='{anime}' WHERE `id` = {message.chat.id}""")
                db.commit()

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAKDt1_ZDdzxRbEIyE7Vv7zV_gtBgqy4AAJ7AAMn9rADlGc4CzFlXPoeBA")
            bot.send_message(message.chat.id, f"Вы добавили - {name}")
        
        else:
            error(message, "Вы не дали названия\n\nПример: /add name")
        
    elif "/set" in message.text:
        id_a = message.text.split(" ")[1]
        st_a = message.text.split(" ")[2]

        if st_a == "+":
            er = 0
            st_a = "просмотрено"

        elif st_a == "-":
            er = 0
            st_a = "непросмотрено"

        else:
            er = 1
            error(message, "Неправильный знак\nДоступно +, -")

        if er == 0:
            with lock:
                c.execute(f"SELECT * FROM `user` WHERE `id`= '{message.chat.id}'")
                anime = ast.literal_eval(c.fetchone()[1])
            
            try:
                anime[int(id_a)-1][1] = st_a
                anime = str(anime).replace("'", '"')
                with lock:
                    c.execute(f"""UPDATE `user` SET `anime`='{anime}' WHERE `id` = {message.chat.id}""")
                    db.commit()
            
                bot.send_message(message.chat.id, "🌸 Успешно!")

            except:
                error(message, "Такой id не найден!")

    elif "/del" in message.text:
        try:
            id_a = message.text.split(" ")[1]

            with lock:
                c.execute(f"SELECT * FROM `user` WHERE `id`= '{message.chat.id}'")
                anime = ast.literal_eval(c.fetchone()[1])

            if id_a ==  "all":
                anime = []

            else:
                del anime[int(id_a)-1]

            anime = str(anime).replace("'", '"')

            with lock:
                c.execute(f"""UPDATE `user` SET `anime`='{anime}' WHERE `id` = {message.chat.id}""")
                db.commit()

            bot.send_message(message.chat.id, "🌸 Успешно!")

        except:
            error(message, "Такой id не найден!")
    
    elif message.text == "/help":
        off_command(message)
        

if __name__ == "__main__":
    bot.polling(True)