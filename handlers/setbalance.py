from telegram import Update
from telegram.ext import ContextTypes

# ✅ Simulated balance database (same as claim.py)
user_balances = {}

# ✅ Only allow certain Telegram IDs (yours for now)
ADMIN_IDS = [123456789]  # Replace with your Telegram ID

async def set_balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔️ You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("❗ Usage:\n/setbalance <telegram_id> <amount>")
        return

    try:
        target_id = int(context.args[0])
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Please provide correct numbers.")
        return

    user_balances[target_id] = amount
    await update.message.reply_text(
        f"✅ Balance of user `{target_id}` set to *{amount} USDT*.",
        parse_mode="Markdown"
    )
