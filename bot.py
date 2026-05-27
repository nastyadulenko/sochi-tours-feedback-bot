import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import database as db
from handlers import router
from config import BOT_TOKEN, ADMIN_ID

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключение обработчиков
dp.include_router(router)

# Настройки webhook
WEBHOOK_HOST = os.environ.get('RENDER_EXTERNAL_URL')  # Render сам дает этот URL
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def on_startup():
    """Действия при запуске бота"""
    logger.info("🚀 Запуск бота на Render.com...")
    
    # Инициализация базы данных
    db.init_db()
    logger.info("✅ База данных готова")
    
    # Установка webhook
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"✅ Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("⏹️ Бот останавливается...")
    await bot.delete_webhook()
    await bot.session.close()

def main():
    """Запуск webhook сервера"""
    app = web.Application()
    
    # Настройка webhook обработчика
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Настройка приложения
    setup_application(app, dp, bot=bot)
    
    # Добавление обработчиков старта и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    # Запуск сервера
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🌐 Запуск webhook сервера на порту {port}")
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
