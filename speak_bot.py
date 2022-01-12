import logging
import time
from logging import getLogger, StreamHandler, DEBUG

from discord import FFmpegPCMAudio, Client
from discord.channel import VoiceChannel
import pyttsx3

from config import TOKEN

# Botで使用
client = Client()
voiceChannel = None

# 音声作成で使用
engine = pyttsx3.init()

# ログ出力で使用
logger = getLogger(__name__)
logger.setLevel(DEBUG)
s_handler = StreamHandler()
s_handler.setLevel(DEBUG)
s_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(s_handler)


@client.event
async def on_ready():
    engine.say('Login')
    engine.runAndWait()


@client.event
async def on_message(message):
    global voiceChannel

    if message.author.bot:
        return

    if not voiceChannel:
        if message.content == 'あうあう':
            voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
            await message.channel.send('読み上げ開始')
            speak(msg='読み上げ開始')
            return
    else:
        if message.content == 'あいあい':
            await message.channel.send('読み上げ終了')
            speak(msg='読み上げ終了')
            time.sleep(3)
            voiceChannel.stop()
            await voiceChannel.disconnect()
            voiceChannel = None
            return
        else:
            speak(msg=message.content)
            return


def speak(msg):
    mp3_file_path = f'msg.mp3'
    engine.save_to_file(msg, mp3_file_path)
    engine.runAndWait()
    voiceChannel.play(FFmpegPCMAudio(executable=r'ffmpeg/ffmpeg.exe', source=mp3_file_path))
    logger.info(f'speak: {msg}')


client.run(TOKEN)
