from telegram import Update
from telegram.ext import ContextTypes
from handlers.setbalance import user_balances  # shared balance dict

async def claim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if balance exists
    if user_id not in user_balances:
        await update.message.reply_text(
            "⚠️ لا يوجد رصيد مفعل لديك.\nاستخدم /submit بعد الإيداع لتفعيل رصيدك."
        )
        return

    balance = user_balances[user_id]

    # Profit tier logic
    if 50 <= balance < 1000:
        rate = 0.05
    elif 1000 <= balance < 5000:
        rate = 0.08
    elif 5000 <= balance < 10000:
        rate = 0.10
    elif balance >= 10000:
        rate = 0.13
    else:
        await update.message.reply_text("⚠️ رصيدك أقل من الحد الأدنى المطلوب.")
        return

    profit = round(balance * rate, 2)

    await update.message.reply_text(
        f"💸 *تم سحب الأرباح!*\n\n"
        f"💰 الرصيد الحالي: *{balance} USDT*\n"
        f"📈 نسبة الربح اليومية: *{int(rate * 100)}%*\n"
        f"✅ ربحك اليومي: *{profit} USDT*\n\n"
        f"_يمكنك المطالبة مرة واحدة كل 24 ساعة._",
        parse_mode="Markdown"
    )
