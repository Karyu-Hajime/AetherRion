from telegram import Update
from telegram.ext import ContextTypes
from database import get_user_data

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    user_data = get_user_data(telegram_id)
    stats = user_data["stats"]
    skills = user_data.get("skills", [])
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
        f"**Kỹ năng**: {', '.join(skills) if skills else 'Chưa có'}\n"
        "─────────────────\n"
        "Quay lại /menu."
    )
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )