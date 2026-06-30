from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from datetime import datetime
from database import get_user

WHITELIST_COMMANDS = ["start", "help", "support"]
WHITELIST_MESSAGES = ["💳 Моя подписка", "🆘 Поддержка", "🔧 Админ-панель"]
WHITELIST_CALLBACK_PREFIXES = ["sub_", "pay_", "admin_", "cal_", "stat_", "st1_", "st2_", "day_", "list_days", "clear_days", "edit_"]

class SubscriptionCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Any:
        user = None
        if isinstance(event, Message):
            user = event.from_user
            if event.text and event.text.startswith('/'):
                if event.text.split()[0][1:] in WHITELIST_COMMANDS:
                    return await handler(event, data)
            if event.text in WHITELIST_MESSAGES:
                return await handler(event, data)
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            if any(event.data.startswith(prefix) for prefix in WHITELIST_CALLBACK_PREFIXES):
                return await handler(event, data)
        if user:
            db_user = await get_user(user.id)
            if db_user and db_user["subscription_end"]:
                try:
                    if datetime.fromisoformat(db_user["subscription_end"]) > datetime.now():
                        return await handler(event, data)
                except:
                    pass
            if isinstance(event, Message):
                await event.answer("⚠️ У вас нет активной подписки. Перейдите в раздел «💳 Моя подписка» для оплаты.")
            elif isinstance(event, CallbackQuery):
                await event.answer("Нет подписки", show_alert=True)
            return
        return await handler(event, data)
