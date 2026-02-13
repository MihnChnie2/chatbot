"""
handlers/callbacks.py — Xử lý callback queries (nút bấm inline)
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.db import (
    get_player, get_session, end_session, update_player,
    start_session, get_leaderboard
)
from puzzles.puzzle_data import PUZZLE_BY_LEVEL, PUZZLE_BY_ID, MAX_LEVEL
from utils.helpers import (
    main_menu_keyboard, game_keyboard, format_rank_emoji,
    level_progress_bar, random_nexus
)

logger = logging.getLogger(__name__)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router cho tất cả callback queries."""
    query = update.callback_query
    await query.answer()  # Tắt loading spinner

    data = query.data
    user = update.effective_user

    action_map = {
        "action:play":       _cb_play,
        "action:hint":       _cb_hint,
        "action:skip":       _cb_skip,
        "action:rank":       _cb_rank,
        "action:status":     _cb_status,
        "action:help":       _cb_help,
        "action:menu":       _cb_menu,
        "action:next_level": _cb_next_level,
        "action:restart":    _cb_restart,
        "action:cancel":     _cb_cancel,
        "confirm:skip":      _cb_confirm_skip,
    }

    handler = action_map.get(data)
    if handler:
        await handler(query, user, context)
    else:
        await query.message.reply_text("⚠️ Hành động không xác định.")


# ─── Callback Actions ─────────────────────────────────────

async def _cb_play(query, user, context) -> None:
    """Bắt đầu / tiếp tục chơi."""
    from handlers.commands import level_handler
    # Tạo fake update để gọi level_handler
    player = get_player(user.id)
    if not player:
        await query.message.reply_text("Gõ /start trước.")
        return

    level = player["current_level"]
    if level > MAX_LEVEL:
        await query.message.reply_text(
            "🎊 Bạn đã hoàn thành tất cả level!\n"
            "Gõ /start để xem màn hoàn thành."
        )
        return

    puzzle = PUZZLE_BY_LEVEL.get(level)
    if not puzzle:
        await query.message.reply_text("⚠️ Không tìm thấy câu đố.")
        return

    session = get_session(user.id)
    if not session or session["puzzle_id"] != puzzle["id"]:
        start_session(user.id, puzzle["id"], level)

    session = get_session(user.id)
    hints_used = session["hints_used"] if session else 0

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *LEVEL {level}/{MAX_LEVEL}* — {puzzle['category']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{puzzle['lore']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{puzzle['question']}\n\n"
        f"📝 _Nhập đáp án ngay trong chat_"
    )

    await query.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=game_keyboard(level, hints_used)
    )


async def _cb_hint(query, user, context) -> None:
    """Gợi ý qua callback."""
    session = get_session(user.id)
    if not session:
        await query.message.reply_text("Không có câu đố nào đang chạy.")
        return

    puzzle = PUZZLE_BY_ID.get(session["puzzle_id"])
    if not puzzle:
        return

    hints = puzzle.get("hints", [])
    hints_used = session["hints_used"]

    if hints_used >= len(hints):
        await query.answer("Bạn đã dùng hết gợi ý!", show_alert=True)
        return

    hint = hints[hints_used]
    new_hints_used = hints_used + 1

    from database.db import update_session
    update_session(user.id, hints_used=new_hints_used)

    text = (
        f"{random_nexus('hint')}\n\n"
        f"💡 *Gợi ý #{new_hints_used}/{len(hints)}:*\n\n"
        f"{hint}\n\n"
        f"_⚠️ Điểm bị trừ 25%._"
    )

    await query.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=game_keyboard(session["level"], new_hints_used)
    )


async def _cb_skip(query, user, context) -> None:
    """Xác nhận bỏ qua."""
    from utils.helpers import confirm_skip_keyboard
    await query.message.reply_text(
        "⟨ NEXUS ⟩\n\n"
        "Bỏ qua? *-50 điểm* và mất combo.\n"
        "_Bạn có chắc?_",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=confirm_skip_keyboard()
    )


async def _cb_confirm_skip(query, user, context) -> None:
    """Thực hiện bỏ qua."""
    session = get_session(user.id)
    if not session:
        await query.message.reply_text("Không có gì để bỏ qua.")
        return

    player = get_player(user.id)
    new_score = max(0, player["total_score"] - 50)
    new_level = player["current_level"] + 1

    update_player(
        user.id,
        total_score=new_score,
        current_level=new_level,
        skips_used=player["skips_used"] + 1,
        combo=0  # Reset combo
    )
    end_session(user.id)

    puzzle = PUZZLE_BY_ID.get(session["puzzle_id"])
    puzzle_name = puzzle.get("id", "?") if puzzle else "?"

    text = (
        "⟨ NEXUS ⟩ Hồ sơ của bạn đã được cập nhật.\n\n"
        f"⏭️ *Bỏ qua:* {puzzle_name}\n"
        f"💸 *Trừ điểm:* -50\n"
        f"🔥 *Combo:* Reset về 0\n\n"
        f"Gõ /level để tiếp tục."
    )

    await query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def _cb_rank(query, user, context) -> None:
    """Hiển thị leaderboard."""
    leaders = get_leaderboard(10)
    if not leaders:
        await query.message.reply_text("Bảng xếp hạng trống.")
        return

    lines = ["🏆 *BẢNG XẾP HẠNG*\n"]
    for i, p in enumerate(leaders, 1):
        name = p["full_name"] or p["username"] or f"Agent #{p['user_id'] % 9999}"
        emoji = format_rank_emoji(i)
        lines.append(f"{emoji} *{name}* — {p['total_score']:,} pts (Lv.{p['current_level']})")

    await query.message.reply_text(
        "\n".join(lines),
        parse_mode=ParseMode.MARKDOWN
    )


async def _cb_status(query, user, context) -> None:
    """Hiển thị trạng thái."""
    player = get_player(user.id)
    if not player:
        await query.message.reply_text("Gõ /start để tạo tài khoản.")
        return

    level = player["current_level"]
    progress = level_progress_bar(min(level - 1, MAX_LEVEL), MAX_LEVEL)

    text = (
        "⟨ NEXUS — HỒ SƠ ⟩\n\n"
        f"🎯 Level: {level}/{MAX_LEVEL}\n"
        f"📈 {progress}\n"
        f"💰 Điểm: {player['total_score']:,}\n"
        f"🔥 Combo: {player['combo']} (max: {player['max_combo']})\n"
        f"💡 Gợi ý: {player['hints_used']}"
    )

    await query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def _cb_help(query, user, context) -> None:
    """Hướng dẫn nhanh."""
    text = (
        "❓ *HƯỚNG DẪN NHANH*\n\n"
        "• Đọc câu đố → nhập đáp án trong chat\n"
        "• /hint — gợi ý (trừ 25% điểm)\n"
        "• /skip — bỏ qua (trừ 50 điểm)\n"
        "• Giải nhanh = điểm cao hơn\n"
        "• Giải liên tục = combo bonus\n\n"
        "_Gõ /help để xem hướng dẫn đầy đủ._"
    )
    await query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def _cb_menu(query, user, context) -> None:
    """Trở về menu chính."""
    player = get_player(user.id)
    level = player["current_level"] if player else 1
    progress = level_progress_bar(min(level - 1, MAX_LEVEL), MAX_LEVEL)

    text = (
        "⟨ NEXUS — MENU CHÍNH ⟩\n\n"
        f"Level: {level}/{MAX_LEVEL} — {progress}\n"
        f"Điểm: {player['total_score']:,}" if player else "⟨ NEXUS — MENU CHÍNH ⟩"
    )

    await query.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )


async def _cb_next_level(query, user, context) -> None:
    """Chuyển sang level tiếp theo."""
    await _cb_play(query, user, context)


async def _cb_restart(query, user, context) -> None:
    """Reset game về đầu."""
    player = get_player(user.id)
    if not player:
        return

    # Reset level về 1 nhưng giữ điểm
    update_player(user.id, current_level=1, combo=0)
    end_session(user.id)

    await query.message.reply_text(
        "⟨ NEXUS ⟩\n\n"
        "Giao thức đã được reset.\n"
        "Điểm số của bạn được giữ lại.\n\n"
        "Gõ /level để bắt đầu lại từ đầu.",
        parse_mode=ParseMode.MARKDOWN
    )


async def _cb_cancel(query, user, context) -> None:
    """Huỷ hành động."""
    await query.message.reply_text(
        "⟨ NEXUS ⟩ Hành động đã bị huỷ.",
        parse_mode=ParseMode.MARKDOWN
    )
