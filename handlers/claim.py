from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

# ✅ Simulated user balances (replace with DB later)
mock_balances = {
    123456789: 2500  # test user
}

# ✅ Claim timestamps per user
last_claims = {}

# 🎯 Tier logic
def get_daily_percent(balance):
    if balance >= 10000:
        return 0.13
    elif balance >= 5000:
        return 0.10
    elif balance >= 1000:
        return 0.08
    else:
        return 0.05

# 🧠 Claim handler
async def claim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.utcnow()

    # Get user's balance
    balance = mock_balances.get(user_id)
    if balance is None:
        await update.effective_message.reply_text(
            "❌ You have no deposit yet.\nSend USDT (TRC20) first to activate your balance."
        )
        return

    # Check if already claimed today
    last_claim = last_claims.get(user_id)
    if last_claim and now.date() == last_claim.date():
        await update.effective_message.reply_text(
            "⏳ You already claimed your daily profit today.\nCome back tomorrow!"
        )
        return

    # Calculate profit
    rate = get_daily_percent(balance)
    profit = round(balance * rate, 2)

    # Record the claim
    last_claims[user_id] = now

    # Send result
    await update.effective_message.reply_markdown(
        f"💸 *Daily Profit Claimed!*\n\n"
        f"💼 Balance: *{balance} USDT*\n"
        f"📈 Rate: *{int(rate * 100)}%*\n"
        f"✅ Profit Earned: *{profit} USDT*\n\n"
        f"Come back tomorrow for your next reward!"
    )
