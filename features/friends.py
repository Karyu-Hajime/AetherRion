from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data, get_telegram_id_from_uid
import logging

logger = logging.getLogger(__name__)

async def handle_friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    
    keyboard = [
        [InlineKeyboardButton("📋 Xem Bạn Bè", callback_data="view_friends")],
        [InlineKeyboardButton("➕ Thêm Bạn", callback_data="add_friend")],
        [InlineKeyboardButton("🔙 Quay lại", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="👥 **Quản Lý Bạn Bè** 👥\n"
             "─────────────────\n"
             "Chọn hành động:\n"
             "- 📋 **Xem Bạn Bè**: Xem danh sách bạn bè.\n"
             "- ➕ **Thêm Bạn**: Gửi lời mời kết bạn.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def view_friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    
    if not user_data["friends"]:
        keyboard = [[InlineKeyboardButton("🔙 Quay lại", callback_data="friends")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="👥 **Danh Sách Bạn Bè** 👥\n❌ Bạn chưa có người bạn nào!\nHãy mời bạn bè qua /menu.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    friends_text = []
    for friend_uid in user_data["friends"]:
        friend_telegram_id = get_telegram_id_from_uid(friend_uid)
        if friend_telegram_id:
            friend_data = get_user_data(friend_telegram_id)
            friends_text.append(f"- **{friend_data['username']}** (UID: {friend_uid})")
        else:
            friends_text.append(f"- UID: {friend_uid} (Không tìm thấy)")
    
    keyboard = [[InlineKeyboardButton("🔙 Quay lại", callback_data="friends")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="👥 **Danh Sách Bạn Bè** 👥\n"
             "─────────────────\n" +
             "\n".join(friends_text),
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def add_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    context.user_data["awaiting_friend_uid"] = True
    
    await query.edit_message_text(
        text="➕ **Thêm Bạn Bè** ➕\n"
             "Vui lòng gửi **UID** của người bạn muốn kết bạn (tôi giử lời mới kết bạn thành công nhưng phía bên hộp thư của người nhận thì để từ uid tôi muốn nó thể hiện tên người dùng và hơn thế nữa khi tôi click vào thì báo là chứ năng ko khả dụng và người đó ko thể đồng ý kết bạn nếu bạn gặp lỗi gì thì có thể tạo ra thêm file nào đó để thực hiện và lưu trữbắt đầu bằng DRA):\n"
             "(Hủy bằng /menu)",
        parse_mode="Markdown"
    )

async def handle_friend_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    telegram_id = update.effective_user.id
    user_data = get_user_data(telegram_id)
    
    context.user_data.pop("awaiting_friend_uid", None)
    
    # Kiểm tra UID hợp lệ
    friend_telegram_id = get_telegram_id_from_uid(uid)
    if not friend_telegram_id:
        await update.message.reply_text(
            text="👥 **Thêm Bạn Bè** 👥\n❌ UID không tồn tại!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    friend_data = get_user_data(friend_telegram_id)
    if not friend_data:
        await update.message.reply_text(
            text="👥 **Thêm Bạn Bè** 👥\n❌ Không tìm thấy người dùng!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Kiểm tra đã là bạn
    if uid in user_data["friends"]:
        await update.message.reply_text(
            text=f"👥 **Thêm Bạn Bè** 👥\n❌ **{friend_data['username']}** đã là bạn của bạn!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Kiểm tra gửi lời mời cho chính mình
    if uid == user_data["uid"]:
        await update.message.reply_text(
            text="👥 **Thêm Bạn Bè** 👥\n❌ Bạn không thể gửi lời mời cho chính mình!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Thêm lời mời vào hộp thư của người nhận
    friend_data["mail"].append({
        "type": "friend_request",
        "from": user_data["uid"],
        "from_username": user_data["username"],
        "content": f"{user_data['username']} muốn kết bạn với bạn!"
    })
    update_user_data(friend_telegram_id, friend_data)
    
    logger.info(f"Sent friend request from {user_data['uid']} to {uid}")
    
    await update.message.reply_text(
        text=f"👥 **Thêm Bạn Bè** 👥\n✅ Đã gửi lời mời kết bạn đến **{friend_data['username']}**!\nQuay lại /menu.",
        parse_mode="Markdown"
    )