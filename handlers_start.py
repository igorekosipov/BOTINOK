from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards_main_menu import get_main_menu
from database import add_user, is_admin

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    await add_user(user.id, user.username, user.first_name)
    admin = await is_admin(user.id)
    text = f"Привет, {user.first_name}! 👋\nЯ бот для учёта доходов за смены.\n\n📌 Возможности:\n- Расчёт зарплаты (часы × ставка)\n- Процент с выручки\n- Чаевые\n- Статистика за день/месяц\n- Календарь смен и выходных\n- Закрытый чат для подписчиков\n\n💳 Подписка: 100₽/мес или 599₽/полгода.\nПодписка оформляется через перевод по реквизитам, после чего вы отправляете чек.\n\n⏰ Каждый день в 1:30 ночи я буду напоминать о необходимости заполнить смену.\n\nИспользуйте меню для навигации."
    await message.answer(text, reply_markup=get_main_menu(admin))
