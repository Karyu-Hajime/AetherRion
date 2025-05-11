# Nhập thư viện JSON và UUID
import json
import uuid
import os
import logging

# Thiết lập logging
logger = logging.getLogger(__name__)

# Đường dẫn file JSON
DATA_FILE = "data/game_data.json"
ITEMS_FILE = "data/items.json"
GIFTCODES_FILE = "data/giftcodes.json"

# Hàm khởi tạo file JSON nếu chưa tồn tại
def init_db():
    # Tạo thư mục data nếu chưa tồn tại
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Kiểm tra và tạo file game_data.json
    if not os.path.exists(DATA_FILE):
        logger.info("Tạo file game_data.json mới")
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f, indent=4)
    
    # Kiểm tra và tạo file items.json
    if not os.path.exists(ITEMS_FILE):
        logger.info("Tạo file items.json mới")
        items = {
            "ITEM001": {
                "name": "Kiếm Lửa Sơ Cấp",
                "category": "vũ khí",
                "role": "Chiến Binh",
                "tier": "sơ cấp",
                "price": 500,
                "description": "Kiếm rực cháy, tăng ATK +10.",
                "effects": {"atk": 10}
            },
            "ITEM002": {
                "name": "Áo Giáp Vàng Trung Cấp",
                "category": "trang bị",
                "role": "Chiến Binh",
                "tier": "trung cấp",
                "price": 800,
                "description": "Áo giáp tăng DEF +15.",
                "effects": {"def": 15}
            },
            "ITEM003": {
                "name": "Thú Cưng Rồng",
                "category": "pet",
                "role": "all",
                "tier": "cao cấp",
                "price": 1000,
                "description": "Rồng nhỏ hỗ trợ chiến đấu, tăng ATK +20.",
                "effects": {"atk": 20, "power": 50}
            },
            "ITEM004": {
                "name": "Sách Phép Hỏa Cầu",
                "category": "sách kỹ năng",
                "role": "Pháp Sư",
                "tier": "sơ cấp",
                "price": 600,
                "description": "Học kỹ năng Hỏa Cầu, gây sát thương phép.",
                "effects": {"skill": "Hỏa Cầu"}
            },
            "ITEM005": {
                "name": "Thuốc Hồi Máu",
                "category": "thuốc",
                "role": "all",
                "tier": "sơ cấp",
                "price": 200,
                "description": "Hồi 50 HP.",
                "effects": {"hp": 50}
            },
            "ITEM006": {
                "name": "Đá Tốc Độ",
                "category": "đá quý",
                "role": "Cung Thủ",
                "tier": "trung cấp",
                "price": 700,
                "description": "Tăng SPEED +10.",
                "effects": {"speed": 10}
            },
            "ITEM007": {
                "name": "Bánh Mana",
                "category": "đồ ăn",
                "role": "all",
                "tier": "sơ cấp",
                "price": 150,
                "description": "Hồi 30 Mana.",
                "effects": {"mana": 30}
            },
            "ITEM008": {
                "name": "Cung Bão Tố Tuyệt Phẩm",
                "category": "vũ khí",
                "role": "Cung Thủ",
                "tier": "tuyệt phẩm",
                "price": 2000,
                "description": "Cung bắn ra mũi tên sét, tăng ATK +50, 10% gây choáng.",
                "effects": {"atk": 50, "stun_chance": 0.1}
            },
            "ITEM009": {
                "name": "Gậy Phép Băng",
                "category": "vũ khí",
                "role": "Pháp Sư",
                "tier": "trung cấp",
                "price": 900,
                "description": "Gậy phép băng, tăng MAGIC +20.",
                "effects": {"magic": 20}
            },
            "ITEM010": {
                "name": "Áo Choàng Hắc Ám",
                "category": "trang bị",
                "role": "Thuật Sư",
                "tier": "cao cấp",
                "price": 1200,
                "description": "Áo choàng tăng DEF +20, MANA +50.",
                "effects": {"def": 20, "mana": 50}
            }
        }
        with open(ITEMS_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4)
    
    # Kiểm tra và tạo file giftcodes.json
    if not os.path.exists(GIFTCODES_FILE):
        logger.info("Tạo file giftcodes.json mới")
        giftcodes = {
            "WELCOME2025": {
                "reward": {"gold": 100, "items": ["ITEM005"]},
                "used_by": [],
                "expires_at": "2025-12-31T23:59:59Z"
            },
            "EVENTSUMMER": {
                "reward": {"gold": 200, "items": ["ITEM007"]},
                "used_by": [],
                "expires_at": "2025-08-31T23:59:59Z"
            },
            "VIPCODE001": {
                "reward": {"gold": 500, "items": ["ITEM006"]},
                "used_by": [],
                "expires_at": "2025-06-30T23:59:59Z"
            }
        }
        with open(GIFTCODES_FILE, "w", encoding="utf-8") as f:
            json.dump(giftcodes, f, indent=4)

# Hàm đọc dữ liệu từ file JSON
def read_db():
    try:
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            logger.warning("File game_data.json không tồn tại hoặc rỗng, khởi tạo mặc định")
            init_db()
            return {"users": {}}
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Lỗi đọc JSON từ game_data.json: {e}")
        init_db()
        return {"users": {}}

# Hàm ghi dữ liệu vào file JSON
def write_db(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Lỗi ghi JSON vào game_data.json: {e}")

# Hàm đọc danh sách vật phẩm
def read_items():
    try:
        if not os.path.exists(ITEMS_FILE):
            logger.warning("File items.json không tồn tại, khởi tạo mặc định")
            init_db()
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Lỗi đọc JSON từ items.json: {e}")
        init_db()
        return {}

# Hàm đọc danh sách giftcode
def read_giftcodes():
    try:
        if not os.path.exists(GIFTCODES_FILE):
            logger.warning("File giftcodes.json không tồn tại, khởi tạo mặc định")
            init_db()
        with open(GIFTCODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Lỗi đọc JSON từ giftcodes.json: {e}")
        init_db()
        return {}

# Hàm ghi danh sách giftcode
def write_giftcodes(giftcodes):
    try:
        with open(GIFTCODES_FILE, "w", encoding="utf-8") as f:
            json.dump(giftcodes, f, indent=4)
    except Exception as e:
        logger.error(f"Lỗi ghi JSON vào giftcodes.json: {e}")

# Hàm kiểm tra xem người dùng đã đăng ký chưa
def is_user_registered(telegram_id):
    data = read_db()
    telegram_id_str = str(telegram_id)
    return telegram_id_str in data["users"] and "accounts" in data["users"][telegram_id_str]

# Hàm đăng ký người dùng
def register_user(telegram_id, username, password, role):
    data = read_db()
    uid = f"DRA{str(uuid.uuid4())[:8].upper()}"
    base_stats = {
        "Chiến Binh": {"hp": 120, "atk": 20, "magic": 5, "def": 15, "speed": 10, "mana": 50},
        "Pháp Sư": {"hp": 80, "atk": 5, "magic": 25, "def": 5, "speed": 8, "mana": 100},
        "Cung Thủ": {"hp": 100, "atk": 15, "magic": 5, "def": 10, "speed": 20, "mana": 60},
        "Thuật Sư": {"hp": 90, "atk": 8, "magic": 20, "def": 8, "speed": 15, "mana": 80}
    }
    user_data = {
        "uid": uid,
        "username": username,
        "password": password,
        "role": role,
        "level": 1,
        "exp": 0,
        "max_exp": 100,
        "gold": 100,
        "inventory": [],
        "pets": [],
        "quests": [],
        "friends": [],
        "mail": [],
        "battles_won": 0,
        "checkin_count": 0,
        "stats": base_stats[role],
        "skills": []
    }
    telegram_id_str = str(telegram_id)
    logger.info(f"Registering user for telegram_id: {telegram_id_str}, current user data: {data.get('users', {}).get(telegram_id_str)}")
    
    # Khởi tạo hoặc sửa cấu trúc nếu cần
    if telegram_id_str not in data["users"] or "accounts" not in data["users"].get(telegram_id_str, {}):
        data["users"][telegram_id_str] = {"accounts": []}
    
    data["users"][telegram_id_str]["accounts"].append(user_data)
    write_db(data)
    logger.info(f"Registered user {username} with UID {uid} for telegram_id {telegram_id_str}")
    return uid

# Hàm kiểm tra đăng nhập
def check_login(uid, password):
    data = read_db()
    for telegram_id, user_data in data["users"].items():
        if "accounts" in user_data:
            for account in user_data["accounts"]:
                if account["uid"] == uid and account["password"] == password:
                    return account
    return None

# Hàm lấy dữ liệu người dùng
def get_user_data(telegram_id, uid=None):
    data = read_db()
    telegram_id_str = str(telegram_id)
    if telegram_id_str not in data["users"] or "accounts" not in data["users"][telegram_id_str]:
        return None
    accounts = data["users"][telegram_id_str]["accounts"]
    if uid:
        for account in accounts:
            if account["uid"] == uid:
                return account
    return accounts[-1] if accounts else None

# Hàm cập nhật dữ liệu người dùng
def update_user_data(telegram_id, updated_data):
    data = read_db()
    telegram_id_str = str(telegram_id)
    if telegram_id_str not in data["users"] or "accounts" not in data["users"][telegram_id_str]:
        return
    accounts = data["users"][telegram_id_str]["accounts"]
    for i, account in enumerate(accounts):
        if account["uid"] == updated_data["uid"]:
            accounts[i] = updated_data
            break
    write_db(data)

# Hàm lấy telegram_id từ UID
def get_telegram_id_from_uid(uid):
    data = read_db()
    for telegram_id, user_data in data["users"].items():
        if "accounts" in user_data:
            for account in user_data["accounts"]:
                if account["uid"] == uid:
                    return telegram_id
    return None