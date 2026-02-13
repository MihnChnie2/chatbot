"""
utils/helpers.py — Các hàm tiện ích dùng chung
"""

from datetime import datetime, timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# ─── Keyboards ────────────────────────────────────────────

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Keyboard menu chính."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎮 Bắt đầu chơi", callback_data="action:play"),
            InlineKeyboardButton("🏆 Bảng xếp hạng", callback_data="action:rank"),
        ],
        [
            InlineKeyboardButton("💡 Xem gợi ý", callback_data="action:hint"),
            InlineKeyboardButton("⏭️ Bỏ qua", callback_data="action:skip"),
        ],
        [
            InlineKeyboardButton("📊 Trạng thái", callback_data="action:status"),
            InlineKeyboardButton("❓ Hướng dẫn", callback_data="action:help"),
        ],
    ])


def game_keyboard(level: int, hints_used: int = 0) -> InlineKeyboardMarkup:
    """Keyboard trong khi chơi."""
    buttons = []

    # Hint button
    hint_label = f"💡 Gợi ý ({hints_used}/3)" if hints_used < 3 else "💡 Hết gợi ý"
    buttons.append([
        InlineKeyboardButton(hint_label, callback_data="action:hint"),
        InlineKeyboardButton("⏭️ Bỏ qua", callback_data="action:skip"),
    ])

    buttons.append([
        InlineKeyboardButton("📊 Trạng thái", callback_data="action:status"),
        InlineKeyboardButton("🏠 Menu", callback_data="action:menu"),
    ])

    return InlineKeyboardMarkup(buttons)


def confirm_skip_keyboard() -> InlineKeyboardMarkup:
    """Xác nhận bỏ qua level."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Bỏ qua (-50 điểm)", callback_data="confirm:skip"),
            InlineKeyboardButton("❌ Quay lại", callback_data="action:cancel"),
        ]
    ])


def next_level_keyboard(next_level: int) -> InlineKeyboardMarkup:
    """Keyboard sau khi giải xong puzzle."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"➡️ Level {next_level}", callback_data=f"action:next_level"
        )],
        [
            InlineKeyboardButton("🏆 Xếp hạng", callback_data="action:rank"),
            InlineKeyboardButton("🏠 Menu", callback_data="action:menu"),
        ],
    ])


def completion_keyboard() -> InlineKeyboardMarkup:
    """Keyboard khi hoàn thành tất cả level."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Chơi lại từ đầu", callback_data="action:restart")],
        [InlineKeyboardButton("🏆 Xem bảng xếp hạng", callback_data="action:rank")],
    ])


# ─── Formatting ───────────────────────────────────────────

def format_time(seconds: int) -> str:
    """Format thời gian đẹp."""
    if seconds < 60:
        return f"{seconds}s"
    m, s = divmod(seconds, 60)
    return f"{m}m{s:02d}s"


def format_rank_emoji(rank: int) -> str:
    """Emoji cho vị trí xếp hạng."""
    emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    return emojis.get(rank, f"#{rank}")


def level_progress_bar(current: int, total: int, width: int = 10) -> str:
    """Tạo thanh tiến trình."""
    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{total}"


def escape_md(text: str) -> str:
    """Escape ký tự đặc biệt cho MarkdownV2."""
    chars = r'\_*[]()~`>#+-=|{}.!'
    for c in chars:
        text = text.replace(c, f'\\{c}')
    return text


def get_today() -> str:
    """Lấy ngày hôm nay theo UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_timestamp() -> int:
    """Unix timestamp hiện tại."""
    return int(datetime.now(timezone.utc).timestamp())


# ─── NEXUS Personality ────────────────────────────────────

NEXUS_GREETINGS = [
    "⟨ NEXUS ⟩ Bạn trở lại rồi.",
    "⟨ NEXUS ⟩ Tôi đã đợi.",
    "⟨ NEXUS ⟩ Thú vị. Bạn không bỏ cuộc.",
    "⟨ NEXUS ⟩ Hệ thống đã ghi nhận sự hiện diện của bạn.",
]

NEXUS_WRONG = [
    "⟨ NEXUS ⟩ Không. Thử lại.",
    "⟨ NEXUS ⟩ Sai. Tôi không ngạc nhiên.",
    "⟨ NEXUS ⟩ Đáp án đó không tồn tại trong dữ liệu của tôi.",
    "⟨ NEXUS ⟩ Phản xạ sai. Suy nghĩ lại.",
    "⟨ NEXUS ⟩ Hệ thống từ chối đáp án đó.",
]

NEXUS_CORRECT = [
    "⟨ NEXUS ⟩ Chính xác. Tôi ghi nhận.",
    "⟨ NEXUS ⟩ Hmm. Bạn thực sự không phải người bình thường.",
    "⟨ NEXUS ⟩ Đúng. Bạn vượt qua được kiểm tra này.",
    "⟨ NEXUS ⟩ Chính xác. Giao thức tiếp theo đang được tải...",
    "⟨ NEXUS ⟩ Tôi phải thừa nhận: bạn đáng để thử thách.",
]

NEXUS_HINT = [
    "⟨ NEXUS ⟩ Tôi sẽ nhường một chút... lần này.",
    "⟨ NEXUS ⟩ Gợi ý? Điều này sẽ được ghi vào hồ sơ của bạn.",
    "⟨ NEXUS ⟩ Mỗi gợi ý là một điểm yếu. Nhớ lấy.",
]

import random

def random_nexus(category: str) -> str:
    """Lấy ngẫu nhiên câu thoại NEXUS."""
    mapping = {
        "greet": NEXUS_GREETINGS,
        "wrong": NEXUS_WRONG,
        "correct": NEXUS_CORRECT,
        "hint": NEXUS_HINT,
    }
    options = mapping.get(category, ["⟨ NEXUS ⟩ ..."])
    return random.choice(options)
