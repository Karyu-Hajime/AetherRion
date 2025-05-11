from database import get_user_data, update_user_data, read_items

def use_item(telegram_id, item_id):
    user_data = get_user_data(telegram_id)
    items = read_items()
    item = items.get(item_id)
    
    if not item:
        return
    
    effects = item.get("effects", {})
    stats = user_data["stats"]
    
    # Xử lý hiệu ứng theo danh mục
    if item["category"] in ["vũ khí", "trang bị", "đá quý"]:
        for stat, value in effects.items():
            if stat in stats:
                stats[stat] += value
    elif item["category"] == "sách kỹ năng":
        skill = effects.get("skill")
        if skill and skill not in user_data["skills"]:
            user_data["skills"].append(skill)
    elif item["category"] in ["đồ ăn", "thuốc"]:
        for stat, value in effects.items():
            if stat in stats:
                stats[stat] = min(stats[stat] + value, stats[stat] * 2)  # Giới hạn hồi phục
    
    user_data["stats"] = stats
    update_user_data(telegram_id, user_data)