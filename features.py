# Nhập các thư viện cần thiết
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user_data, update_user_data, read_db, write_db, read_items
import random
import datetime

# Hàm xử lý điểm danh
async def handle_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    
    # Kiểm tra thời gian điểm danh
    today = datetime.date.today().isoformat()
    last_checkin = user_data.get("last_checkin", "")
    
    if last_checkin == today:
        await query.edit_message_text(
            text="📜 **Điểm Danh Hàng Ngày** 📜\n❌ Bạn đã điểm danh hôm nay rồi!\nHãy quay lại vào ngày mai! ✨\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Cập nhật vàng, thời gian điểm danh, và số lần điểm danh
    user_data["gold"] += 100
    user_data["last_checkin"] = today
    user_data["checkin_count"] = user_data.get("checkin_count", 0) + 1
    update_user_data(telegram_id, user_data)
    
    await query.edit_message_text(
        text="📜 **Điểm Danh Hàng Ngày** 📜\n✅ Bạn nhận được **100 vàng**! ✨\nQuay lại /menu.",
        parse_mode="Markdown"
    )

# Hàm xử lý thú cưng
async def handle_pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    
    # Hiển thị danh sách thú cưng
    pets = user_data.get("pets", [])
    if not pets:
        text = "🐾 **Thú Cưng** 🐾\n❌ Bạn chưa có thú cưng nào!\nHãy đến **Shop** để nhận nuôi một người bạn đồng hành! 🐉\nQuay lại /menu."
    else:
        text = "🐾 **Thú Cưng** 🐾\n**Danh sách thú cưng**:\n" + "\n".join([f"- **{pet['name']}** (Sức mạnh: {pet['power']})" for pet in pets]) + "\nQuay lại /menu."
    
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý thông tin tài khoản
async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    
    # Hiển thị thông tin
    stats = user_data["stats"]
    text = (
        "👤 **Hồ Sơ Nhân Vật** 👤\n"
        "─────────────────\n"
        f"**Tên**: {user_data['username']}\n"
        f"**UID**: `{user_data['uid']}`\n"
        f"**Vai trò**: {user_data['role']}\n"
        f"**Ngày tham gia**: {user_data['checkin_count']} ngày\n"
        "─────────────────\n"
        f"**Level**: {user_data['level']}\n"
        f"**EXP**: {user_data['exp']}/{user_data['max_exp']}\n"
        f"**Vàng**: {user_data['gold']} 💰\n"
        f"**HP**: {stats['hp']} ❤️\n"
        f"**ATK**: {stats['atk']} 🗡️\n"
        f"**MAGIC**: {stats['magic']} 🔮\n"
        f"**DEF**: {stats['def']} 🛡️\n"
        f"**SPEED**: {stats['speed']} ⚡\n"
        f"**Mana**: {stats['mana']} 💧\n"
        f"**Trận thắng**: {user_data['battles_won']} 🏆\n"
        "─────────────────\n"
        "Quay lại /menu."
    )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý giftcode
async def handle_giftcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Yêu cầu nhập giftcode
    context.user_data["awaiting_giftcode"] = True
    await query.edit_message_text(
        text="🎁 **Nhập Giftcode** 🎁\nVui lòng gửi **mã giftcode**:\n(Hủy bằng /menu)",
        parse_mode="Markdown"
    )

# Hàm xử lý hộp thư
async def handle_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    
    # Hiển thị hộp thư
    mails = user_data.get("mail", [])
    if not mails:
        text = "📬 **Hộp Thư** 📬\n❌ Hộp thư trống!\nTham gia **sự kiện** để nhận thư từ hệ thống! 📩\nQuay lại /menu."
    else:
        text = "📬 **Hộp Thư** 📬\n**Danh sách thư**:\n" + "\n".join([f"- **{mail['title']}**: {mail['content']}" for mail in mails]) + "\nQuay lại /menu."
    
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý bản đồ
async def handle_map(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query
    query = update.callback_query
    
    # Hiển thị bản đồ (giả lập)
    text = (
        "🗺️ **Bản Đồ Phiêu Lưu** 🗺️\n"
        "─────────────────\n"
        "- 🌲 **Rừng Huyền Bí**: Nơi ẩn chứa kho báu!\n"
        "- 🌋 **Núi Lửa Rực Cháy**: Thử thách khắc nghiệt!\n"
        "- 🏰 **Thành Phố Phép Thuật**: Trung tâm giao thương!\n"
        "─────────────────\n"
        "Chọn khu vực để khám phá! (Chưa khả dụng)\nQuay lại /menu."
    )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý giải đố
async def handle_puzzle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Tạo câu đố ngẫu nhiên
    riddles = [
        {"question": "Tôi không có cánh, nhưng tôi bay. Tôi không có mắt, nhưng tôi khóc. Tôi là gì?", "answer": "đám mây"},
        {"question": "Càng lấy đi càng lớn, tôi là gì?", "answer": "lỗ"}
    ]
    riddle = random.choice(riddles)
    
    # Lưu câu đố vào context
    context.user_data["current_puzzle"] = riddle
    context.user_data["awaiting_puzzle_answer"] = True
    
    await query.edit_message_text(
        text=f"🧩 **Giải Đố Bí Ẩn** 🧩\n**Câu đố**: {riddle['question']}\nGửi **câu trả lời** của bạn:\n(Hủy bằng /menu)",
        parse_mode="Markdown"
    )

# Hàm xử lý shop
async def handle_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy danh sách vật phẩm
    items = read_items()
    
    # Tạo danh sách vật phẩm trong shop
    keyboard = [
        [InlineKeyboardButton(f"{items['ITEM001']['name']} ({items['ITEM001']['price']} vàng)", callback_data="shop_buy_ITEM001")],
        [InlineKeyboardButton(f"{items['ITEM003']['name']} ({items['ITEM003']['price']} vàng)", callback_data="shop_buy_ITEM003")],
        [InlineKeyboardButton("🔙 Quay lại", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🏪 **Shop Phép Thuật** 🏪\n"
        "─────────────────\n"
        f"- **{items['ITEM001']['name']}**: {items['ITEM001']['description']} (ID: ITEM001)\n"
        f"- **{items['ITEM003']['name']}**: {items['ITEM003']['description']} (ID: ITEM003)\n"
        "─────────────────\n"
        "Chọn vật phẩm để mua:"
    )
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Hàm xử lý mua vật phẩm từ shop
async def handle_shop_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    item_id = query.data.split("_")[2]
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu
    user_data = get_user_data(telegram_id)
    items = read_items()
    item = items.get(item_id)
    
    if not item:
        await query.edit_message_text(
            text=f"🏪 **Shop Phép Thuật** 🏪\n❌ Vật phẩm không tồn tại!\nQuay lại /menu.",
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
    if item_id.startswith("ITEM003") or item_id.startswith("ITEM004"):  # Thú cưng
        user_data["pets"].append({"name": item["name"], "power": 50})
    else:
        user_data["inventory"].append(item_id)
    update_user_data(telegram_id, user_data)
    
    await query.edit_message_text(
        text=f"🏪 **Shop Phép Thuật** 🏪\n✅ Bạn đã mua **{item['name']}** (ID: {item_id}) thành công!\nQuay lại /menu.",
        parse_mode="Markdown"
    )

# Hàm xử lý túi đồ
async def handle_inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng và vật phẩm
    user_data = get_user_data(telegram_id)
    items = read_items()
    
    # Hiển thị túi đồ
    inventory = user_data.get("inventory", [])
    if not inventory:
        text = "🎒 **Túi Đồ** 🎒\n❌ Túi đồ trống!\nHãy mua vật phẩm ở **Shop** hoặc quay **Gacha**! 🛒\nQuay lại /menu."
    else:
        text = "🎒 **Túi Đồ** 🎒\n**Danh sách vật phẩm**:\n" + "\n".join([f"- **{items[item_id]['name']}** (ID: {item_id})" for item_id in inventory]) + "\nQuay lại /menu."
    
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý sự kiện
async def handle_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query
    query = update.callback_query
    
    # Hiển thị sự kiện (giả lập)
    text = (
        "🎉 **Sự Kiện Đặc Biệt** 🎉\n"
        "─────────────────\n"
        "- 🐉 **Săn Rồng Huyền Thoại**: Đối mặt với rồng cổ đại!\n"
        "- ✨ **Lễ Hội Phép Thuật**: Nhận thưởng độc quyền!\n"
        "─────────────────\n"
        "Tham gia sự kiện để nhận phần thưởng! (Chưa khả dụng)\nQuay lại /menu."
    )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý Gacha
async def handle_gacha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng và vật phẩm
    user_data = get_user_data(telegram_id)
    items = read_items()
    
    # Kiểm tra vàng
    if user_data["gold"] < 200:
        await query.edit_message_text(
            text="🎰 **Gacha May Mắn** 🎰\n❌ Bạn cần **200 vàng** để quay!\nHãy kiếm thêm vàng! 💰\nQuay lại /menu.",
            parse_mode="Markdown"
        )
        return
    
    # Trừ vàng và quay Gacha
    user_data["gold"] -= 200
    rewards = ["ITEM001", "ITEM002", "ITEM004"]
    reward_id = random.choice(rewards)
    user_data["inventory"].append(reward_id)
    update_user_data(telegram_id, user_data)
    
    await query.edit_message_text(
        text=f"🎰 **Gacha May Mắn** 🎰\n✅ Bạn nhận được **{items[reward_id]['name']}** (ID: {reward_id})! 🎉\nQuay lại /menu.",
        parse_mode="Markdown"
    )

# Hàm xử lý nhiệm vụ
async def handle_quest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    
    # Hiển thị nhiệm vụ
    quests = user_data.get("quests", [])
    if not quests:
        # Thêm nhiệm vụ mẫu
        user_data["quests"] = [{"title": "Săn 5 quái vật", "progress": 0, "total": 5, "reward": 300}]
        update_user_data(telegram_id, user_data)
        quests = user_data["quests"]
    
    text = "📋 **Nhiệm Vụ** 📋\n**Danh sách nhiệm vụ**:\n" + "\n".join([f"- **{q['title']}** ({q['progress']}/{q['total']})" for q in quests]) + "\nQuay lại /menu."
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý bạn bè
async def handle_friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    
    # Hiển thị danh sách bạn bè
    friends = user_data.get("friends", [])
    if not friends:
        text = "👥 **Bạn Bè** 👥\n❌ Bạn chưa có bạn bè nào!\nHãy kết bạn để cùng phiêu lưu! 😊\nQuay lại /menu."
    else:
        text = "👥 **Bạn Bè** 👥\n**Danh sách bạn bè**:\n" + "\n".join([f"- **{friend}**" for friend in friends]) + "\nQuay lại /menu."
    
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

# Hàm xử lý chiến đấu
async def handle_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy query và telegram_id
    query = update.callback_query
    telegram_id = query.from_user.id
    
    # Lấy dữ liệu người dùng
    user_data = get_user_data(telegram_id)
    user_stats = user_data["stats"]
    
    # Tạo quái vật giả lập
    monster = {
        "name": "Quái Vật Hắc Ám",
        "hp": 100,
        "atk": 15,
        "def": 10,
        "speed": 12
    }
    
    # Xác định lượt đi dựa trên SPEED
    user_turn = user_stats["speed"] >= monster["speed"]
    
    # Biến theo dõi trận đấu
    user_hp = user_stats["hp"]
    monster_hp = monster["hp"]
    battle_log = ["⚔️ **Trận Chiến Bắt Đầu** ⚔️"]
    
    while user_hp > 0 and monster_hp > 0:
        if user_turn:
            # Lượt của người chơi
            # Tính tỉ lệ né của quái
            dodge_chance = monster["speed"] / (monster["speed"] + 100)
            if random.random() < dodge_chance:
                battle_log.append(f"🔥 **{monster['name']}** né được đòn!")
            else:
                # Tính sát thương
                damage = max(0, user_stats["atk"] - monster["def"] // 2)
                if user_data["role"] in ["Pháp Sư", "Thuật Sư"]:
                    # Pháp Sư, Thuật Sư dùng MAGIC cho kỹ năng
                    damage = max(0, user_stats["magic"] - monster["def"] // 2)
                monster_hp -= damage
                battle_log.append(f"🗡️ Bạn gây **{damage} sát thương** lên **{monster['name']}** (HP: {monster_hp})")
        else:
            # Lượt của quái
            # Tính tỉ lệ né của người chơi
            dodge_chance = user_stats["speed"] / (user_stats["speed"] + 100)
            if random.random() < dodge_chance:
                battle_log.append(f"🔥 Bạn né được đòn của **{monster['name']}**!")
            else:
                # Tính sát thương
                damage = max(0, monster["atk"] - user_stats["def"] // 2)
                user_hp -= damage
                battle_log.append(f"👹 **{monster['name']}** gây **{damage} sát thương** lên bạn (HP: {user_hp})")
        
        # Đổi lượt
        user_turn = not user_turn
    
    # Kết thúc trận đấu
    if user_hp > 0:
        user_data["battles_won"] += 1
        user_data["gold"] += 50
        user_data["exp"] += 20
        if user_data["exp"] >= user_data["max_exp"]:
            user_data["level"] += 1
            user_data["exp"] = 0
            user_data["max_exp"] += 50
            user_data["stats"]["hp"] += 10
            user_data["stats"]["atk"] += 2
            user_data["stats"]["magic"] += 2
            user_data["stats"]["def"] += 2
            user_data["stats"]["speed"] += 2
            user_data["stats"]["mana"] += 10
            battle_log.append("🎉 **Bạn đã lên cấp!**")
        update_user_data(telegram_id, user_data)
        battle_log.append("🏆 **Bạn thắng!** Nhận **50 vàng** và **20 EXP**!")
    else:
        battle_log.append("😔 **Bạn đã thua!** Hãy thử lại.")
    
    # Hiển thị kết quả
    await query.edit_message_text(
        text="\n".join(battle_log) + "\nQuay lại /menu.",
        parse_mode="Markdown"
    )