import logging
import sys
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from auth import start, handle_auth_choice, register_username, register_password, handle_role_choice, login_uid, login_password
from menu import show_menu, handle_menu
from features.friends import handle_friend_uid
from features.giftcode import handle_giftcode_input

# Thiết lập logging với mã hóa UTF-8
class UnicodeSafeFormatter(logging.Formatter):
    def format(self, record):
        try:
            return super().format(record)
        except UnicodeEncodeError:
            # Thay thế ký tự không mã hóa được bằng '?'
            record.msg = record.msg.encode('ascii', errors='replace').decode('ascii')
            return super().format(record)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # File log dùng UTF-8
        logging.StreamHandler(sys.stdout)  # Console dùng sys.stdout
    ]
)

# Áp dụng formatter cho console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(UnicodeSafeFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logging.getLogger().handlers[1] = console_handler

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error(f"Update {update} caused error: {context.error}")
    if update.callback_query:
        await update.callback_query.message.reply_text("❌ An error occurred. Please try again!")
    elif update.message:
        await update.message.reply_text("❌ An error occurred. Please try again!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler cho lệnh /start và menu
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))
    
    # Handler cho callback query
    application.add_handler(CallbackQueryHandler(handle_menu))
    
    # Handler cho quá trình đăng ký và đăng nhập
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auth_handler))
    
    # Handler cho lỗi
    application.add_error_handler(error_handler)
    
    logger.info("Bot is starting...")
    application.run_polling()

async def auth_handler(update, context):
    if context.user_data.get("awaiting_username"):
        await register_username(update, context)
    elif context.user_data.get("awaiting_password"):
        await register_password(update, context)
    elif context.user_data.get("awaiting_role"):
        await handle_role_choice(update, context)
    elif context.user_data.get("awaiting_login_uid"):
        await login_uid(update, context)
    elif context.user_data.get("awaiting_login_password"):
        await login_password(update, context)
    elif context.user_data.get("awaiting_friend_uid"):
        await handle_friend_uid(update, context)
    elif context.user_data.get("awaiting_giftcode"):
        await handle_giftcode_input(update, context)

if __name__ == "__main__":
    main()