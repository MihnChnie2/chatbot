"""
handlers/messages.py — Xử lý tin nhắn thường (đáp án người dùng gửi)
"""

import logging
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.db import (
    get_player, get_session, end_session, update_player,
    update_session, record_solve, start_session
)
from puzzles.puzzle_data import PUZZLE_BY_ID, PUZZLE_BY_LEVEL, MAX_LEVEL
from puzzles.scoring import calculate_score, check_answer, format_score_breakdown
from utils.helpers import (
    game_keyboard, next_level_keyboard, completion_keyboard,
    random_nexus, get_timestamp, format_time
)

logger = logging.getLogger(__name__)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Nhận và kiểm tra đáp án từ người dùng."""
    user = update.effective_user
    text = update.message.text.strip()

    # Bỏ qua lệnh
    if text.startswith("/"):
        return

    player = get_player(user.id)
    if not player:
        await update.message.reply_text(
            "Bạn chưa có tài khoản. Gõ /start để bắt đầu."
        )
        return

    session = get_session(user.id)
    if not session:
        await update.message.reply_text(
            "⟨ NEXUS ⟩ Không có giao thức nào đang chạy.\n"
            "Gõ /level để nhận câu đố.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    puzzle = PUZZLE_BY_ID.get(session["puzzle_id"])
    if not puzzle:
        await update.message.reply_text("⚠️ Lỗi hệ thống: puzzle not found.")
        return

    # ─── Kiểm tra đáp án ──────────────────────────────────
    is_correct = check_answer(text, puzzle)

    if is_correct:
        await _handle_correct(update, player, session, puzzle)
    else:
        await _handle_wrong(update, session, puzzle)


async def _handle_correct(update, player, session, puzzle) -> None:
    """Xử lý khi đáp án đúng."""
    user = update.effective_user

    # Tính thời gian
    try:
        started = datetime.fromisoformat(
            session["started_at"].replace("Z", "+00:00")
        )
    except ValueError:
        started = datetime.strptime(
            session["started_at"], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone.utc)

    time_taken = max(1, get_timestamp() - int(started.timestamp()))
    hints_used = session["hints_used"]
    wrong_count = session["wrong_count"]
    current_combo = player["combo"] + 1

    # Tính điểm
    final_score = calculate_score(
        base_score=puzzle["base_score"],
        time_taken=time_taken,
        hints_used=hints_used,
        wrong_count=wrong_count,
        combo=current_combo,
        has_time_bonus=puzzle.get("time_bonus", True)
    )

    # Cập nhật max combo
    max_combo = max(player["max_combo"], current_combo)

    # Lưu database
    record_solve(
        user_id=user.id,
        puzzle_id=puzzle["id"],
        level=session["level"],
        score=final_score,
        time_taken=time_taken,
        hints_used=hints_used
    )

    update_player(
        user_id=user.id,
        total_score=player["total_score"] + final_score,
        current_level=player["current_level"] + 1,
        hints_used=player["hints_used"] + hints_used,
        combo=current_combo,
        max_combo=max_combo,
        wrong_answers=player["wrong_answers"] + wrong_count
    )

    end_session(user.id)

    next_level = player["current_level"] + 1
    is_final = next_level > MAX_LEVEL

    # ─── Response ─────────────────────────────────────────
    combo_text = ""
    if current_combo >= 3:
        combo_text = f"\n🔥 *COMBO x{current_combo}!* Điểm nhân thêm!"
    elif current_combo == 2:
        combo_text = "\n🔥 *COMBO x2!*"

    score_breakdown = format_score_breakdown(
        puzzle["base_score"], time_taken, hints_used,
        wrong_count, current_combo, final_score
    )

    text = (
        f"{random_nexus('correct')}\n\n"
        f"✅ *ĐÚNG RỒI!*{combo_text}\n\n"
        f"*Đáp án:* `{puzzle['answer'].upper()}`\n\n"
        f"📖 *Giải thích:*\n{puzzle['explanation']}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{score_breakdown}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏱️ Thời gian: {format_time(time_taken)}"
    )

    if is_final:
        keyboard = completion_keyboard()
        text += "\n\n🎊 *Bạn đã hoàn thành tất cả các level!*"
    else:
        keyboard = next_level_keyboard(next_level)
        text += f"\n\n➡️ Level tiếp theo: *{next_level}/{MAX_LEVEL}*"

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )


async def _handle_wrong(update, session, puzzle) -> None:
    """Xử lý khi đáp án sai."""
    user = update.effective_user

    new_wrong = session["wrong_count"] + 1
    update_session(user.id, wrong_count=new_wrong)
    update_player(user.id, wrong_answers=0)  # sẽ cộng khi giải xong

    text = (
        f"{random_nexus('wrong')}\n\n"
        f"❌ *Sai rồi.* (Lần {new_wrong})\n"
        f"_Điểm sẽ bị trừ 10% khi giải xong._\n\n"
    )

    # Sau 3 lần sai, gợi ý nhỏ
    if new_wrong >= 3:
        hints = puzzle.get("hints", [])
        if hints:
            text += f"💬 *Gợi ý tự động:* {hints[0]}\n\n"
            text += "_Đây là lần cuối cùng tôi nhân nhượng._"

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=game_keyboard(session["level"], session["hints_used"])
    )
