"""
╔══════════════════════════════════════════════╗
║  CIPHER PROTOCOL — TELEGRAM CRYPTO BOT       ║
║  Bối cảnh: Tổ chức CIPHER gửi mật thư       ║
╚══════════════════════════════════════════════╝

Entry point. Khởi chạy bot và đăng ký handlers.
"""

import logging
import os
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters
)
from handlers.commands import (
    start_handler, level_handler, hint_handler,
    skip_handler, rank_handler, status_handler, help_handler
)
from handlers.messages import message_handler
from handlers.callbacks import callback_handler
from database.db import init_db
from utils.scheduler import setup_scheduler

# ─── Logging ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Token ────────────────────────────────────────────────
# Windows (CMD)
BOT_TOKEN="8555291430:AAEUeVaz1Y1y8cksDol0WEm9_mhGo-HD-qY"

# Mac / Linux
TELEGRAM_BOT_TOKEN="8555291430:AAEUeVaz1Y1y8cksDol0WEm9_mhGo-HD-qY"


def main() -> None:
    """Khởi động CIPHER PROTOCOL Bot."""
    # Khởi tạo database
    init_db()
    logger.info("✅ Database initialized")

    # Tạo application
    app = Application.builder().token(BOT_TOKEN).build()

    # ─── Command Handlers ─────────────────────────────────
    app.add_handler(CommandHandler("start",  start_handler))
    app.add_handler(CommandHandler("level",  level_handler))
    app.add_handler(CommandHandler("hint",   hint_handler))
    app.add_handler(CommandHandler("skip",   skip_handler))
    app.add_handler(CommandHandler("rank",   rank_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("help",   help_handler))

    # ─── Callback Queries (Inline Buttons) ────────────────
    app.add_handler(CallbackQueryHandler(callback_handler))

    # ─── Message Handler ──────────────────────────────────
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler
    ))

    # ─── Scheduler (Daily puzzle, events) ─────────────────
    setup_scheduler(app)

    logger.info("🔐 CIPHER PROTOCOL Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
