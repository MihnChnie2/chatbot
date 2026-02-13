"""
utils/scheduler.py — Lên lịch sự kiện tự động
- Daily puzzle reset
- Gửi thông báo cho người chơi active
"""

import logging
import random
from datetime import datetime, timezone, time as dt_time

from puzzles.puzzle_data import DAILY_POOL
from database.db import set_daily_puzzle, get_daily_puzzle

logger = logging.getLogger(__name__)


def pick_daily_puzzle(date: str) -> str:
    """Chọn câu đố ngày dựa trên ngày (deterministic)."""
    existing = get_daily_puzzle(date)
    if existing:
        return existing

    # Dùng date làm seed để consistent trong ngày
    day_num = int(date.replace("-", "")) % len(DAILY_POOL)
    puzzle = DAILY_POOL[day_num]
    set_daily_puzzle(date, puzzle["id"])
    logger.info(f"Daily puzzle set for {date}: {puzzle['id']}")
    return puzzle["id"]


def setup_scheduler(app) -> None:
    """
    Khởi tạo job scheduler.
    
    Dùng JobQueue của python-telegram-bot để:
    - Reset daily puzzle lúc 00:00 UTC
    - Gửi reminder cho người chơi chưa hoàn thành
    """
    if app.job_queue is None:
        logger.warning("JobQueue không khả dụng. Cài: pip install python-telegram-bot[job-queue]")
        return

    # Daily puzzle reset lúc 00:00 UTC
    app.job_queue.run_daily(
        _daily_puzzle_reset,
        time=dt_time(0, 0, 0, tzinfo=timezone.utc),
        name="daily_puzzle_reset"
    )

    # Chạy ngay khi khởi động để set puzzle hôm nay
    app.job_queue.run_once(
        _daily_puzzle_reset,
        when=0,
        name="daily_puzzle_init"
    )

    logger.info("✅ Scheduler setup complete")


async def _daily_puzzle_reset(context) -> None:
    """Job: reset daily puzzle."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    puzzle_id = pick_daily_puzzle(today)
    logger.info(f"🌅 Daily puzzle for {today}: {puzzle_id}")
