import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest

# Define the bot token
TOKEN = 'TOKEN'

# Define the buttons in the specified layout with additional rows
buttons = [
    [InlineKeyboardButton("Flappy PEPE", callback_data='flappy_pepe'), InlineKeyboardButton("Pepelum", url="http://pepelum.site/")],
    [InlineKeyboardButton("Pepeblocks Faucet", url="https://faucet.pepeblocks.com/"), InlineKeyboardButton("Ravener Faucet", url="https://pepe.ravener.is-a.dev/")],
    [InlineKeyboardButton("Stakecube Faucet", url="https://stakecube.net/app/community"), InlineKeyboardButton("Pepecoin.org", url="https://pepecoin.org/")],
    [InlineKeyboardButton("Pepe Explorer", url="https://pepeexplorer.com/"), InlineKeyboardButton("Pepeblocks", url="https://pepeblocks.com/")],
    [InlineKeyboardButton("Pepecoin Telegram Group", url="https://t.me/PepecoinGroup")],
    [InlineKeyboardButton("Discord", url="https://discord.gg/pepecoin"), InlineKeyboardButton("Reddit", url="https://reddit.com/r/Pepecoin")]
]

# The rest of the code remains the same

# The rest of the code remains the same

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text('Choose an option:',reply_markup=keyboard)

# Button press handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'flappy_pepe':
        await query.message.reply_text('http://t.me/flappypepecoin_bot/flappy_pepe')

# Main function to start the bot
def main() -> None:
    request = HTTPXRequest(connect_timeout=10.0, read_timeout=20.0)
    application = Application.builder().token(TOKEN).request(request).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
