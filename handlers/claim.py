from telegram import Update
from telegram.ext import ContextTypes
from handlers.setbalance import user_balances  # ✅ Shared dictionary of balances

async def claim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # ✅ Check if user has an active balance
    if user_id not in user_balances:
        await update.message.reply_text(
            "⚠️ *No active balance found.*\n\n"
            "Please deposit and submit your transaction hash using /submit to activate your balance.",
            parse_mode="Markdown"
        )
        return

    balance = user_balances[user_id]

    # ✅ Determine profit rate based on balance tier
    if 50 <= balance < 1000:
        rate = 0.05
        tier = "🟢 5%"
    elif 1000 <= balance < 5000:
        rate = 0.08
        tier = "💰 8%"
    elif 5000 <= balance < 10000:
        rate = 0.10
        tier = "🪙 10%"
    elif balance >= 10000:
        rate = 0.13
        tier = "🏦 13%"
    else:
        await update.message.reply_text(
            "⚠️ Your balance is below the minimum 50 USDT.\nPlease deposit more to activate profit.",
            parse_mode="Markdown"
        )
        return

    profit = round(balance * rate, 2)

    # ✅ Reply with profit message
    await update.message.reply_text(
        f"💸 *Profit Claimed!*\n\n"
        f"👤 User: `{user.first_name}`\n"
        f"💼 Balance: *{balance} USDT*\n"
        f"📈 Tier: {tier}\n"
        f"📤 Profit: *{profit} USDT*\n\n"
        f"🔁 Come back in 24 hours to claim again.",
        parse_mode="Markdown"
    )
