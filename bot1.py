import logging
import os
from shutil import move
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)
import requests, json

login_id = "b4ea1e08036008d3f7f8"
key_id = "4yQokdMp9rtKgXV"
session = requests.Session()

def get_url():
    cred = { "login":login_id,"key":key_id }
    response = session.get("https://api.strtape.tech/file/ul?",headers=cred,)
    data = json.loads(response.text)
    ul_url = data.get('result').get('url')
    return ul_url

ul_url = get_url()

def ul_video(ul_url,files):
    headers = { "login":login_id,"key":key_id }
    response = session.post(ul_url,files = files,headers=headers)
    data = json.loads(response.text)
    url = data.get('result').get('url')
    #size_in_bytes = data.get('result').get('size')
    #mb = int(size_in_bytes)/1024/1024
    return url
    
def filemoon(url):
    os.system(f"curl -d 'key=31525r7d0x3h23qpfytj9&url={url}' -H 'Content-Type: application/x-www-form-urlencoded' -X POST https://filemoonapi.com/api/remote/add")
    #file = open("/content/drive/MyDrive/streamlinks.txt","a+")
    file = open("/sdcard/tg/streamlinks.txt","a+")
    file.writelines(f"\n{url}")
    file.close()
   
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "6197871086:AAG4t6pvjyHlpa7fg5jvNl6ANgDijhAg_Kg"
BASE_URL = "http://0.0.0.0:8081/bot"
##OUTPUT_DIR = "/content/drive/MyDrive/scr/"
OUTPUT_DIR = "/sdcard/tg/"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )

# Keep track of the progress while downloading
async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Downloading!")
    document = update.message.video
    file = await context.bot.get_file(document)
    await update.message.reply_text(f"File {document.file_name} downloaded.\nNow moving.")
    move(file.file_path.lstrip(TOKEN),f"{OUTPUT_DIR}{document.file_name}")
    await update.message.reply_text(f"File moved.\nLocation: {OUTPUT_DIR}{document.file_name}")
    path = f"{OUTPUT_DIR}{document.file_name}"
    with open(path, "rb") as file:
        files = {'file': file}
        url = ul_video(ul_url,files)
        await update.message.reply_text(f"Link : {url}")
        filemoon(url)
        await update.message.reply_text(f"File Uploaded on filemoon")

async def document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Downloading!")
    document = update.message.document
    file = await context.bot.get_file(document)
    await update.message.reply_text(f"File {document.file_name} downloaded.\nNow moving.")
    move(file.file_path.lstrip(TOKEN),f"{OUTPUT_DIR}{document.file_name}")
    await update.message.reply_text(f"File moved.\nLocation: {OUTPUT_DIR}{document.file_name}")
    path = f"{OUTPUT_DIR}{document.file_name}"
    with open(path, "rb") as file:
        files = {'file': file}
        url = ul_video(ul_url,files)
        await update.message.reply_text(f"Link : {url}")


def main() -> None:
    application = Application.builder().token(TOKEN).base_url(BASE_URL).base_file_url("").read_timeout(864000).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, video))
    application.add_handler(MessageHandler(filters.Document.ALL, document))
    application.run_polling()

if __name__ == "__main__":
    main()
