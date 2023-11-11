from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command

from app.misc.filters import IsSubscribedToChannels, IsRegistered
from app.misc.keyboards import main as main_kb, request as request_kb
from app.misc.states import RequestStates
from app.misc.translations import languages, translations, user_language as get_user_language


router: Router = Router()


@router.message(StateFilter(RequestStates.INSERT_MESSAGE), IsSubscribedToChannels(), IsRegistered(), Command(commands=['cancel']))
async def cmd_request_cancel(msg: Message, state: FSMContext) -> None:
    user_language: str = await get_user_language(telegram_id=msg.from_user.id, language_code=msg.from_user.language_code)
    await state.set_state(state=RequestStates.MAIN)
    await msg.reply(text=translations[user_language]['messages']['user']['request']['create']['cancel'], reply_markup=await request_kb(msg=msg))

for language in languages:
    @router.message(StateFilter(None), IsSubscribedToChannels(), IsRegistered(), F.text.lower() == translations[language]['keyboards']['reply']['user']['request']['main'].lower())
    async def cmd_request(msg: Message, state: FSMContext) -> None:
        user_language: str = await get_user_language(telegram_id=msg.from_user.id, language_code=msg.from_user.language_code)
        await state.set_state(state=RequestStates.MAIN)
        await msg.reply(text=translations[user_language]['messages']['user']['request']['main'], reply_markup=await request_kb(msg=msg))

for language in languages:
    @router.message(StateFilter(RequestStates.MAIN), IsSubscribedToChannels(), IsRegistered(), F.text.lower() == translations[language]['keyboards']['reply']['user']['request']['create'].lower())
    async def cmd_request_create_insert_message(msg: Message, state: FSMContext) -> None:
        user_language: str = await get_user_language(telegram_id=msg.from_user.id, language_code=msg.from_user.language_code)
        await state.set_state(state=RequestStates.INSERT_MESSAGE)
        await msg.reply(text=translations[user_language]['messages']['user']['request']['create']['message'], reply_markup=ReplyKeyboardRemove())

@router.message(StateFilter(RequestStates.INSERT_MESSAGE), IsSubscribedToChannels(), IsRegistered())
async def cmd_request_create(msg: Message, state: FSMContext) -> None:
    user_language: str = await get_user_language(telegram_id=msg.from_user.id, language_code=msg.from_user.language_code)
    min_length: int = 32
    if len(msg.text) < min_length:
        await msg.reply(text=str.format(translations[user_language]['messages']['user']['request']['create']['message_too_short'], min_length))
        await msg.answer(text=translations[user_language]['messages']['user']['request']['create']['message'])
        return
    await state.set_state(state=RequestStates.MAIN)
    await msg.reply(text=translations[user_language]['messages']['user']['request']['create']['success'], reply_markup=await request_kb(msg=msg))

for language in languages:
    @router.message(StateFilter(RequestStates.MAIN), IsSubscribedToChannels(), IsRegistered(), F.text.lower() == translations[language]['keyboards']['reply']['user']['request']['back'].lower())
    async def cmd_request_exit(msg: Message, state: FSMContext) -> None:
        user_language: str = await get_user_language(telegram_id=msg.from_user.id, language_code=msg.from_user.language_code)
        await state.clear()
        await msg.reply(text=translations[user_language]['messages']['user']['request']['back'], reply_markup=await main_kb(msg=msg))