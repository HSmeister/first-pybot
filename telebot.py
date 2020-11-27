import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Привет! Я знаю наизусть все населённые пункты России. Введи /play, чтобы сыграть со мной в города😏')
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/play'))
async def play(event):
    await event.respond('Начнём! Ты первый😋')
    raise events.StopPropagation


@bot.on(events.NewMessage)
async def game(event):
    sender_id = event.sender_id
    with open(f'{sender_id}.txt', 'a') as storage:
        message = event.raw_text
        with open('city.txt') as same_file:
            same_file.seek(0)
            text = same_file.read()
            if text.count(message) > 0:
                if checklist(sender_id, message):
                    let = getletter(message)
                    storage.write(message + '\n')
                    answer = getword(let, sender_id)
                    storage.write(answer + '\n')
                    await event.respond(answer)
                else:
                    await event.respond('Такое слово мы уже называли. Давай новое!😁')
            else:
                await event.respond('Насколько я знаю, такого населённого пункта не существует в России. Попробуй еще раз😉')
                raise events.StopPropagation


def checklist(sen_id, chewo):
    with open(f'{sen_id}.txt', 'r') as list_file:
        list_file.seek(0)
        used_words = list_file.read()
        if used_words.count(chewo) > 0:
            return False
        return True


def getletter(word):
    lastlet = word[len(word)-1]
    if lastlet in ['ь', 'ъ', 'ы']:
        lastlet = word[len(word)-2]
    return lastlet


def getword(letter, sen_id):
    file = open('city.txt')
    for line in file:
        if line[0] == letter.upper():
            if checklist(sen_id, line):
                return line
                break
    file.close()


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
