import logging
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN: Final = ' '
BOT_USERNAME: Final = " "

logging.basicConfig(format='%(levelname)s - (%(asctime)s) - %(message)s - (Line: %(lineno)d) -[%(filename)s]',
                    datefmt='%H:%M:%S',
                    encoding='utf-8',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Command Handlers
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s started Bot", update.effective_user.username)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome!",
        reply_to_message_id=update.effective_message.id
    )


async def dice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s want dice", update.effective_user.username)
    await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s want help", update.effective_user.username)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""Here is the help message for you! :
            /start->Will start bot for you
            /dice ->Will send you a dice
            /help -> Will Show Me Again!""",
        reply_to_message_id=update.effective_message.id
    )


async def repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s want to repeat something", update.effective_user.username)
    text = " " .join(context.args)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id
    )


# Message Handlers
def generate_response(text: str) -> str:
    parsed_text = text.lower().strip()
    if "hello" in parsed_text:
        return "Hello to you!"
    if "how are you" in parsed_text:
        return "Good! what about you?"
    if "good" in parsed_text:
        return "Amazing! i'm glad to hear that!!"


async def response_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s want response to message ", update.effective_user.username)
    chat_type = update.effective_chat.type
    if BOT_USERNAME not in update.effective_message.text and chat_type == "group":
        return
    answer_text = generate_response(update.effective_message.text)
    user_first_name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer_text + f"\n{user_first_name}",
        reply_to_message_id=update.effective_message.id
    )


async def echo_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("user %s want response to sticker", update.effective_user.username)
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=update.effective_message.sticker,
        reply_to_message_id=update.effective_message.id
    )


# Error Handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("error : [%s] on %s update ", context.error,update)

if __name__ == '__main__':
    logger.info("Building Bot...")
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler('start', start_handler))
    bot.add_handler(CommandHandler('dice', dice_handler))
    bot.add_handler(CommandHandler('help', help_handler))
    bot.add_handler(CommandHandler('repeat', repeat_handler))
    bot.add_handler(MessageHandler(filters.TEXT, response_to_message))
    bot.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))
    bot.add_error_handler(error_handler)

    # Bot Start
    logger.info("Bot Start polling ...")
    bot.run_polling()
