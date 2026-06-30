import asyncio
from datetime import datetime
from utils_subscription_check import check_subscription

async def send_daily_reminder(bot):
    import aiosqlite
    from database import DB_NAME
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT telegram_id, first_name FROM users")
        users = await cursor.fetchall()
    today_str = datetime.now().strftime("%d.%m.%Y")
    for user in users:
        user_id, first_name = user[0], user[1]
        if await check_subscription(user_id):
            try:
                await bot.send_message(user_id, f"🌙 Доброй ночи, {first_name}!\n\n📅 {today_str}\n\nНе забудьте заполнить смену за сегодня! 📝\nПерейдите в раздел «🧮 Калькулятор» чтобы добавить данные.")
            except:
                pass
        await asyncio.sleep(0.05)

async def scheduler_loop(bot):
    while True:
        now = datetime.now()
        if now.hour == 1 and now.minute == 30:
            await send_daily_reminder(bot)
            await asyncio.sleep(120)
        await asyncio.sleep(30)

async def start_scheduler(bot):
    asyncio.create_task(scheduler_loop(bot))
    print("Планировщик запущен (1:30)")
