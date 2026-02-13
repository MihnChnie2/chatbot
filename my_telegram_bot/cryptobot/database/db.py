"""
database/db.py — SQLite State Management
Lưu trạng thái người chơi, điểm số, lịch sử giải đố
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "cipher_protocol.db")


def get_conn() -> sqlite3.Connection:
    """Trả về connection SQLite với row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Tạo bảng nếu chưa tồn tại."""
    with get_conn() as conn:
        conn.executescript("""
        -- Bảng người chơi
        CREATE TABLE IF NOT EXISTS players (
            user_id       INTEGER PRIMARY KEY,
            username      TEXT,
            full_name     TEXT,
            current_level INTEGER DEFAULT 1,
            total_score   INTEGER DEFAULT 0,
            hints_used    INTEGER DEFAULT 0,
            skips_used    INTEGER DEFAULT 0,
            wrong_answers INTEGER DEFAULT 0,
            combo         INTEGER DEFAULT 0,
            max_combo     INTEGER DEFAULT 0,
            joined_at     TEXT DEFAULT (datetime('now')),
            last_active   TEXT DEFAULT (datetime('now'))
        );

        -- Bảng lịch sử giải đố
        CREATE TABLE IF NOT EXISTS solve_history (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER,
            puzzle_id     TEXT,
            level         INTEGER,
            score_earned  INTEGER,
            time_taken    INTEGER,       -- giây
            hints_used    INTEGER DEFAULT 0,
            solved_at     TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES players(user_id)
        );

        -- Bảng active session (câu đố hiện tại)
        CREATE TABLE IF NOT EXISTS active_sessions (
            user_id       INTEGER PRIMARY KEY,
            puzzle_id     TEXT,
            level         INTEGER,
            started_at    TEXT DEFAULT (datetime('now')),
            hints_used    INTEGER DEFAULT 0,
            wrong_count   INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES players(user_id)
        );

        -- Bảng puzzle daily (câu đố ngày)
        CREATE TABLE IF NOT EXISTS daily_puzzle (
            date          TEXT PRIMARY KEY,
            puzzle_id     TEXT
        );

        -- Bảng giải daily puzzle
        CREATE TABLE IF NOT EXISTS daily_solves (
            user_id       INTEGER,
            date          TEXT,
            score         INTEGER,
            PRIMARY KEY (user_id, date),
            FOREIGN KEY (user_id) REFERENCES players(user_id)
        );
        """)


# ─── Player Operations ────────────────────────────────────

def get_or_create_player(user_id: int, username: str, full_name: str) -> sqlite3.Row:
    """Lấy hoặc tạo player mới."""
    with get_conn() as conn:
        player = conn.execute(
            "SELECT * FROM players WHERE user_id = ?", (user_id,)
        ).fetchone()

        if not player:
            conn.execute(
                """INSERT INTO players (user_id, username, full_name)
                   VALUES (?, ?, ?)""",
                (user_id, username, full_name)
            )
            conn.commit()
            player = conn.execute(
                "SELECT * FROM players WHERE user_id = ?", (user_id,)
            ).fetchone()

        return player


def update_player(user_id: int, **kwargs) -> None:
    """Cập nhật field của player."""
    if not kwargs:
        return
    fields = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [user_id]
    with get_conn() as conn:
        conn.execute(
            f"UPDATE players SET {fields}, last_active = datetime('now') WHERE user_id = ?",
            values
        )
        conn.commit()


def get_player(user_id: int) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM players WHERE user_id = ?", (user_id,)
        ).fetchone()


# ─── Session Operations ───────────────────────────────────

def start_session(user_id: int, puzzle_id: str, level: int) -> None:
    """Bắt đầu session câu đố mới."""
    with get_conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO active_sessions
               (user_id, puzzle_id, level, started_at, hints_used, wrong_count)
               VALUES (?, ?, ?, datetime('now'), 0, 0)""",
            (user_id, puzzle_id, level)
        )
        conn.commit()


def get_session(user_id: int) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM active_sessions WHERE user_id = ?", (user_id,)
        ).fetchone()


def update_session(user_id: int, **kwargs) -> None:
    if not kwargs:
        return
    fields = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [user_id]
    with get_conn() as conn:
        conn.execute(
            f"UPDATE active_sessions SET {fields} WHERE user_id = ?", values
        )
        conn.commit()


def end_session(user_id: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM active_sessions WHERE user_id = ?", (user_id,)
        )
        conn.commit()


# ─── Score & History ──────────────────────────────────────

def record_solve(user_id: int, puzzle_id: str, level: int,
                 score: int, time_taken: int, hints_used: int) -> None:
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO solve_history
               (user_id, puzzle_id, level, score_earned, time_taken, hints_used)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, puzzle_id, level, score, time_taken, hints_used)
        )
        conn.commit()


def get_leaderboard(limit: int = 10) -> List:
    with get_conn() as conn:
        return conn.execute(
            """SELECT user_id, username, full_name, total_score,
                      current_level, max_combo
               FROM players
               ORDER BY total_score DESC
               LIMIT ?""",
            (limit,)
        ).fetchall()


def has_solved_puzzle(user_id: int, puzzle_id: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM solve_history WHERE user_id = ? AND puzzle_id = ?",
            (user_id, puzzle_id)
        ).fetchone()
        return row is not None


# ─── Daily Puzzle ─────────────────────────────────────────

def set_daily_puzzle(date: str, puzzle_id: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO daily_puzzle (date, puzzle_id) VALUES (?, ?)",
            (date, puzzle_id)
        )
        conn.commit()


def get_daily_puzzle(date: str) -> Optional[str]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT puzzle_id FROM daily_puzzle WHERE date = ?", (date,)
        ).fetchone()
        return row["puzzle_id"] if row else None


def record_daily_solve(user_id: int, date: str, score: int) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO daily_solves (user_id, date, score) VALUES (?, ?, ?)",
            (user_id, date, score)
        )
        conn.commit()


def has_solved_daily(user_id: int, date: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM daily_solves WHERE user_id = ? AND date = ?",
            (user_id, date)
        ).fetchone()
        return row is not None
