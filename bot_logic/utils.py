from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton)


NEW_TASK_BUTTON_TEXT = "Создать задачу"
CONFIRM_COMPANY_BUTTON_TEXT = "Сохранить"
CANCEL_COMPANY_BUTTON_TEXT = "Отменить"

waving_hand = '\U0001F44B'

WELCOME_MESSAGE = f"""Привет! {waving_hand}\n
Здесь вы можете оставлять мне задачи!
Давайте зарегистрируем вас.\n
Введите, пожалуйста, название компании:"""
COMPANY_NAME_CONFIRMATION = """Сохранить за вами компанию *{}*?"""
COMPANY_NAME_SAVED = """Компания *{}* сохранена за вами."""
COMPANY_NAME_CANCEL = """Введите другое название."""
INSTRUCTION_MESSAGE = f"""Итак, как это работает?\n
1. Нажмите на кнопку *{NEW_TASK_BUTTON_TEXT}*\n
2. Отправьте сюда файл с техническим заданием\n
Я свяжусь с вами, если возникнут какие-то вопросы."""
ERROR_MESSAGE = "Попробуйте снова или свяжитесь со мной."
USER_ALREADY_EXISTS = "Я уже вас зарегистрировал!"
NEW_TASK_PROMPT = """Пришлите сюда файл с заданием!"""
SUCCESS_FILE_SAVED = "Файл успешно перенаправлен!"
TASK_INFO = """Компания: {}\n
ID таски: {}\n
Создано: {}"""


def get_default_keyboard(button_text):
    default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    default_keyboard.row(button_text)
    return default_keyboard


def get_company_confirmation_keyboard():
    default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    default_keyboard.row(CONFIRM_COMPANY_BUTTON_TEXT)
    default_keyboard.row(CANCEL_COMPANY_BUTTON_TEXT)
    return default_keyboard


def get_task_keyboard(task_id: str, user_id: str) -> InlineKeyboardMarkup:
    done = InlineKeyboardButton("Сделано!", callback_data=f'button_done_{task_id}_{user_id}')
    task_keyboard = InlineKeyboardMarkup().add(done)
    return task_keyboard
