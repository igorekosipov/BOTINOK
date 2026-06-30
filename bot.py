import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, ADMIN_IDS, PROXY_URL
from database import init_db, add_user, set_admin
from handlers_start import start_router
from handlers_subscription import sub_router
from handlers_calculator import calc_router
from handlers_statistics import stat_router
from handlers_work_calendar import cal_router
from handlers_support import support_router
from handlers_chat import chat_router
from handlers_admin import admin_router
from scheduler import start_scheduler

async def setup_admins():
    for admin_id in ADMIN_IDS:
        await add_user(admin_id, "admin", "Администратор")
        await set_admin(admin_id, 1)
        print(f"Админ {admin_id} добавлен")

async def main():
    await init_db()
    await setup_admins()
    
    # Настройка прокси
    if PROXY_URL:
        session = AiohttpSession(proxy=PROXY_URL)
        print(f"Прокси: {PROXY_URL}")
    else:
        session = AiohttpSession()
        print("Без прокси")
    
    bot = Bot(token=BOT_TOKEN, session=session, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    dp.include_router(start_router)
    dp.include_router(sub_router)
    dp.include_router(calc_router)
    dp.include_router(stat_router)
    dp.include_router(cal_router)
    dp.include_router(support_router)
    dp.include_router(chat_router)
    dp.include_router(admin_router)
    
    await start_scheduler(bot)
    
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
