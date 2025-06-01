from telegram import Update
from telegram.ext import ContextTypes
from handlers.setbalance import user_balances  # shared balances

async def claim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.effective_message  # ✅ works for both /claim and button

    if user_id not in user_balances:
        await message.reply_text(
            "⚠️ No active balance found.\nPlease deposit and submit your TX hash using /submit first."
        )
        return

    balance = user_balances[user_id]

    # Tier logic
    if 50 <= balance < 1000:
        rate = 0.05
    elif 1000 <= balance < 5000:
        rate = 0.08
    elif 5000 <= balance < 10000:
        rate = 0.10
    elif balance >= 10000:
        rate = 0.13
    else:
        await message.reply_text("⚠️ Your balance is below the minimum threshold.")
        return

    profit = round(balance * rate, 2)

    await message.reply_text(
        f"💸 *Profit Claimed!*\n\n"
        f"Your current balance: *{balance} USDT*\n"
        f"Daily rate: *{int(rate * 100)}%*\n"
        f"Today's profit: *{profit} USDT*\n\n"
        f"_Come back in 24h to claim again._",
        parse_mode="Markdown"
    )
