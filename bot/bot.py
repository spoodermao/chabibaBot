#!/bin/python

from dotenv import dotenv_values
TOKEN = dotenv_values(".env")['TOKEN']

import logging

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

print('khay')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def chabiba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    admins = await context.bot.get_chat_administrators(chat_id)

    [await context.bot.send_message(chat_id, text= "["+" ](tg://user?id="+str(x.user.id)+")", parse_mode="Markdown") for x in admins]


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    chabiba_handler = CommandHandler('chabiba', chabiba)

    application.add_handler(chabiba_handler)

    application.run_polling()
