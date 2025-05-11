from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data, read_items
from features.items import use_item
import logging

logger = logging.getLogger(__name__)

async def handle_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🍎 Đồ Ăn", callback_data="shop_category_đồ ăn")],
        [InlineKeyboardButton("🗡️ Vũ Khí", callback_data="shop_category_vũ khí")],
        [InlineKeyboardButton("🛡️ Trang Bị", callback_data="shop_category_trang bị")],
        [InlineKeyboardButton("📘 Sách Kỹ Năng", callback_data="shop_category_sách kỹ năng")],
        [InlineKeyboardButton("💊 Thuốc", callback_data="shop_category_thuốc")],
        [InlineKeyboardButton("💎 Đá Quý", callback_data="shop_category_đá quý")],
        [InlineKeyboardButton("🐉 Pet", callback_data="shop_category_pet")],
        [InlineKeyboardButton("🔙 Quay lại", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🏪 **Shop Phép Thuật** 🏪\n"
        "─────────────────\n"
        "Chọn danh mục để xem vật phẩm:\n"
        "- 🍎 **Đồ Ăn**: Hồi phục năng lượng.\n"
        "- 🗡️ **Vũ Khí**: Tăng sức mạnh tấn công.\n"
        "- 🛡️ **Trang Bị**: Tăng phòng thủ.\n"
        "- 📘 **Sách Kỹ Năng**: Học kỹ năng mới.\n"
        "- 💊 **Thuốc**: Hồi máu, mana.\n"
        "- 💎 **Đá Quý**: Hiệu ứng đặc biệt.\n"
        "- 🐉 **Pet**: Bạn đồng hành chiến đấu."
    )
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_shop_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data.split("_")[2].strip().lower()
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    role = user_data["role"].strip().lower()
    items = read_items()
    
    # Lọc vật phẩm theo danh mục và vai trò
    valid_items = {
        item_id: item for item_id, item in items.items()
        if item["category"].strip().lower() == category and 
           (item["role"].strip().lower() == role or item["role"].strip().lower() == "all")
    }
    
    logger.info(f"Shop category: {category}, User role: {role}, Valid items: {valid_items}")
    
    if not valid_items:
        keyboard = [[InlineKeyboardButton("🔙 Quay lại", callback_data="shop")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"🏪 **Shop Phép Thuật - {category.title()}** 🏪\n"
                 f"❌ Không có vật phẩm nào trong danh mục **{category}** cho vai trò **{user_data['role']}**!\n"
                 "Hãy thử danh mục khác hoặc quay lại.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    keyboard = [
        [InlineKeyboardButton(f"{item['name']} ({item['price']} vàng)", callback_data=f"shop_buy_{item_id}")]
        for item_id, item in valid_items.items()
    ]
    keyboard.append([InlineKeyboardButton("🔙 Quay lại", callback_data="shop")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        f"🏪 **Shop Phép Thuật - {category.title()}** 🏪\n"
        "─────────────────\n" +
        "\n".join([
            f"- **{item['name']}** ({item['tier']}): {item['description']} (ID: {item_id})"
            for item_id, item in valid_items.items()
        ]) +
        "\n─────────────────\nChọn vật phẩm để mua:"
    )
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_shop_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    item_id = query.data.split("_")[2]
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    items = read_items()
    item = items.get(item_id)
    
    if not item:
        await query.edit_message_text(
            text=f"🏪 **Shop Phép Thuật** 🏪\n❌ Vật phẩm không tồn tại!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Kiểm tra vai trò
    if item["role"].strip().lower() != "all" and item["role"].strip().lower() != user_data["role"].strip().lower():
        await query.edit_message_text(
            text=f"🏪 **Shop Phép Thuật** 🏪\n❌ Vật phẩm **{item['name']}** chỉ dành cho **{item['role']}**!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Kiểm tra vàng
    if user_data["gold"] < item["price"]:
        await query.edit_message_text(
            text=f"🏪 **Shop Phép Thuật** 🏪\n❌ Bạn không đủ vàng để mua **{item['name']}**!\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Trừ vàng và thêm vật phẩm
    user_data["gold"] -= item["price"]
    if item["category"] == "pet":
        user_data["pets"].append({"name": item["name"], "power": item["effects"].get("power", 50)})
    else:
        user_data["inventory"].append(item_id)
    
    # Áp dụng hiệu ứng (trừ pet, xử lý sau)
    if item["category"] != "pet":
        use_item(telegram_id, item_id)
    
    update_user_data(telegram_id, user_data)
    
    await query.edit_message_text(
        text=f"🏪 **Shop Phép Thuật** 🏪\n✅ Bạn đã mua **{item['name']}** (ID: {item_id}) thành công!\nQuay lại /menu.",
        parse_mode="Markdown"
    )