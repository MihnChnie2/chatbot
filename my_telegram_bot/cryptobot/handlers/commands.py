"""
handlers/commands.py — Xử lý các lệnh /start, /level, /hint, /skip, /rank, /status
"""

import logging
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.db import (
    get_or_create_player, get_player, get_session,
    start_session, update_session, end_session,
    update_player, get_leaderboard, record_solve,
    get_daily_puzzle, has_solved_daily
)
from puzzles.puzzle_data import PUZZLE_BY_LEVEL, MAX_LEVEL, PUZZLE_BY_ID, DAILY_POOL
from puzzles.scoring import calculate_score, format_score_breakdown
from utils.helpers import (
    main_menu_keyboard, game_keyboard, confirm_skip_keyboard,
    next_level_keyboard, level_progress_bar, format_rank_emoji,
    random_nexus, get_today, get_timestamp, format_time
)

logger = logging.getLogger(__name__)


# ─── /start ───────────────────────────────────────────────

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Màn hình chào mừng và tạo profile."""
    user = update.effective_user
    player = get_or_create_player(
        user.id,
        user.username or "",
        user.full_name or "Unknown"
    )

    is_new = player["total_score"] == 0 and player["current_level"] == 1

    if is_new:
        text = (
            "```\n"
            "╔══════════════════════════════════╗\n"
            "║   C I P H E R  P R O T O C O L  ║\n"
            "║      Hệ thống kiểm tra bí mật    ║\n"
            "╚══════════════════════════════════╝\n"
            "```\n\n"
            "⟨ NEXUS — KHỞI ĐỘNG ⟩\n\n"
            "Phát hiện đặc vụ mới.\n"
            f"ID: `0x{user.id % 0xFFFF:04X}`\n"
            f"Tên hiển thị: *{user.full_name}*\n\n"
            "Danh tính thật của bạn đã bị xoá.\n"
            "Từ bây giờ, bạn là *Đặc vụ 0x00*.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🎯 Nhiệm vụ: Vượt qua 10 cấp độ kiểm tra\n"
            "🔐 Phân loại: Mật mã • Logic • Đố mẹo • Đa tầng\n"
            "👾 Kẻ thù: NEXUS — AI kiểm soát hệ thống\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "_Gõ /level để bắt đầu thử thách đầu tiên._"
        )
    else:
        level = player["current_level"]
        progress = level_progress_bar(min(level - 1, MAX_LEVEL), MAX_LEVEL)
        text = (
            f"{random_nexus('greet')}\n\n"
            f"*Đặc vụ:* {user.full_name}\n"
            f"*Level hiện tại:* {level}/{MAX_LEVEL}\n"
            f"*Điểm số:* {player['total_score']:,}\n"
            f"*Tiến trình:* {progress}\n\n"
            "_Gõ /level để tiếp tục._"
        )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )


# ─── /level ───────────────────────────────────────────────

async def level_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hiển thị câu đố hiện tại."""
    user = update.effective_user
    player = get_player(user.id)

    if not player:
        await update.message.reply_text(
            "Bạn chưa đăng ký. Gõ /start để bắt đầu."
        )
        return

    level = player["current_level"]

    # Đã hoàn thành tất cả?
    if level > MAX_LEVEL:
        await _send_completion(update, player)
        return

    puzzle = PUZZLE_BY_LEVEL.get(level)
    if not puzzle:
        await update.message.reply_text("⚠️ Không tìm thấy câu đố. Liên hệ admin.")
        return

    # Bắt đầu session
    session = get_session(user.id)
    if not session or session["puzzle_id"] != puzzle["id"]:
        start_session(user.id, puzzle["id"], level)

    await _send_puzzle(update, puzzle, level, hints_used=0)


async def _send_puzzle(update, puzzle: dict, level: int, hints_used: int) -> None:
    """Gửi câu đố tới người dùng."""
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *LEVEL {level}/{MAX_LEVEL}* — {puzzle['category']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{puzzle['lore']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{puzzle['question']}\n\n"
        f"📝 _Nhập đáp án ngay trong chat_"
    )

    if update.callback_query:
        await update.callback_query.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=game_keyboard(level, hints_used)
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=game_keyboard(level, hints_used)
        )


async def _send_completion(update, player) -> None:
    """Màn hoàn thành toàn bộ game."""
    from utils.helpers import completion_keyboard
    text = (
        "```\n"
        "╔══════════════════════════════════╗\n"
        "║  🎉  GIAO THỨC HOÀN THÀNH  🎉   ║\n"
        "╚══════════════════════════════════╝\n"
        "```\n\n"
        "⟨ NEXUS — THÔNG ĐIỆP CUỐI ⟩\n\n"
        "Đặc vụ 0x00...\n\n"
        "Bạn đã vượt qua tất cả 10 cấp độ.\n"
        "Tôi phải thừa nhận: tôi đã nhầm khi đánh giá thấp bạn.\n\n"
        "CIPHER chào đón bạn.\n"
        "Hay chính xác hơn: *bạn đã tự chứng minh mình xứng đáng*.\n\n"
        f"📊 *Điểm cuối cùng:* {player['total_score']:,}\n"
        f"🔥 *Combo cao nhất:* {player['max_combo']}\n"
        f"💡 *Gợi ý đã dùng:* {player['hints_used']}\n\n"
        "_Giao thức kết thúc. Hoặc... mới bắt đầu?_"
    )

    send_func = update.callback_query.message.reply_text if update.callback_query else update.message.reply_text
    await send_func(text, parse_mode=ParseMode.MARKDOWN, reply_markup=completion_keyboard())


# ─── /hint ────────────────────────────────────────────────

async def hint_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gợi ý cho câu đố hiện tại."""
    user = update.effective_user
    session = get_session(user.id)

    if not session:
        await update.message.reply_text(
            "Bạn chưa có câu đố nào. Gõ /level để bắt đầu."
        )
        return

    puzzle = PUZZLE_BY_ID.get(session["puzzle_id"])
    if not puzzle:
        await update.message.reply_text("⚠️ Lỗi: không tìm thấy câu đố.")
        return

    hints = puzzle.get("hints", [])
    hints_used = session["hints_used"]

    if hints_used >= len(hints):
        text = (
            f"{random_nexus('hint')}\n\n"
            "❌ Bạn đã dùng hết gợi ý cho câu đố này.\n"
            "_Không có thêm manh mối nào được phép._"
        )
    else:
        hint = hints[hints_used]
        new_hints_used = hints_used + 1
        update_session(user.id, hints_used=new_hints_used)

        text = (
            f"{random_nexus('hint')}\n\n"
            f"💡 *Gợi ý #{new_hints_used}/{len(hints)}:*\n\n"
            f"{hint}\n\n"
            f"_⚠️ Điểm sẽ bị trừ {25}% vì dùng gợi ý._"
        )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=game_keyboard(session["level"], session["hints_used"])
    )


# ─── /skip ────────────────────────────────────────────────

async def skip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bỏ qua câu đố (xác nhận trước)."""
    user = update.effective_user
    session = get_session(user.id)

    if not session:
        await update.message.reply_text(
            "Không có câu đố nào để bỏ qua. Gõ /level để bắt đầu."
        )
        return

    await update.message.reply_text(
        "⟨ NEXUS ⟩\n\n"
        "Bạn muốn bỏ qua?\n"
        "Điều này sẽ bị ghi vào hồ sơ.\n\n"
        "⚠️ *Chi phí:* -50 điểm và mất streak combo.\n\n"
        "_Bạn có chắc không?_",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=confirm_skip_keyboard()
    )


# ─── /rank ────────────────────────────────────────────────

async def rank_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hiển thị bảng xếp hạng top 10."""
    leaders = get_leaderboard(10)

    if not leaders:
        await update.message.reply_text("Chưa có ai trên bảng xếp hạng.")
        return

    lines = ["🏆 *BẢNG XẾP HẠNG — CIPHER PROTOCOL*\n"]
    for i, p in enumerate(leaders, 1):
        name = p["full_name"] or p["username"] or f"Agent #{p['user_id'] % 9999}"
        emoji = format_rank_emoji(i)
        lines.append(
            f"{emoji} *{name}*\n"
            f"   📊 {p['total_score']:,} pts • Level {p['current_level']}/{MAX_LEVEL} • 🔥x{p['max_combo']}"
        )

    # Hiển thị vị trí người dùng hiện tại
    user = update.effective_user
    player = get_player(user.id)
    if player:
        all_leaders = get_leaderboard(100)
        my_rank = next(
            (i + 1 for i, p in enumerate(all_leaders) if p["user_id"] == user.id),
            "N/A"
        )
        lines.append(f"\n👤 *Bạn:* Hạng #{my_rank} — {player['total_score']:,} pts")

    await update.message.reply_text(
        "\n".join(lines),
        parse_mode=ParseMode.MARKDOWN
    )


# ─── /status ──────────────────────────────────────────────

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hiển thị trạng thái người chơi hiện tại."""
    user = update.effective_user
    player = get_player(user.id)

    if not player:
        await update.message.reply_text("Gõ /start để tạo tài khoản.")
        return

    session = get_session(user.id)
    level = player["current_level"]
    progress = level_progress_bar(min(level - 1, MAX_LEVEL), MAX_LEVEL)

    text = (
        "⟨ NEXUS — HỒ SƠ ĐẶC VỤ ⟩\n\n"
        f"👤 *{user.full_name}*\n"
        f"🆔 `0x{user.id % 0xFFFF:04X}`\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *Level:* {level}/{MAX_LEVEL}\n"
        f"📈 *Tiến trình:* {progress}\n"
        f"💰 *Tổng điểm:* {player['total_score']:,}\n"
        f"🔥 *Combo hiện tại:* {player['combo']}\n"
        f"🏅 *Combo cao nhất:* {player['max_combo']}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 *Gợi ý đã dùng:* {player['hints_used']}\n"
        f"⏭️ *Bỏ qua:* {player['skips_used']}\n"
        f"❌ *Trả lời sai:* {player['wrong_answers']}\n"
    )

    if session:
        puzzle = PUZZLE_BY_ID.get(session["puzzle_id"])
        if puzzle:
            elapsed = get_timestamp() - int(
                datetime.fromisoformat(session["started_at"].replace("Z", "+00:00")).timestamp()
                if "T" in session["started_at"] else
                datetime.strptime(session["started_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
            )
            text += (
                f"\n⏱️ *Câu đố hiện tại:* Level {session['level']}\n"
                f"🕐 *Thời gian đã dùng:* {format_time(elapsed)}\n"
                f"💡 *Hint đã dùng:* {session['hints_used']}/3\n"
            )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )


# ─── /help ────────────────────────────────────────────────

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hướng dẫn chơi."""
    text = (
        "⟨ NEXUS — HƯỚNG DẪN ⟩\n\n"
        "🎮 *Cách chơi:*\n"
        "Nhận câu đố → Giải đáp → Vượt level\n\n"
        "📋 *Lệnh:*\n"
        "`/start` — Màn hình chào mừng\n"
        "`/level` — Câu đố hiện tại\n"
        "`/hint` — Xem gợi ý (−25% điểm)\n"
        "`/skip` — Bỏ qua (−50 điểm)\n"
        "`/rank` — Bảng xếp hạng\n"
        "`/status` — Trạng thái của bạn\n\n"
        "💰 *Điểm số:*\n"
        "• Tốc độ: ≤30s (+50%) • ≤60s (+20%)\n"
        "• Combo: giải liên tục để nhân điểm\n"
        "• Hint: mỗi hint trừ 25%\n"
        "• Trả lời sai: mỗi lần trừ 10%\n\n"
        "🔐 *Loại câu đố:*\n"
        "• Mật mã học (Caesar, Morse, Base64...)\n"
        "• Logic & Suy luận\n"
        "• Đố mẹo & Phản trực giác\n"
        "• Manh mối đa tầng\n\n"
        "_Nghi ngờ tất cả. Tin tưởng không ai._"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
