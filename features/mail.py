from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data, get_telegram_id_from_uid  # noqa
import logging

logger = logging.getLogger(__name__)

async def handle_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    
    try:
        user_data = get_user_data(telegram_id)
        if not user_data:
            raise ValueError("User data not found")
        
        # Khởi tạo mail nếu không tồn tại
        if "mail" not in user_data or not isinstance(user_data["mail"], list):
            user_data["mail"] = []
            update_user_data(telegram_id, user_data)
        
        if not user_data["mail"]:
            keyboard = [[InlineKeyboardButton("🔙 Quay lại", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text="📬 **Hộp Thư** 📬\n❌ Bạn chưa có thư nào!\nQuay lại /menu.",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return
        
        logger.info(f"Mail list for telegram_id {telegram_id}: {user_data['mail']}")
        
        mail_buttons = []
        for idx, mail in enumerate(user_data["mail"]):
            if not isinstance(mail, dict):
                logger.warning(f"Invalid mail format at index {idx}: {mail}")
                continue
            mail_type = mail.get("type", "")
            sender = mail.get("from_username", mail.get("from", "Unknown")) if mail_type == "friend_request" else "Hệ thống"
            mail_buttons.append([InlineKeyboardButton(
                f"📩 Từ {sender}", callback_data=f"view_mail_{idx}"
            )])
        
        if not mail_buttons:
            keyboard = [[InlineKeyboardButton("🔙 Quay lại", callback_data="menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text="📬 **Hộp Thư** 📬\n❌ Không có thư hợp lệ!\nQuay lại /menu.",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return
        
        mail_buttons.append([InlineKeyboardButton("🔙 Quay lại", callback_data="menu")])
        reply_markup = InlineKeyboardMarkup(mail_buttons)
        
        await query.edit_message_text(
            text="📬 **Hộp Thư** 📬\nChọn một thư để xem chi tiết:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    except Exception as e:
        logger.error(f"Error in handle_mail for telegram_id {telegram_id}: {str(e)}")
        await query.edit_message_text(
            text="❌ Lỗi khi mở hộp thư! Vui lòng thử lại.\nQuay lại /menu.",
            parse_mode="Markdown"
        )

async def view_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    
    try:
        user_data = get_user_data(telegram_id)
        if not user_data or "mail" not in user_data:
            raise ValueError("User data or mail not found")
        
        mail_idx = int(query.data.split("_")[-1])
        if mail_idx < 0 or mail_idx >= len(user_data["mail"]):
            raise ValueError(f"Invalid mail index: {mail_idx}")
        
        mail = user_data["mail"][mail_idx]
        if not isinstance(mail, dict):
            raise ValueError(f"Invalid mail format at index {mail_idx}: {mail}")
        
        mail_content = mail.get("content", "Không có nội dung.")
        
        keyboard = []
        if mail.get("type") == "friend_request":
            sender = mail.get("from_username", mail.get("from", "Unknown"))
            mail_content = f"Lời mời kết bạn từ **{sender}** (UID: {mail.get('from', 'N/A')})\n\n{mail_content}"
            keyboard.append([
                InlineKeyboardButton("✅ Chấp nhận", callback_data=f"friend_request_accept_{mail_idx}"),
                InlineKeyboardButton("❌ Từ chối", callback_data=f"friend_request_reject_{mail_idx}")
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Quay lại", callback_data="mail")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"📬 **Nội Dung Thư** 📬\n─────────────────\n{mail_content}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    except Exception as e:
        logger.error(f"Error in view_mail for telegram_id {telegram_id}: {str(e)}")
        await query.edit_message_text(
            text="❌ Lỗi khi xem thư! Vui lòng thử lại.\nQuay lại /menu.",
            parse_mode="Markdown"
        )

async def handle_friend_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    
    try:
        user_data = get_user_data(telegram_id)
        if not user_data or "mail" not in user_data:
            raise ValueError("User data or mail not found")
        
        action, mail_idx = query.data.split("_")[-2], int(query.data.split("_")[-1])
        if mail_idx < 0 or mail_idx >= len(user_data["mail"]):
            raise ValueError(f"Invalid mail index: {mail_idx}")
        
        mail = user_data["mail"][mail_idx]
        if mail.get("type") != "friend_request":
            raise ValueError(f"Mail at index {mail_idx} is not a friend request")
        
        sender_uid = mail.get("from")
        if not sender_uid:
            raise ValueError("Sender UID not found in mail")
        
        sender_username = mail.get("from_username", sender_uid)
        
        if action == "accept":
            # Thêm bạn vào danh sách của cả hai
            sender_telegram_id = get_telegram_id_from_uid(sender_uid)
            if sender_telegram_id:
                sender_data = get_user_data(sender_telegram_id)
                if sender_data:
                    if user_data["uid"] not in sender_data["friends"]:
                        sender_data["friends"].append(user_data["uid"])
                        update_user_data(sender_telegram_id, sender_data)
                else:
                    logger.warning(f"Sender data not found for UID: {sender_uid}")
            else:
                logger.warning(f"Sender telegram_id not found for UID: {sender_uid}")
            
            if sender_uid not in user_data["friends"]:
                user_data["friends"].append(sender_uid)
            
            # Xóa thư
            user_data["mail"].pop(mail_idx)
            update_user_data(telegram_id, user_data)
            
            logger.info(f"User {user_data['uid']} accepted friend request from {sender_uid}")
            await query.edit_message_text(
                text=f"✅ Bạn đã chấp nhận lời mời kết bạn từ **{sender_username}**!\nQuay lại /menu.",
                parse_mode="Markdown"
            )
        else:  # action == "reject"
            # Xóa thư
            user_data["mail"].pop(mail_idx)
            update_user_data(telegram_id, user_data)
            
            logger.info(f"User {user_data['uid']} rejected friend request from {sender_uid}")
            await query.edit_message_text(
                text=f"❌ Bạn đã từ chối lời mời kết bạn từ **{sender_username}**!\nQuay lại /menu.",
                parse_mode="Markdown"
            )
    
    except Exception as e:
        logger.error(f"Error in handle_friend_request for telegram_id {telegram_id}: {str(e)}")
        await query.edit_message_text(
            text="❌ Lỗi khi xử lý lời mời kết bạn! Vui lòng thử lại.\nQuay lại /menu.",
            parse_mode="Markdown"
        )