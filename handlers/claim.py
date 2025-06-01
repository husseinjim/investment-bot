from telegram import Update
from telegram.ext import ContextTypes
from handlers.setbalance import user_balances  # ✅ Import shared balances

async def claim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user has a balance
    if user_id not in user_balances:
        await update.message.reply_text(
            "⚠️ No active balance found.\nPlease deposit and submit your TX hash using /submit first."
        )
        return

    balance = user_balances[user_id]

    # Calculate profit based on tiers
    if 50 <= balance < 1000:
        rate = 0.05
    elif 1000 <= balance < 5000:
        rate = 0.08
    elif 5000 <= balance < 10000:
        rate = 0.10
    elif balance >= 10000:
        rate = 0.13
    else:
        await update.message.reply_text("⚠️ Your balance is below the minimum threshold.")
        return

    profit = balance * rate

    await update.message.reply_text(
        f"💸 *Profit Claimed!*\n\n"
        f"Your current balance: *{balance} USDT*\n"
        f"Daily rate: *{int(rate * 100)}%*\n"
        f"Today's profit: *{round(profit, 2)} USDT*\n\n"
        f"_Come back in 24h to claim again._",
        parse_mode="Markdown"
    )
