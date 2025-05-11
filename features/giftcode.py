from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data, read_giftcodes, write_giftcodes, read_items
from datetime import datetime
import pytz

async def handle_giftcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    context.user_data["awaiting_giftcode"] = True
    await query.edit_message_text(
        text="🎁 **Nhập Giftcode** 🎁\nVui lòng gửi **mã giftcode**:\n(Hủy bằng /menu)",
        parse_mode="Markdown"
    )

async def handle_giftcode_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    telegram_id = update.effective_user.id
    user_data = get_user_data(telegram_id)
    giftcodes = read_giftcodes()
    
    context.user_data.pop("awaiting_giftcode", None)
    
    if code not in giftcodes:
        await update.message.reply_text(
            text="🎁 **Giftcode** 🎁\n❌ Mã giftcode không hợp lệ!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Kiểm tra thời hạn
    expires_at = giftcodes[code].get("expires_at")
    if expires_at:
        expire_date = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
        current_date = datetime.now(pytz.UTC)
        if current_date > expire_date:
            await update.message.reply_text(
                text="🎁 **Giftcode** 🎁\n❌ Mã giftcode đã hết hạn!\nQuay lại /menu.",
                parse_mode="Markdown"
            )
            return
    
    # Kiểm tra đã sử dụng
    if user_data["uid"] in giftcodes[code]["used_by"]:
        await update.message.reply_text(
            text="🎁 **Giftcode** 🎁\n❌ Bạn đã sử dụng mã này rồi!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Áp dụng phần thưởng
    reward = giftcodes[code]["reward"]
    if "gold" in reward:
        user_data["gold"] += reward["gold"]
    if "items" in reward:
        user_data["inventory"].extend(reward["items"])
    
    # Đánh dấu đã sử dụng
    giftcodes[code]["used_by"].append(user_data["uid"])
    write_giftcodes(giftcodes)
    update_user_data(telegram_id, user_data)
    
    reward_text = []
    if "gold" in reward:
        reward_text.append(f"{reward['gold']} vàng")
    if "items" in reward:
        items = read_items()
        reward_text.append(", ".join([items.get(item_id, {}).get("name", "Vật phẩm không xác định") for item_id in reward["items"]]))
    
    await update.message.reply_text(
        text=f"🎁 **Giftcode** 🎁\n✅ Đổi mã thành công! Bạn nhận được: **{', '.join(reward_text)}**!\nQuay lại /menu.",
        parse_mode="Markdown"
    )