from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import is_user_registered, register_user, check_login, get_user_data, update_user_data
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if context.user_data.get("user"):
        await update.message.reply_text(
            f"🌌 **Chào mừng quay lại, {context.user_data['user']['username']}**!\n"
            "Nhập /menu để tiếp tục cuộc phiêu lưu! 🧙‍♂️",
            parse_mode="Markdown"
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📝 Đăng Ký", callback_data="register")],
        [InlineKeyboardButton("🔑 Đăng Nhập", callback_data="login")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌌 **Chào mừng đến với Thế Giới Phép Thuật!** 🌌\n"
        "─────────────────\n"
        "Chọn một hành động để bắt đầu:\n"
        "- 📝 **Đăng Ký**: Tạo nhân vật mới.\n"
        "- 🔑 **Đăng Nhập**: Tiếp tục với nhân vật hiện có.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_auth_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    choice = query.data
    context.user_data["awaiting_auth_choice"] = False
    
    if choice == "register":
        context.user_data["awaiting_register_username"] = True
        await query.edit_message_text(
            "📝 **Đăng Ký** 📝\nVui lòng nhập **tên nhân vật** (tối đa 20 ký tự):",
            parse_mode="Markdown"
        )
    elif choice == "login":
        context.user_data["awaiting_login_uid"] = True
        await query.edit_message_text(
            "🔑 **Đăng Nhập** 🔑\nVui lòng nhập **UID** của bạn (bắt đầu bằng DRA):",
            parse_mode="Markdown"
        )

async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    if len(username) > 20:
        await update.message.reply_text(
            "❌ **Tên nhân vật quá dài!** Vui lòng nhập tên dưới 20 ký tự.",
            parse_mode="Markdown"
        )
        return
    context.user_data["awaiting_register_username"] = False
    context.user_data["awaiting_register_password"] = True
    context.user_data["temp_username"] = username
    await update.message.reply_text(
        "🔒 **Đăng Ký** 🔒\nVui lòng nhập **mật khẩu** (tối thiểu 6 ký tự):",
        parse_mode="Markdown"
    )

async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    if len(password) < 6:
        await update.message.reply_text(
            "❌ **Mật khẩu quá ngắn!** Vui lòng nhập mật khẩu từ 6 ký tự trở lên.",
            parse_mode="Markdown"
        )
        return
    context.user_data["awaiting_register_password"] = False
    context.user_data["temp_password"] = password
    
    keyboard = [
        [InlineKeyboardButton("Chiến Binh ⚔️", callback_data="role_Chiến Binh")],
        [InlineKeyboardButton("Pháp Sư 🧙‍♂️", callback_data="role_Pháp Sư")],
        [InlineKeyboardButton("Cung Thủ 🏹", callback_data="role_Cung Thủ")],
        [InlineKeyboardButton("Thuật Sư 🦹‍♂️", callback_data="role_Thuật Sư")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🛡️ **Chọn vai trò** 🛡️\n"
        "─────────────────\n"
        "Chọn một vai trò cho nhân vật của bạn:\n"
        "- ⚔️ **Chiến Binh**: Máu dày, sát thương vật lý mạnh.\n"
        "- 🧙‍♂️ **Pháp Sư**: Phép thuật mạnh, máu yếu.\n"
        "- 🏹 **Cung Thủ**: Tốc độ cao, tấn công tầm xa.\n"
        "- 🦹‍♂️ **Thuật Sư**: Kết hợp phép và kỹ năng đặc biệt.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_role_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    role = query.data.split("_")[1]
    telegram_id = query.from_user.id
    username = context.user_data["temp_username"]
    password = context.user_data["temp_password"]
    
    uid = register_user(telegram_id, username, password, role)
    user_data = get_user_data(telegram_id, uid)
    context.user_data["user"] = user_data
    
    await query.edit_message_text(
        f"🎉 **Đăng ký thành công!** 🎉\n"
        f"**Tên nhân vật**: {username}\n"
        f"**UID**: {uid}\n"
        f"**Vai trò**: {role}\n"
        f"Nhập /menu để bắt đầu cuộc phiêu lưu! 🌌",
        parse_mode="Markdown"
    )

async def login_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    context.user_data["awaiting_login_uid"] = False
    context.user_data["temp_uid"] = uid
    context.user_data["awaiting_login_password"] = True
    await update.message.reply_text(
        "🔒 **Đăng Nhập** 🔒\nVui lòng nhập **mật khẩu**:",
        parse_mode="Markdown"
    )

async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    uid = context.user_data["temp_uid"]
    context.user_data["awaiting_login_password"] = False
    
    user_data = check_login(uid, password)
    if user_data:
        telegram_id = update.effective_user.id
        context.user_data["user"] = user_data
        update_user_data(telegram_id, user_data)
        await update.message.reply_text(
            f"✅ **Đăng nhập thành công!** Chào mừng **{user_data['username']}**!\n"
            "Nhập /menu để tiếp tục cuộc phiêu lưu! 🌌",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ **UID hoặc mật khẩu không đúng!**\n"
            "Thử lại với /start hoặc kiểm tra thông tin đăng nhập.",
            parse_mode="Markdown"
        )

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("📝 Đăng Ký", callback_data="register")],
        [InlineKeyboardButton("🔑 Đăng Nhập", callback_data="login")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🚪 **Đăng xuất thành công!** 🚪\n"
        "─────────────────\n"
        "Chọn một hành động để tiếp tục:\n"
        "- 📝 **Đăng Ký**: Tạo nhân vật mới.\n"
        "- 🔑 **Đăng Nhập**: Tiếp tục với nhân vật hiện có."
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )