import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest
from telegram.error import RetryAfter

# Define the bot token
TOKEN = 'token'

# Define the initial buttons layout
main_buttons = [
    [InlineKeyboardButton("Play Flappy PEPE", callback_data='flappy_pepe')],
    [InlineKeyboardButton("Pepecoin.org", url="https://pepecoin.org/"), InlineKeyboardButton("Faucets", callback_data='faucets')],
    [InlineKeyboardButton("Explorers", callback_data='explorers'), InlineKeyboardButton("Community", callback_data='community'), InlineKeyboardButton("Guides", callback_data='guides')]
]

# Define the buttons for Explorers
explorers_buttons = [
    [InlineKeyboardButton("PepeExplorer", url="https://pepeexplorer.com/"), InlineKeyboardButton("PepeBlocks", url="https://pepeblocks.com/"), InlineKeyboardButton("CoinExplorer", url="https://www.coinexplorer.net/PEP/")],
    [InlineKeyboardButton("Back", callback_data='main_menu')]
]

# Define the buttons for Faucets
faucets_buttons = [
    [InlineKeyboardButton("Pepeblocks", url="https://faucet.pepeblocks.com/"), InlineKeyboardButton("Ravener", url="https://pepe.ravener.is-a.dev/"), InlineKeyboardButton("Stakecube", url="https://stakecube.net/app/community")],
    [InlineKeyboardButton("Back", callback_data='main_menu')]
]

# Define the buttons for Community
community_buttons = [
    [InlineKeyboardButton("Telegram", url="https://t.me/PepecoinGroup"), InlineKeyboardButton("Discord", url="https://discord.gg/pepecoin"), InlineKeyboardButton("Reddit", url="https://reddit.com/r/Pepecoin")],
    [InlineKeyboardButton("Back", callback_data='main_menu')]
]

# Define the buttons for Guides
guides_buttons = [
    [InlineKeyboardButton("Pepelum Guides", url="https://pepelum.site/")],
    [InlineKeyboardButton("Wallets", url="https://pepelum.site/?p=wallets"), InlineKeyboardButton("Mining", url="https://pepelum.site/?p=mining")],
    [InlineKeyboardButton("Buying Ᵽepecoin", url="https://pepelum.site/?p=getpepecoin"), InlineKeyboardButton("Tip Bots", url="https://pepelum.site/?p=bots")],
    [InlineKeyboardButton("Back", callback_data='main_menu')]
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Store the ID of the user who started the bot
    context.user_data['user_id'] = update.message.from_user.id
    keyboard = InlineKeyboardMarkup(main_buttons)
    await update.message.reply_text('Choose an option:', reply_markup=keyboard)

# Button press handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    # Check if the user pressing the button is the same as the one who started the interaction
    if 'user_id' in context.user_data and user_id != context.user_data['user_id']:
        # Ignore the button press if it's not the original user
        return
    
    await query.answer()

    try:
        # Show buttons based on the user's selection
        if query.data == 'flappy_pepe':
            await query.message.reply_text('http://t.me/flappypepecoin_bot/flappy_pepe')
        elif query.data == 'explorers':
            keyboard = InlineKeyboardMarkup(explorers_buttons)
            await query.message.edit_text('Choose an explorer:', reply_markup=keyboard)
        elif query.data == 'faucets':
            keyboard = InlineKeyboardMarkup(faucets_buttons)
            await query.message.edit_text('Choose a faucet:', reply_markup=keyboard)
        elif query.data == 'community':
            keyboard = InlineKeyboardMarkup(community_buttons)
            await query.message.edit_text('Choose a community platform:', reply_markup=keyboard)
        elif query.data == 'guides':
            keyboard = InlineKeyboardMarkup(guides_buttons)
            await query.message.edit_text('Choose a guide:', reply_markup=keyboard)
        elif query.data == 'main_menu':
            keyboard = InlineKeyboardMarkup(main_buttons)
            await query.message.edit_text('Choose an option:', reply_markup=keyboard)
        
        # Add a delay to avoid hitting the rate limit
        await asyncio.sleep(0.1)

    except RetryAfter as e:
        logging.warning(f"Rate limit exceeded. Retrying in {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        await button(update, context)

# Main function to start the bot
def main() -> None:
    request = HTTPXRequest(connect_timeout=10.0, read_timeout=20.0)
    application = Application.builder().token(TOKEN).request(request).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
