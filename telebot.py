import os
import telethon
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
file = open('city.txt')


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Привет! Я знаю наизусть все населённые пункты России. Введи /play, чтобы сыграть со мной в города😏')
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/play'))
async def play(event):
        await event.respond('Начнём! Ты первый😋')
        @bot.on(events.NewMessage)
        async def game(event):
            lis = list()
            message = event.raw_text
            with open('city.txt') as same_file:
                text = same_file.read()
                if text.count(message) > 0:
                    if lis.count(message) == 0:
                        await event.respond('hi')
                        let = message[len(message)-1]
                        await event.respond(getword(let, lis))
                else:
                    await event.respond('Насколько я знаю, такого населённого пункта не существует в России. Попробуй еще раз😉')
                    raise events.StopPropagation

def getword(letter, used_lis):
    for line in file:
        if line[0] == letter:
            if used_lis.count(line) == 0:
                return line
                break


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
