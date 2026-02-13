# 🔐 CIPHER PROTOCOL — Telegram Crypto Bot

> *"Câu đố không phải để chứng minh bạn thông minh. Nó là để người chơi cảm thấy họ thông minh."*

Bot Telegram giải mật mã với bối cảnh câu chuyện xuyên suốt — NEXUS, một AI bí ẩn, đang kiểm tra bạn.

---

## 🎭 Bối cảnh (Lore)

Người chơi là **Đặc vụ 0x00** — danh tính bị xoá, đang bị kiểm tra bởi **NEXUS**, một AI kiểm soát tổ chức bí mật CIPHER. Mỗi câu đố là một "giao thức kiểm tra" với lời dẫn chuyện từ NEXUS.

---

## 📁 Cấu trúc dự án

```
bot/
├── main.py                  # Entry point
├── requirements.txt
├── cipher_protocol.db       # SQLite (tự tạo)
│
├── handlers/
│   ├── commands.py          # /start /level /hint /skip /rank /status /help
│   ├── messages.py          # Kiểm tra đáp án
│   └── callbacks.py         # Inline button callbacks
│
├── puzzles/
│   ├── puzzle_data.py       # 10 câu đố + daily pool
│   └── scoring.py           # Tính điểm, kiểm tra đáp án
│
├── database/
│   └── db.py                # SQLite operations
│
└── utils/
    ├── helpers.py            # Keyboards, formatting, NEXUS personality
    └── scheduler.py          # Daily puzzle scheduler
```

---

## 🚀 Cài đặt & Chạy

### 1. Tạo bot Telegram

Nhắn tin với [@BotFather](https://t.me/BotFather):
```
/newbot
```
Lấy token dạng: `1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`

### 2. Cài thư viện

```bash
pip install -r requirements.txt
```

### 3. Cấu hình token

**Cách A** — Biến môi trường (khuyến nghị):
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
python main.py
```

**Cách B** — Sửa trực tiếp trong `main.py`:
```python
BOT_TOKEN = "your_token_here"
```

### 4. Chạy bot

```bash
cd bot/
python main.py
```

---

## 🎮 Các lệnh

| Lệnh | Mô tả |
|------|-------|
| `/start` | Màn hình chào mừng, tạo tài khoản |
| `/level` | Câu đố hiện tại |
| `/hint` | Gợi ý (trừ 25% điểm/hint) |
| `/skip` | Bỏ qua (trừ 50 điểm, reset combo) |
| `/rank` | Bảng xếp hạng top 10 |
| `/status` | Trạng thái người chơi |
| `/help` | Hướng dẫn đầy đủ |

---

## 🧩 10 Level Câu đố

| Level | ID | Loại | Độ khó |
|-------|----|------|--------|
| 1 | L01_CAESAR | 🔐 Caesar Cipher | ⭐ |
| 2 | L02_MORSE | 🔐 Morse Code | ⭐⭐ |
| 3 | L03_BINARY | 🔐 Binary → ASCII | ⭐⭐ |
| 4 | L04_ATBASH | 🔐 Atbash Cipher | ⭐⭐⭐ |
| 5 | L05_LOGIC | 🧩 Logic (ai nói dối?) | ⭐⭐⭐ |
| 6 | L06_BASE64 | 🔐 Base64 | ⭐⭐⭐ |
| 7 | L07_REVERSE | 🔐 Reverse String | ⭐⭐ |
| 8 | L08_RIDDLE | 🤯 Đố mẹo tâm lý | ⭐⭐⭐ |
| 9 | L09_MULTILAYER | 🕵️ Morse+ROT13+Reverse | ⭐⭐⭐⭐ |
| 10 | L10_BOSS | 👑 Boss: Reverse+Base64 | ⭐⭐⭐⭐⭐ |

---

## 💰 Hệ thống điểm

### Công thức tính điểm
```
final = base_score × time_mult × hint_mult × wrong_mult × combo_mult
```

### Multipliers
| Điều kiện | Hệ số |
|-----------|-------|
| Giải ≤ 30 giây | ×1.5 (Speed!) |
| Giải ≤ 60 giây | ×1.2 |
| Giải ≤ 120 giây | ×1.0 |
| Giải ≤ 300 giây | ×0.8 |
| Giải > 300 giây | ×0.6 |
| Mỗi hint dùng | ×0.75 |
| Mỗi lần sai | ×0.9 |
| Combo ×N | ×(1 + min(0.5, N×0.1)) |

### Base score
- Level 1–4: 100–250 pts
- Level 5–7: 300–350 pts
- Level 8–9: 350–500 pts
- Level 10 (Boss): 1000 pts

---

## 🗃️ Database Schema

```sql
players         -- User info, score, level, combo
active_sessions -- Câu đố đang chơi, thời gian bắt đầu
solve_history   -- Lịch sử giải đố
daily_puzzle    -- Câu đố ngày
daily_solves    -- Ai đã giải daily
```

---

## ➕ Thêm câu đố mới

Thêm vào `puzzles/puzzle_data.py`:

```python
{
    "id": "L11_NEW",
    "level": 11,
    "category": "🔐 Mật mã học",
    "lore": "⟨ NEXUS ⟩ ...",          # Câu chuyện
    "question": "...",                 # Câu hỏi (Markdown)
    "answer": "đáp án",               # Lowercase
    "alt_answers": ["variant"],       # Chấp nhận thêm
    "hints": ["h1", "h2", "h3"],      # 3 gợi ý
    "explanation": "...",             # Giải thích
    "base_score": 400,
    "time_bonus": True,
}
```

---

## 🏗️ Mở rộng

### Thêm multiplayer
- Tạo bảng `challenges` cho PvP
- Dùng `InlineKeyboardButton` với `switch_inline_query`

### Daily puzzle tốt hơn
- Tăng pool trong `DAILY_POOL`
- Dùng ngày làm seed để consistent

### Puzzle sinh ngẫu nhiên
```python
import random
# Caesar với shift ngẫu nhiên
shift = random.randint(1, 25)
```

### ARG Mini (Alternate Reality Game)
- Ẩn mã trong username bot
- Câu đố yêu cầu tìm manh mối trên web

---

## 🔧 Cấu hình nâng cao

```python
# Trong main.py
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Trong database/db.py
DB_PATH = "/path/to/your/database.db"
```

---

*CIPHER PROTOCOL — Because the best puzzle makes the player feel smart.*
