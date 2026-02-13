"""
puzzles/scoring.py — Tính điểm và kiểm tra đáp án
"""

import re
from typing import Optional


# ─── Điểm ─────────────────────────────────────────────────

TIME_BONUS_THRESHOLDS = [
    (30,  1.5),   # ≤30s  → 150% điểm
    (60,  1.2),   # ≤60s  → 120%
    (120, 1.0),   # ≤120s → 100%
    (300, 0.8),   # ≤300s → 80%
    (None, 0.6),  # >300s → 60%
]

HINT_PENALTY = 0.25    # Mỗi hint trừ 25%
WRONG_PENALTY = 0.1    # Mỗi lần sai trừ 10%
COMBO_BONUS = 0.1      # Mỗi combo thêm 10% (max 50%)


def calculate_score(
    base_score: int,
    time_taken: int,
    hints_used: int,
    wrong_count: int,
    combo: int,
    has_time_bonus: bool = True,
) -> int:
    """
    Tính điểm cuối cùng.

    Công thức:
      final = base * time_mult * hint_mult * wrong_mult * combo_mult
    """
    score = float(base_score)

    # Time multiplier
    if has_time_bonus:
        multiplier = 0.6
        for threshold, mult in TIME_BONUS_THRESHOLDS:
            if threshold is None or time_taken <= threshold:
                multiplier = mult
                break
        score *= multiplier

    # Hint penalty
    hint_mult = max(0.25, 1.0 - hints_used * HINT_PENALTY)
    score *= hint_mult

    # Wrong answer penalty
    wrong_mult = max(0.3, 1.0 - wrong_count * WRONG_PENALTY)
    score *= wrong_mult

    # Combo bonus
    combo_bonus = min(0.5, combo * COMBO_BONUS)
    score *= (1.0 + combo_bonus)

    return max(10, int(score))  # Tối thiểu 10 điểm


# ─── Kiểm tra đáp án ─────────────────────────────────────

def normalize(text: str) -> str:
    """Chuẩn hoá đáp án để so sánh."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    # Bỏ dấu câu cuối
    text = text.rstrip('!?.,;:')
    return text


def check_answer(user_input: str, puzzle: dict) -> bool:
    """
    Kiểm tra xem đáp án người dùng có đúng không.
    Chấp nhận answer chính và alt_answers.
    """
    user_norm = normalize(user_input)
    correct_norm = normalize(puzzle["answer"])

    if user_norm == correct_norm:
        return True

    for alt in puzzle.get("alt_answers", []):
        if user_norm == normalize(alt):
            return True

    return False


# ─── Format điểm ─────────────────────────────────────────

def format_score_breakdown(
    base_score: int,
    time_taken: int,
    hints_used: int,
    wrong_count: int,
    combo: int,
    final_score: int,
) -> str:
    """Trả về chuỗi breakdown điểm số."""
    lines = [f"💰 *Điểm gốc:* {base_score}"]

    if hints_used > 0:
        lines.append(f"💡 *Hint penalty:* -{hints_used * 25}%")
    if wrong_count > 0:
        lines.append(f"❌ *Wrong penalty:* -{wrong_count * 10}%")
    if combo > 1:
        lines.append(f"🔥 *Combo x{combo}:* +{min(50, (combo-1) * 10)}%")
    if time_taken <= 30:
        lines.append(f"⚡ *Speed bonus:* +50%")
    elif time_taken <= 60:
        lines.append(f"⚡ *Speed bonus:* +20%")

    lines.append(f"\n✨ *Tổng điểm: {final_score}*")
    return "\n".join(lines)
