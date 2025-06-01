from telegram import Update
from telegram.ext import ContextTypes

# ✅ Updated USDT TRC20 wallet address
USDT_TRC20_ADDRESS = "TLXrJrvBkZSJGsTFKrm29jq9wy1mgA7PmV"

async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    message = (
        f"💰 *USDT Deposit Instructions*\n\n"
        f"Please send *USDT (TRC20)* to the following address:\n\n"
        f"`{USDT_TRC20_ADDRESS}`\n\n"
        f"🔁 After sending, keep the TX hash ready. In future versions, "
        f"you'll be able to submit it for balance verification.\n\n"
        f"✅ Minimum deposit: 50 USDT\n"
        f"💰 Maximum deposit: 50,000 USDT\n\n"
        f"⚠️ If you plan to deposit more than 50,000 USDT, please contact us first through our website.\n\n"
        f"_You will earn daily profit based on your deposit tier._"
    )

    await update.message.reply_markdown(message)
