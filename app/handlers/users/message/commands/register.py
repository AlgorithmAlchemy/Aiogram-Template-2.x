"""
Обработчик команды /register с использованием FSM
"""
from aiogram import types
from aiogram.dispatcher import FSMContext

from app.keyboards.inline.keyboards import MainKeyboards
from app.loader import dp
from app.models import User, UserSettings, UserStats
from app.states.user.registration import RegistrationStates


class RegisterCommand:
    """Команда регистрации пользователя"""

    @staticmethod
    @dp.message_handler(commands=['register'])
    async def handle(message: types.Message, state: FSMContext):
        """Обработчик команды /register"""
        user_id = message.from_user.id

        # Проверяем, не зарегистрирован ли уже пользователь
        user, created = User.get_or_create(
            user_id=user_id,
            defaults={
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'username': message.from_user.username,
                'language_code': message.from_user.language_code,
                'is_bot': message.from_user.is_bot
            }
        )

        if not created:
            await message.answer(
                "Вы уже зарегистрированы! Используйте /profile для просмотра профиля."
            )
            return

        # Создаем настройки и статистику для нового пользователя
        UserSettings.create(user=user)
        UserStats.create(user=user)

        # Начинаем процесс регистрации
        await state.set_state(RegistrationStates.waiting_for_name)

        await message.answer(
            "Добро пожаловать! Давайте завершим регистрацию.\n\n"
            "Как вас зовут? (введите ваше полное имя)"
        )

    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_name)
    async def process_name(message: types.Message, state: FSMContext):
        """Обработка введенного имени"""
        await state.update_data(name=message.text)
        await state.set_state(RegistrationStates.waiting_for_age)

        await message.answer(
            f"Отлично, {message.text}! Теперь укажите ваш возраст:"
        )

    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_age)
    async def process_age(message: types.Message, state: FSMContext):
        """Обработка введенного возраста"""
        try:
            age = int(message.text)
            if age < 1 or age > 120:
                await message.answer("Пожалуйста, введите корректный возраст (1-120):")
                return

            await state.update_data(age=age)
            await state.set_state(RegistrationStates.waiting_for_city)

            await message.answer(
                f"Возраст: {age} лет. Теперь укажите ваш город:"
            )
        except ValueError:
            await message.answer("Пожалуйста, введите возраст числом:")

    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_city)
    async def process_city(message: types.Message, state: FSMContext):
        """Обработка введенного города"""
        await state.update_data(city=message.text)

        # Получаем все данные
        data = await state.get_data()

        # Обновляем пользователя в БД
        user_id = message.from_user.id
        user = User.get(User.user_id == user_id)

        # Здесь можно добавить дополнительные поля в модель User
        # user.age = data.get('age')
        # user.city = data.get('city')
        # user.save()

        # Завершаем регистрацию
        await state.finish()

        await message.answer(
            f"""
<b>✅ Регистрация завершена!</b>

<b>Ваши данные:</b>
• Имя: {data.get('name')}
• Возраст: {data.get('age')} лет
• Город: {data.get('city')}

Добро пожаловать в бота! Используйте /help для получения справки.
""",
            parse_mode=types.ParseMode.HTML,
            reply_markup=MainKeyboards.get_main_keyboard()
        )


# Регистрация обработчиков состояний
@dp.message_handler(state=RegistrationStates.waiting_for_name)
async def name_handler(message: types.Message, state: FSMContext):
    await RegisterCommand.process_name(message, state)


@dp.message_handler(state=RegistrationStates.waiting_for_age)
async def age_handler(message: types.Message, state: FSMContext):
    await RegisterCommand.process_age(message, state)


@dp.message_handler(state=RegistrationStates.waiting_for_city)
async def city_handler(message: types.Message, state: FSMContext):
    await RegisterCommand.process_city(message, state)
