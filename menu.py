from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from auth import start, handle_auth_choice, register_username, register_password, handle_role_choice, login_uid, login_password, logout
from features.checkin import handle_checkin
from features.profile import handle_profile
from features.pet import handle_pet
from features.shop import handle_shop
from features.inventory import handle_inventory
from features.gacha import handle_gacha
from features.battle import handle_battle
from features.quest import handle_quest
from features.friends import handle_friends, view_friends, add_friend, handle_friend_uid
from features.mail import handle_mail, view_mail, handle_friend_request
from features.map import handle_map
from features.puzzle import handle_puzzle
from features.event import handle_event
from features.giftcode import handle_giftcode
import logging

logger = logging.getLogger(__name__)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("user"):
        await update.message.reply_text(
            "❌ Vui lòng đăng nhập hoặc đăng ký để sử dụng menu!\nDùng /start để bắt đầu.",
            parse_mode="Markdown"
        )
        return
    
    user_data = context.user_data["user"]
    keyboard = [
        [InlineKeyboardButton("📋 Hồ Sơ", callback_data="profile"),
         InlineKeyboardButton("🎁 Giftcode", callback_data="giftcode")],
        [InlineKeyboardButton("🏪 Shop", callback_data="shop"),
         InlineKeyboardButton("🎒 Kho Đồ", callback_data="inventory")],
        [InlineKeyboardButton("👥 Bạn Bè", callback_data="friends"),
         InlineKeyboardButton("📬 Hộp Thư", callback_data="mail")],
        [InlineKeyboardButton("⚔️ Chiến Đấu", callback_data="battle"),
         InlineKeyboardButton("🗺️ Bản Đồ", callback_data="map")],
        [InlineKeyboardButton("📜 Nhiệm Vụ", callback_data="quest"),
         InlineKeyboardButton("🎰 Gacha", callback_data="gacha")],
        [InlineKeyboardButton("🐾 Pet", callback_data="pet"),
         InlineKeyboardButton("🧩 Puzzle", callback_data="puzzle")],
        [InlineKeyboardButton("🎉 Sự Kiện", callback_data="event"),
         InlineKeyboardButton("📅 Check-in", callback_data="checkin")],
        [InlineKeyboardButton("🚪 Đăng Xuất", callback_data="logout")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🌌 **Chào mừng {user_data['username']} đến với Menu Chính!** 🌌\n"
        "─────────────────\n"
        "Chọn một chức năng để tiếp tục:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    logger.info(f"Handling callback query with data: {data}")
    
    handlers = {
        "profile": handle_profile,
        "giftcode": handle_giftcode,
        "shop": handle_shop,
        "inventory": handle_inventory,
        "friends": handle_friends,
        "mail": handle_mail,
        "battle": handle_battle,
        "map": handle_map,
        "quest": handle_quest,
        "gacha": handle_gacha,
        "pet": handle_pet,
        "puzzle": handle_puzzle,
        "event": handle_event,
        "checkin": handle_checkin,
        "logout": logout,
        "register": handle_auth_choice,
        "login": handle_auth_choice,
        "view_friends": view_friends,
        "add_friend": add_friend,
        "view_mail": view_mail
    }
    
    if data in handlers:
        await handlers[data](update, context)
    elif data.startswith("friend_request_accept_") or data.startswith("friend_request_reject_"):
        await handle_friend_request(update, context)
    else:
        logger.warning(f"Unknown callback data: {data}")
        await query.edit_message_text(
            text="❌ Chức năng không khả dụng!\nQuay lại /menu.",
            parse_mode="Markdown"
        )