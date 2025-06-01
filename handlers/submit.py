from telegram import Update
from telegram.ext import ContextTypes

# Temporary storage for submitted hashes (replace with DB later)
submitted_hashes = {}

async def submit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if hash was included
    if not context.args:
        await update.message.reply_text(
            "📝 Please provide your transaction hash after the command.\n\nExample:\n/submit abcd1234efgh5678"
        )
        return

    tx_hash = context.args[0]

    # Basic validation (TRC20 hashes are usually 64 chars)
    if len(tx_hash) < 30:
        await update.message.reply_text("❌ That doesn't look like a valid TX hash. Please double-check it.")
        return

    # Save it
    submitted_hashes[user_id] = tx_hash
    await update.message.reply_text(
        f"✅ Your TX hash has been submitted:\n`{tx_hash}`\n\nWe will review and activate your balance soon.",
        parse_mode="Markdown"
    )
