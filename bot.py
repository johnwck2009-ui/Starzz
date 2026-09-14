import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

BOT_NAME = "Starz Promosyon"

PICKS = [
    "Try a new hobby today.",
    "Listen to a song you have never heard before.",
    "Send a kind message to someone you appreciate.",
    "Take a short walk and explore somewhere nearby.",
    "Learn one interesting fact today.",
    "Put your phone away for 15 minutes and relax.",
    "Write down one thing you want to accomplish this week.",
    "Watch a movie you have never seen before.",
    "Try a food you have not had recently.",
    "Do something small that makes you happy.",
]


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Random Pick", callback_data="pick")],
        [InlineKeyboardButton("About Starz", callback_data="about")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Welcome to {BOT_NAME}.\n\n"
        "Need something random? Tap Random Pick and see what you get."
    )
    await update.message.reply_text(text, reply_markup=menu())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "pick":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Another One", callback_data="pick")],
            [InlineKeyboardButton("Back", callback_data="back")],
        ])
        await query.edit_message_text(
            f"Your random pick:\n\n{random.choice(PICKS)}",
            reply_markup=keyboard,
        )
    elif query.data == "about":
        await query.edit_message_text(
            f"{BOT_NAME}\n\nA simple bot for random ideas and little surprises.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="back")]
            ]),
        )
    elif query.data == "back":
        await query.edit_message_text(
            f"Welcome to {BOT_NAME}.\n\nNeed something random? Tap Random Pick and see what you get.",
            reply_markup=menu(),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use /start to open the menu and get a random pick."
    )


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()


if __name__ == "__main__":
    main()
