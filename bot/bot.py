#!/bin/python
import pymongo
import logging
from os import getenv
import requests
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ChatMemberHandler

TOKEN = getenv("TOKEN")
username = getenv("MANGODB_USERNAME")
password = getenv("MANGODB_PASSWORD")

print('khay')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
    
client = pymongo.MongoClient("mongodb+srv://"+username+":"+password+"@chabibacluster.wklsylj.mongodb.net/?retryWrites=true&w=majority")
db = client.chabibaDB

async def chabiba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    admins = await context.bot.get_chat_administrators(chat_id)

    #[await context.bot.send_message(chat_id, text= "["+" ](tg://user?id="+str(x.user.id)+")", parse_mode="Markdown") for x in admins]
    await context.bot.send_message(chat_id, text=' '.join([ "["+str(x.user.username or x.user.first_name+(" "+x.user.last_name if x.user.last_name else  "") )+"](tg://user?id="+str(x.user.id)+")" for x in admins ]), parse_mode="Markdown")

async def fiha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    collection = db[str(chat_id)]

    user = update.effective_user
    print(user)
    collection.replace_one({'id':user.id},
        {
            'id': user.id,
            'is_bot': user.is_bot,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }, upsert=True)
    await context.bot.send_message(chat_id, text="sa7it khay", parse_mode="Markdown")
   
async def mafihach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    collection = db[str(chat_id)]

    user = (update.effective_user)

    collection.delete_one({'id': user.id})
    await context.bot.send_message(chat_id, text=":'( I'm صاد", parse_mode="Markdown")

async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    collection = db[str(chat_id)]

    await context.bot.send_message(chat_id, text=' '.join([ "["+str(x['username'] or x['first_name']+(" "+x['last_name'] if x['last_name'] else "" ) )+"](tg://user?id="+str(x['id'])+")" for x in collection.find() ]), parse_mode="Markdown")

async def flush(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    collection = db[str(chat_id)]
     
    admins = await context.bot.get_chat_administrators(chat_id)
    user = (update.effective_user)
    if any(user==x.user for x in admins):
        collection.drop()       
        await context.bot.send_message(chat_id, text="fffllluuussssssshhhhhhhh", parse_mode="Markdown")
    else:
        await context.bot.send_message(chat_id, text="Be admin", parse_mode="Markdown")

#async def dakhel_kharej(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
# (chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    #print(update.chat_member)
    #old_member, new_member = update.chat_member.difference().get("is_member", (None, None))
    

    
if __name__ == '__main__':
  #while True:
    url = "https://api.telegram.org/bot"+TOKEN+"/getMe"
    req = requests.get(url)
    if req:
        application = ApplicationBuilder().token(TOKEN).build()
        chabiba_handler = CommandHandler('chabiba', chabiba)
        fiha_handler = CommandHandler('fiha', fiha)
        mafihach_handler = CommandHandler('mafihach', mafihach)
        everyone_handler = CommandHandler('everyone', everyone)
        flush_handler = CommandHandler('flush', flush)

        #dakhel_kharej = ChatMemberHandler(dakhel_kharej, 1, block=True)
        #application.add_handler(dakhel_kharej)


        application.add_handler(chabiba_handler)
        application.add_handler(fiha_handler)
        application.add_handler(mafihach_handler)
        application.add_handler(everyone_handler)
        application.add_handler(flush_handler)

        application.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        print("There is another instance running")
        exit()
