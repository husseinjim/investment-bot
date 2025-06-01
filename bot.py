from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

from handlers.deposit import deposit_handler
from handlers.claim import claim_handler

BOT_TOKEN = os.environ["BOT_TOKEN"]  # Railway injects this automatically

# Start message with menu buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💸 Claim Profit", callback_data="claim_profit")],
        [InlineKeyboardButton("🪙 Make Deposit", callback_data="make_deposit")],
        [InlineKeyboardButton("🎁 Referral Rewards", callback_data="referral_rewards")],
        [InlineKeyboardButton("📊 Profit Distribution", callback_data="profit_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to the Investment Bot! 🚀\n\nChoose an option below to get started 👇",
        reply_markup=reply_markup
    )

# Handle all button presses
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "claim_profit":
        await claim_handler(update, context)
    elif query.data == "make_deposit":
        # Instead of calling deposit_handler directly (which expects a message),
        # just send the same deposit message from here:
        address = "TLXrJrvBkZSJGsTFKrm29jq9wy1mgA7PmV"
        text = (
            f"🪙 *USDT Deposit Instructions*\n\n"
            f"Please send *USDT (TRC20)* to the following address:\n\n"
            f"`{address}`\n\n"
            f"✅ Minimum deposit: 50 USDT\n"
            f"✅ Maximum deposit: 50,000 USDT\n\n"
            f"⚠️ If you plan to deposit more than 50,000 USDT, please contact us first through our website.\n\n"
            f"_You will earn daily profit based on your deposit tier._"
        )
        await query.message.reply_markdown(text)
    elif query.data == "referral_rewards":
        await query.edit_message_text("🎁 Referral system is coming soon! Stay tuned.")
    elif query.data == "profit_info":
        await query.edit_message_text(
            "📊 *Profit Tiers:*\n"
            "🟢 $50 – $999 → 5%\n"
            "💰 $1,000 – $4,999 → 8%\n"
            "🪙 $5,000 – $9,999 → 10%\n"
            "🏦 $10,000+ → 13%\n\n"
            "_Profits are claimable once per day._",
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deposit", deposit_handler))
    app.add_handler(CommandHandler("claim", claim_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
