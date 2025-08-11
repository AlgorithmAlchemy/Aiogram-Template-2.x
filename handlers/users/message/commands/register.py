"""
Обработчик команды /register с использованием FSM
"""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import config
from models.user import User
from states.user.registration import RegistrationStates
from keyboards.inline.keyboards import MainKeyboards

from loader import dp


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
                'language_code': message.from_user.language_code
            }
        )
        
        if not created:
            await message.answer(
                "Вы уже зарегистрированы! Используйте /profile для просмотра профиля."
            )
            return
        
        # Начинаем процесс регистрации
        await state.set_state(RegistrationStates.waiting_for_name)
        
        await message.answer(
            "Добро пожаловать! Давайте завершим регистрацию.\n\n"
            "Как вас зовут? (введите ваше полное имя)"
        )
    
    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_name)
    async def process_name(message: types.Message, state: FSMContext):
        """Обработка имени пользователя"""
        if len(message.text) < 2:
            await message.answer("Имя должно содержать минимум 2 символа. Попробуйте еще раз.")
            return
        
        # Сохраняем имя
        await state.update_data(name=message.text)
        
        # Переходим к следующему шагу
        await state.set_state(RegistrationStates.waiting_for_age)
        
        await message.answer(
            f"Отлично, {message.text}! Теперь укажите ваш возраст:"
        )
    
    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_age)
    async def process_age(message: types.Message, state: FSMContext):
        """Обработка возраста пользователя"""
        try:
            age = int(message.text)
            if age < 13 or age > 120:
                await message.answer("Возраст должен быть от 13 до 120 лет. Попробуйте еще раз.")
                return
        except ValueError:
            await message.answer("Пожалуйста, введите корректный возраст (число).")
            return
        
        # Сохраняем возраст
        await state.update_data(age=age)
        
        # Переходим к следующему шагу
        await state.set_state(RegistrationStates.waiting_for_city)
        
        await message.answer(
            "Хорошо! Теперь укажите ваш город:"
        )
    
    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_city)
    async def process_city(message: types.Message, state: FSMContext):
        """Обработка города пользователя"""
        if len(message.text) < 2:
            await message.answer("Название города должно содержать минимум 2 символа. Попробуйте еще раз.")
            return
        
        # Сохраняем город
        await state.update_data(city=message.text)
        
        # Переходим к финальному шагу
        await state.set_state(RegistrationStates.waiting_for_confirmation)
        
        # Получаем все данные
        data = await state.get_data()
        
        confirmation_text = f"""
<b>📝 Подтвердите данные регистрации:</b>

<b>Имя:</b> {data['name']}
<b>Возраст:</b> {data['age']} лет
<b>Город:</b> {data['city']}

Все верно? Отправьте "да" для подтверждения или "нет" для повторного ввода.
"""
        
        await message.answer(confirmation_text, parse_mode='HTML')
    
    @staticmethod
    @dp.message_handler(state=RegistrationStates.waiting_for_confirmation)
    async def process_confirmation(message: types.Message, state: FSMContext):
        """Обработка подтверждения регистрации"""
        if message.text.lower() in ['да', 'yes', 'y', 'д']:
            # Получаем данные
            data = await state.get_data()
            
            # Обновляем пользователя в базе данных
            user = User.get(User.user_id == message.from_user.id)
            # Здесь можно добавить дополнительные поля в модель User
            # user.full_name = data['name']
            # user.age = data['age']
            # user.city = data['city']
            user.save()
            
            # Завершаем регистрацию
            await state.finish()
            
            welcome_text = f"""
<b>🎉 Регистрация завершена!</b>

Добро пожаловать, {data['name']}!

Теперь вы можете использовать все возможности бота.
Используйте /help для получения справки.
"""
            
            keyboard = MainKeyboards.get_main_menu()
            await message.answer(welcome_text, parse_mode='HTML', reply_markup=keyboard)
            
        elif message.text.lower() in ['нет', 'no', 'n', 'н']:
            # Начинаем заново
            await state.set_state(RegistrationStates.waiting_for_name)
            await message.answer(
                "Хорошо, давайте начнем заново.\n\nКак вас зовут?"
            )
        else:
            await message.answer(
                "Пожалуйста, ответьте 'да' для подтверждения или 'нет' для повторного ввода."
            )
    
    @staticmethod
    @dp.message_handler(commands=['cancel'], state='*')
    async def cancel_registration(message: types.Message, state: FSMContext):
        """Отмена регистрации"""
        current_state = await state.get_state()
        if current_state is None:
            await message.answer("Нечего отменять.")
            return
        
        await state.finish()
        await message.answer(
            "Регистрация отменена. Вы можете начать заново командой /register"
        )
