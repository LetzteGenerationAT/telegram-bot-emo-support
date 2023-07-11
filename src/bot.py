"""
Telegram bot to automatically send messages to emo support group
"""
import logging
import os
# pylint: disable=import-error
from dateutil import tz
from telegram import Update
from telegram.ext import filters, MessageHandler, CommandHandler, ApplicationBuilder, ContextTypes

from config import config

DATE_FORMAT  = "%m/%d/%Y %H:%M:%S"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def _create_group_message(update:Update, dt_format: str, number: int):
    return f"""
Firstname: *{update.effective_user.first_name}*
Lastname: *{update.effective_user.last_name}*
Username: [{update.effective_user.username}](https://t.me/{update.effective_user.username})
Date: {dt_format}
Casenumber: {number}
            

{update.effective_message.text}"""

async def private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """A private message is received. Send a message to the group."""

    number = config.next_case_number()

    local_zone = tz.tzlocal()
    dt_local = update.effective_message.date.astimezone(local_zone)
    dt_format = dt_local.strftime(DATE_FORMAT)


    if update.effective_user.username is None:
        await context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="""Please provide a *username* so that we can contact you. \n
[Settings](tg://settings) \n
[How to add a username in telegram](https://www.swipetips.com/how-to-add-a-username-in-telegram/) \n
[FAQ - Telegram username](https://telegram.org/faq#usernames-and-t-me) \n""",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
    else:
        await context.bot.send_message(
            chat_id=os.environ["EMO_SUPPORT_GROUP_ID"],
            text=_create_group_message(update, dt_format, number),
            parse_mode="markdown",
        )
        await context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=config.get_response_message()
        )

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send the current response message.
    """
    await context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text="Current response message: " +config.get_response_message()
    )

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Set the current response message to the text of the message except the command.
    """
    messsage = update.effective_message.text[12:]
    config.set_response_message(messsage)
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

    config.write_config()

if __name__ == '__main__':
    main()
