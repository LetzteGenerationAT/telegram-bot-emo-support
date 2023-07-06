'''
Telegram bot to automatically send messages to emo support group
'''
import logging
import os
# pylint: disable=import-error
from dateutil import tz
from telegram import Update
from telegram.ext import filters, MessageHandler, CommandHandler, ApplicationBuilder, ContextTypes

DATE_FORMAT  = "%m/%d/%Y %H:%M:%S"
RESPONSE_MESSAGE_FILE = "response-message.txt"
CASE_NUMBER_FILE = "case-number.txt"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def _read_case_number() -> int:
    try:
        with open(CASE_NUMBER_FILE, "r", encoding="utf-8") as file:
            number =  file.read()
            return int(number)
    except FileNotFoundError :
        return 0


def _set_case_number(case_number: int) -> None:
    with open(CASE_NUMBER_FILE, "w", encoding="utf-8") as file:
        return file.write(str(case_number))
    

def _next_case_number() -> int:
    number = _read_case_number() + 1
    _set_case_number(number)
    return number

def _read_response_message() -> str:
    try:
        with open(RESPONSE_MESSAGE_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError :
        return "Thank you for reaching out!"

def _set_response_message(response_message) -> None:
    with open(RESPONSE_MESSAGE_FILE, "w", encoding="utf-8") as file:
        return file.write(response_message)

async def private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """A private message is received. Send a message to the group."""

    number = _next_case_number()

    local_zone = tz.tzlocal()
    dt_local = update.effective_message.date.astimezone(local_zone)
    dt_format = dt_local.strftime(DATE_FORMAT)

    await context.bot.send_message(
        chat_id=os.environ["EMO_SUPPORT_GROUP_ID"],
        text=f"""
Firstname: *{update.effective_user.first_name}*
Lastname: *{update.effective_user.last_name}*
Username: [{update.effective_user.username}](https://t.me/{update.effective_user.username})
Date: {dt_format}
Casenumber: {number}
               

{update.effective_message.text}""",
        parse_mode="markdown",
    )

    await context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=_read_response_message()
    )

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send the current response message.
    """
    await context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text="Current response message: " +_read_response_message()
    )

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Set the current response message to the text of the message except the command.
    """
    messsage = update.effective_message.text[12:]
    _set_response_message(messsage)
    await context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text="Set response message to: " + messsage
    )

def main():
    """
    Create the app.
    Add Handlers.
    Run Polling for messages.
    """
    app = ApplicationBuilder().token(os.environ['TELEGRAM_API_TOKEN']).build()

    private_message_handler = MessageHandler(
        filters.TEXT &
        (~filters.COMMAND) &
        filters.ChatType.PRIVATE, private_message
    )
    get_message_handler = CommandHandler(
        "get_message", get_message
    )
    set_message_handler = CommandHandler(
        "set_message", set_message
    )

    app.add_handler(private_message_handler)
    app.add_handler(get_message_handler)
    app.add_handler(set_message_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
