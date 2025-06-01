from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

# Simulated user balances (mocked)
mock_balances = {
    123456789: 12000,  # Example user
}

last_claims = {}

def get_daily_percent(balance):
    if balance >= 10000:
        return 0.13
    elif balance >= 5000:
        return 0.10
    elif balance >= 1000:
        return 0.08
    else:
        return 0.05

async def claim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.utcnow()

    balance = mock_balances.get(user_id, 12000)  # You can edit this for testing

    # Check if already claimed today
    last_claim = last_claims.get(user_id)
    if last_claim and now.date() == last_claim.date():
        await update.message.reply_text(
            "⏳ You've already claimed your daily profit today.\nCome back tomorrow!"
        )
        return

    # Calculate profit
    rate = get_daily_percent(balance)
    profit = round(balance * rate, 2)
    last_claims[user_id] = now

    # Choose emoji
    emoji = "🟢" if balance < 1000 else "💰" if balance < 5000 else "🪙" if balance < 10000 else "🏦"

    await update.message.reply_markdown(
        f"{emoji} *Daily Profit Claimed!*\n\n"
        f"💼 Your Deposit: *{balance} USDT*\n"
        f"📈 Rate: *{int(rate * 100)}%*\n"
        f"💸 Profit Earned: *{profit} USDT*\n\n"
        f"✅ Profits are credited daily. Come back tomorrow to claim again!"
    )
