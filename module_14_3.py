
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import asyncio

api = "____________________________"
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
kb_calc = InlineKeyboardMarkup()
kb_calc1 = InlineKeyboardMarkup()

bt3 = InlineKeyboardButton(text="Рассчитать", callback_data='calories')
bt4 = InlineKeyboardButton(text="Формула расчёта", callback_data='formulas')

kb_calc.add(bt3)
kb_calc1.add(bt4)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Выберете необходимое:')],
        [
            KeyboardButton(text='Мужчина'),
            KeyboardButton(text='Женщина'),
            KeyboardButton(text='Перейти к покупкам')
        ]
    ],
    resize_keyboard=True
)
inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data='product_buying')],
        [InlineKeyboardButton(text="Product2", callback_data='product_buying')],
        [InlineKeyboardButton(text="Product3", callback_data='product_buying')],
        [InlineKeyboardButton(text="Product4", callback_data='product_buying')],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
    ],
    resize_keyboard=True
)

class UserState(StatesGroup):
    gender = State()
    btt = State()
    age = State()
    growth = State()
    weight = State()
    buy = State()

@dp.message_handler()
async def main_menu(message):
    await message.answer(f"Привет, {message.from_user.username}! Я бот, помогающий следить за здоровьем. Укажите свой пол"
                         f" и мы подберём витамины для вас.",
                         reply_markup=start_menu)
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    gender = message.text.lower()
    if gender not in ["мужчина", "женщина"]:
        await message.answer("Пожалуйста, выберите 'Мужчина' или 'Женщина'.")
        return
    await state.update_data(gender=gender)
    await message.answer("Пока я подбираю для вас витамины, можете потратить время с пользой."
                         "Могу предложить вам расчитать норму калорий:",
                         reply_markup=kb_calc)
    await UserState.btt.set()

@dp.callback_query_handler(text='calories', state=UserState.btt)
async def restart_calculation(call, state):
    # Сброс состояния и переход к вводу возраста
    await UserState.age.set()
    await call.message.answer("Введите свой возраст.")
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите возраст числом.")
        return
    await state.update_data(age=int(message.text))
    await message.answer(f"Принято! Ваш возраст: {message.text}")
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите рост числом.")
        return
    await state.update_data(growth=int(message.text))
    await message.answer(f"Принято! Ваш рост: {message.text}")
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите вес числом.")
        return
    await state.update_data(weight=int(message.text))
    await message.answer(f"Принято! Ваш вес: {message.text}")
    data = await state.get_data()
    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])
    gender = data['gender']

    if gender == 'мужчина':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    else:
        calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories} ккал в день.")
    await message.answer("Посмотеть формулу рассчета:", reply_markup=kb_calc1)
    await UserState.btt.set()

@dp.callback_query_handler(text='formulas', state=UserState.btt)
async def show_formulas(call, state):
    data = await state.get_data()
    gender = data.get('gender')

    # Формулы расчета калорий
    if gender == 'мужчина':
        formula = ("Формула для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5 \n"
                   "Теперь можете перейти к покупкам")
    else:
        formula = ("Формула для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161 \n"
                   "Теперь можете перейти к покупкам")

    await call.message.answer(formula)
    await call.answer()
    await UserState.buy.set()
   # await UserState.btt.set()  # `UserState.btt` для дальнейшего использования кнопок

@dp.message_handler(state=UserState.buy)
async def get_buying_list(message, state):
    data = await state.get_data()
    gender = data.get('gender')

    if gender == 'мужчина':
        for i in range(1, 5):
            # Подготовка данных для мужских витаминов
            name = f"Product{i}"
            description = f"Описание {i}"
            price = i * 100
            img = f"Files/{i}.jpg"
            with open(img, "rb") as img1:
            # Отправка сообщения с изображением и текстом
                await message.answer_photo(
                    photo=img1,
                    caption=f"Название: {name} | Описание: {description} | Цена: {price}"
                    )
        await message.answer("Выберите продукт для покупки:", reply_markup=inline_menu)
        await state.finish()
    else:
        for i in range(1, 5):
            # Подготовка данных для товара
            name = f"Product{i}"
            description = f"Описание {i}"
            price = i * 100
            img = f"Files/{i + 10}.jpg"
            with open(img, "rb") as img1:
                 # Отправка сообщения с изображением и текстом
                await message.answer_photo(
                    photo=img1,
                    caption=f"Название: {name} | Описание: {description} | Цена: {price}"
                    )
        await message.answer("Выберите продукт для покупки:", reply_markup=inline_menu)
        await state.finish()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.callback_query_handler(text="back_to_catalog")
async def back(call):
    await call.message.answer("Вы вернулись вначало", reply_markup=start_menu)
    #await call.message.answer("Что вас интересует?", reply_markup=kb_calc)
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)