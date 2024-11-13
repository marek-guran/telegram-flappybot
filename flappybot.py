import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest
from telegram.error import RetryAfter

# Define the bot token
TOKEN = ''

# Helper function to generate buttons with user-specific callback data
def generate_main_buttons(user_id):
    return [
        [InlineKeyboardButton("Play Flappy PEPE", url="http://t.me/flappypepecoin_bot/flappy_pepe")],
        [InlineKeyboardButton("Pepecoin.org", url="https://pepecoin.org/"), InlineKeyboardButton("Faucets", callback_data=f'faucets_{user_id}')],
        [InlineKeyboardButton("Explorers", callback_data=f'explorers_{user_id}'), InlineKeyboardButton("Community", callback_data=f'community_{user_id}'), InlineKeyboardButton("Guides", callback_data=f'guides_{user_id}')]
    ]

# Generate user-specific buttons for Explorers
def generate_explorers_buttons(user_id):
    return [
        [InlineKeyboardButton("PepeExplorer", url="https://pepeexplorer.com/"), InlineKeyboardButton("PepeBlocks", url="https://pepeblocks.com/"), InlineKeyboardButton("CoinExplorer", url="https://www.coinexplorer.net/PEP/")],
        [InlineKeyboardButton("Back", callback_data=f'main_menu_{user_id}')]
    ]

# Generate user-specific buttons for Faucets
def generate_faucets_buttons(user_id):
    return [
        [InlineKeyboardButton("Pepeblocks", url="https://faucet.pepeblocks.com/"), InlineKeyboardButton("Ravener", url="https://pepe.ravener.is-a.dev/"), InlineKeyboardButton("Stakecube", url="https://stakecube.net/app/community")],
        [InlineKeyboardButton("Back", callback_data=f'main_menu_{user_id}')]
    ]

# Generate user-specific buttons for Community
def generate_community_buttons(user_id):
    return [
        [InlineKeyboardButton("Telegram", url="https://t.me/PepecoinGroup"), InlineKeyboardButton("Discord", url="https://discord.gg/pepecoin"), InlineKeyboardButton("Reddit", url="https://reddit.com/r/Pepecoin")],
        [InlineKeyboardButton("Back", callback_data=f'main_menu_{user_id}')]
    ]

# Generate user-specific buttons for Guides
def generate_guides_buttons(user_id):
    return [
        [InlineKeyboardButton("Pepelum Guides", url="https://pepelum.site/")],
        [InlineKeyboardButton("Wallets", url="https://pepelum.site/?p=wallets"), InlineKeyboardButton("Mining", url="https://pepelum.site/?p=mining")],
        [InlineKeyboardButton("Buying Ᵽepecoin", url="https://pepelum.site/?p=getpepecoin"), InlineKeyboardButton("Tip Bots", url="https://pepelum.site/?p=bots")],
        [InlineKeyboardButton("Back", callback_data=f'main_menu_{user_id}')]
    ]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the ID of the user who started the bot
    user_id = update.message.from_user.id

    # Generate buttons specific to this user
    keyboard = InlineKeyboardMarkup(generate_main_buttons(user_id))
    
    await update.message.reply_text('Choose an option:', reply_markup=keyboard)

# Button press handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    # Extract the button's original user ID from the callback data
    callback_data = query.data
    original_user_id = int(callback_data.split('_')[-1])  # Extract the user ID from the callback_data

    # Check if the user pressing the button is the same as the one who started the interaction
    if user_id != original_user_id:
        # Send the action in a DM to the user pressing the button along with the main buttons
        keyboard = InlineKeyboardMarkup(generate_main_buttons(user_id))
        await context.bot.send_message(user_id, text="Choose an option:", reply_markup=keyboard)
        await query.answer("Your options just flapped their way into your DMs! Check 'em out!", show_alert=True)
        return

    await query.answer()

    try:
        # Show buttons based on the user's selection
        if callback_data.startswith('flappy_pepe'):
            await query.message.reply_text('http://t.me/flappypepecoin_bot/flappy_pepe')
        elif callback_data.startswith('explorers'):
            keyboard = InlineKeyboardMarkup(generate_explorers_buttons(original_user_id))
            await query.message.edit_text('Choose an explorer:', reply_markup=keyboard)
        elif callback_data.startswith('faucets'):
            keyboard = InlineKeyboardMarkup(generate_faucets_buttons(original_user_id))
            await query.message.edit_text('Choose a faucet:', reply_markup=keyboard)
        elif callback_data.startswith('community'):
            keyboard = InlineKeyboardMarkup(generate_community_buttons(original_user_id))
            await query.message.edit_text('Choose a community platform:', reply_markup=keyboard)
        elif callback_data.startswith('guides'):
            keyboard = InlineKeyboardMarkup(generate_guides_buttons(original_user_id))
            await query.message.edit_text('Choose a guide:', reply_markup=keyboard)
        elif callback_data.startswith('main_menu'):
            keyboard = InlineKeyboardMarkup(generate_main_buttons(original_user_id))
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
