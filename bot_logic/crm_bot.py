import os
import logging
import traceback
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

import bot_logic.utils as utils
from db.connection_pool import get_connection
import db.database as db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.environ['TOKEN']
ADMIN_ID = int(os.environ['ADMIN_ID'])

crm_bot = Bot(token=TOKEN)
dp = Dispatcher(crm_bot, storage=MemoryStorage())

class NewUser(StatesGroup):
    GetCompanyName = State()
    SaveOrCancel = State()
    WelcomeInstructions = State()

class NewTask(StatesGroup):
    GetTask = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    with get_connection() as connection:
        if db.check_user_exists(connection, user_id):
            await message.answer(utils.USER_ALREADY_EXISTS,
                                 reply_markup=utils.get_default_keyboard(utils.NEW_TASK_BUTTON_TEXT))
            return
    await message.answer(utils.WELCOME_MESSAGE,
                         parse_mode=types.ParseMode.MARKDOWN)

    await NewUser.GetCompanyName.set()


@dp.message_handler(state=NewUser.GetCompanyName)
async def get_company_name(message: types.Message, state: FSMContext):
    company_name = message.text
    user_id = message.from_user.id
    async with state.proxy() as company:
        company['name'] = company_name
        company['user_id'] = user_id
    await message.answer(utils.COMPANY_NAME_CONFIRMATION.format(company_name),
                         reply_markup=utils.get_company_confirmation_keyboard(),
                         parse_mode=types.ParseMode.MARKDOWN)
    await NewUser.SaveOrCancel.set()


@dp.message_handler(lambda message: message.text == utils.CONFIRM_COMPANY_BUTTON_TEXT,
                    state=NewUser.SaveOrCancel)
async def save_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as company:
        company_name = company['name']
        user_id = company['user_id']
        try:
            with get_connection() as connection:
                db.add_user(connection, user_id, company_name)
            await message.answer(utils.COMPANY_NAME_SAVED.format(company_name),
                                 parse_mode=types.ParseMode.MARKDOWN)
            await message.answer(utils.INSTRUCTION_MESSAGE,
                                 reply_markup=utils.get_default_keyboard(utils.NEW_TASK_BUTTON_TEXT),
                                 parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        except:
            await message.answer(utils.ERROR_MESSAGE,
                                 reply_markup=utils.get_default_keyboard(utils.NEW_TASK_BUTTON_TEXT))


@dp.message_handler(lambda message: message.text == utils.CANCEL_COMPANY_BUTTON_TEXT,
                    state=NewUser.SaveOrCancel)
async def cancel_company_name(message: types.Message):
    await message.answer(utils.COMPANY_NAME_CANCEL)
    await NewUser.GetCompanyName.set()


@dp.message_handler(lambda message: message.text == utils.NEW_TASK_BUTTON_TEXT)
async def create_task(message: types.Message):
    await message.answer(utils.NEW_TASK_PROMPT)
    await NewTask.GetTask.set()


@dp.message_handler(state=NewTask.GetTask,
                    content_types=types.ContentType.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    try:
        user_id = str(message.from_user.id)
        file_id = message.document.file_id
        file = await crm_bot.get_file(file_id)
        file_path = file.file_path
        file_name = file_path.split('/')[-1]
        file_extension = file_name.split('.')[-1]
        downloaded_file = await crm_bot.download_file(file_path)
        file_content = downloaded_file.read()
        creation_date = datetime.datetime.now().strftime('%d/%m/%Y')
        with get_connection() as connection:
            task_id = db.add_task(connection, user_id, file_content, file_extension, creation_date)
            company_name = db.get_company_name(connection, user_id)
        await crm_bot.send_document(ADMIN_ID,
                                    caption=utils.TASK_INFO.format(company_name, task_id, creation_date),
                                    document=file_id,
                                    reply_markup=utils.get_task_keyboard(task_id, user_id))
        await message.answer(utils.SUCCESS_FILE_SAVED.format(file_name),
                             reply_markup=utils.get_default_keyboard(utils.NEW_TASK_BUTTON_TEXT),
                             parse_mode=types.ParseMode.MARKDOWN)
    except Exception as e:
        await message.answer(utils.ERROR_MESSAGE,
                             reply_markup=utils.get_default_keyboard(utils.NEW_TASK_BUTTON_TEXT))
        traceback.print_exc()
    await state.finish()


@dp.callback_query_handler(lambda query: query.data.startswith('button_done_'))
async def process_done_button(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split('_')[-2]
    user_id = callback_query.data.split('_')[-1]
    with get_connection() as connection:
        db.remove_task(connection, task_id)
    await crm_bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)