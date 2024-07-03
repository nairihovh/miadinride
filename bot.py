import asyncio

import config
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart, Command
from aiogram.client.default import DefaultBotProperties

import functions
from markups import *
from aiogram.enums import ParseMode, ChatMemberStatus

from api import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
logger = logging.getLogger(__name__)


db = Database("db.sql")

user_steps = {}


async def check_phone_number(step, user, message, text, user_id, force=False):
    if user[4] != None and not force\
            and step != "phone_number":
        return True
    if force or (user[4] == None and step != "phone_number"):
        user_steps[user_id] = {"step": "phone_number"}
        await message.answer("Ուղարկեք ձեր հեռախոսահամարը")
        return False

    if step == "phone_number":
        if text.startswith("0") or text.startswith("+374"):
            db.setPhoneNumber(user_id=user_id, phone_number=text)
            await message.answer("Ձեր հեռախոսահամաը տեղադրված է։\n"
                                 f"{text}")
            user_steps[user_id] = {"step": "choose_option"}
            await send_welcome(message)
        else:
            await message.answer("Ուղարկեք ձեր հեռախոսահամարը")
            return False


async def subscribed(message: Message):
    channel_id = config.CHANNEL_ID
    try:
        user_member_status = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)
        if user_member_status.status != ChatMemberStatus.LEFT:
            return True
    except Exception as e:
        print(f"Error checking user subscription: {e}")
    return False


@dp.message(Command("set_phone_number"))
async def change_phone_number(message):
    user_id = message.from_user.id
    user = db.getUser(user_id)
    if db.userExists(user_id):
        user_steps[message.from_user.id] = {"step": "choose_option"}
        user_option = user_steps.get(user_id, {"step": "choose_option"})
        step = user_option.get("step")
        text = message.text
        await check_phone_number(step, user, message, text, user_id, True)


@dp.message(CommandStart())
async def send_welcome(message):
    db.registerUser(message.from_user.id, message.from_user)
    text = message.text
    user_id = message.from_user.id

    user_steps[message.from_user.id] = {"step" : "choose_option"}
    await message.answer(f"Բոտից օգտվելու համար օգտվեք սեղմակներից։", reply_markup=markup)
    user_option = user_steps.get(user_id, {"step": "choose_option"})
    is_subscribed = await subscribed(message)
    if not is_subscribed:
        await message.answer(f"Խնդրում ենք բաժանորդագրվել մեր ալիքին։ {config.CHANNEL_ID}")

    step = user_option.get("step")
    user = db.getUser(user_id)
    if user[4] == None:
        await check_phone_number(step, user, message, text, user_id)


@dp.callback_query()  # Use the decorator without arguments
async def handle_callback(call: aiogram.types.CallbackQuery):
    if db.userExists(call.from_user.id):
        user = db.getUser(call.from_user.id)
    try:
        msg = f"`{call.from_user.first_name}`-ը ցանկանում է կապնվել ձեզ հետ ուղեւորության հարցով։"
        if user:
            phone_number = str(user[4])
            if phone_number.startswith("374"):
                phone_number.replace("374", "+374")
            else:
                phone_number = "0"+phone_number
            msg += f"\nՆրա հեռախոսահամարն է՝ {phone_number}"
        await bot.send_message(int(call.data), msg)
        await bot.send_message(int(call.from_user.id), f"Դուք ցանկանում եք սկսել երթեւեկությունը ալիքում դրված հայտարարություններից մեկի հետ, շուտով հայտատերը կկապնվի ձեզ հետ։")
    except Exception as e:
        print(e)
    await call.answer("Ուղարկված է պատվիրատուին, շուտով նա կապ կհաստատի ձեզ հետ։")

@dp.message()
async def handle_messages(message):
    user_id = message.from_user.id
    text = message.text
    user_option = user_steps.get(user_id, {"step": "choose_option"})
    step = user_option.get("step")
    user = db.getUser(user_id)
    is_subscribed = await subscribed(message)
    if not is_subscribed:
        await message.answer(f"Խնդրում ենք բաժանորդագրվել մեր ալիքին։ {config.CHANNEL_ID}")
        return

    if user[4] == None or step == "phone_number":
        await check_phone_number(step, user, message, text, user_id)
        return

    if text == "Հետ":
        await handle_back(message, user_option)
        return

    if text[-2:] == "ic" or text[-2:] == "ից":
        text = text.replace(text[-2:], "")

    await handle_step(step=step, text=text, user_id=user_id, message=message, user_option=user_option)


async def handle_step(step, text, user_id, message, user_option):
    if step == "choose_option":
        if text == "Գնում եմ, կտանեմ":
            user_steps[user_id] = {"step" : "is_going"}
            user_steps[user_id].update({"type": "is_going"})
            msg = functions.generateText(user_option, step, text)
            await message.answer(msg, reply_markup=markup_remove_with_back)
        elif text == "Ցանկանում եմ գնալ":
            user_steps[user_id] = {"step": "want_to_go"}
            user_steps[user_id].update({"type": "want_to_go"})
            msg = functions.generateText(user_option, step, text)
            await message.answer(msg, reply_markup=markup_remove_with_back)
        else:
            await message.answer("Ուղարկեք «Գնում եմ, կտանեմ» հրամանը։")
    elif step == "is_going":
        user_steps[user_id].update({"step": "from"})
        user_steps[user_id].update({"from": text})
        msg = functions.generateText(user_option, step, text)
        await message.answer(msg, reply_markup=markup_remove_with_back)
    elif step == "want_to_go":
        user_steps[user_id].update({"step": "from"})
        user_steps[user_id].update({"from": text})
        msg = functions.generateText(user_option, step, text)
        await message.answer(msg, reply_markup=markup_remove_with_back)
    elif step == "from":
        user_steps[user_id].update({"step": "to"})
        user_steps[user_id].update({"to": text})
        msg = functions.generateText(user_option, step, text)
        await message.answer(msg, reply_markup=markup_remove_with_back)
    elif step == "to":
        user_steps[user_id].update({"step": "when"})
        user_steps[user_id].update({"when": text})
        msg = functions.generateText(user_option, step, text)
        await message.answer(msg, reply_markup=markup_remove_with_back)
    elif step == "when":
        try:
            count = int(text)
        except:
            await message.answer("Գրեք միայն թիվ։")
            return
        user_steps[user_id].update({"step": "count"})
        user_steps[user_id].update({"count": count})
        msg = functions.generateText(user_option, step, text)
        await message.answer(msg, reply_markup=markup_remove_with_back)
    elif step == "count":
        user_steps[user_id].update({"step": "price"})
        user_steps[user_id].update({"price": text})
        msg = functions.generateText(user_option, step, text)
        await message.answer(msg, reply_markup=markup_apply_reject)
    elif step == "price":
        if text == "Հաստատել":
            await handle_apply(message, user_option)
        elif text == "Մերժել/Ջնջել":
            await handle_reject(message, user_option)
    else:
        await message.answer("Ինչ որ բան սխալ է։")


async def handle_apply(message, user_option):
    user_option = user_option
    user_option.update({"user_chat_id" : message.from_user.id})
    # print(user_option)
    msg = ""
    if user_option['type'] == "want_to_go":
        msg = (f"***{message.from_user.first_name}***-ն ***{user_option['when']}***\n"
               f"***{user_option['from']}***-ից ցանկանում է գնալ ***{user_option['to']}***\n"
               f"Ուղեւորների քանակը՝ ***{user_option['count']}***\n"
               f"Մեկ անձի համար պատրաստ է վճարել՝ ***{user_option['price']}*** AMD\n")
    else:
        msg = (f"***{message.from_user.first_name}***-ն ***{user_option['when']}***\n"
               f"***{user_option['from']}***-ից գնում է ***{user_option['to']}***\n"
               f"Մեքենայի մեջ կա ***{user_option['count']}*** ազատ տեղ\n"
               f"Ամեն անձի վճարը՝ ***{user_option['price']}*** AMD\n")
    markup_want_to_go, markup_is_going = create_inline_markups(message.from_user.id)
    inline_markup = markup_want_to_go if user_option['type'] == "is_going" else markup_is_going
    try:
        msg += (f"\n\nՍեղմելուց առաջ ցանկալի է\n"
               f"որ գրանցված լինեք մեր @miasinridebot-ում")
        await bot.send_message(config.CHANNEL_ID, msg,
                               reply_markup=inline_markup)
        await message.answer("Ձեր պատվերը գրանցված է")
        await send_welcome(message)
    except Exception as e:
        await message.answer(f"Տեղի է ունեցել սխալ։, {e}")

async def handle_reject(message, user_option):
    await send_welcome(message)


async def handle_back(message, user_option):
    step = user_option.get("step")
    steps_back = {
        'is_going' : ('choose_option', markup, "Ընտրե'ք"),
        'want_to_go' : ('choose_option', markup, "Ընտրե'ք"),
        'from' : ('is_going' if user_option.get('type') == 'is_going' else 'want_to_go', markup_remove_with_back, ""),
        'to' : ('from', markup_remove_with_back, ""),
        'when': ('to', markup_remove_with_back, ""),
        'count': ('when', markup_remove_with_back, ""),
        'price': ('count', markup_remove_with_back, "")
    }

    if step in steps_back:
        user_option['step'], mark, msg = steps_back[step]
        try:
            back_step = steps_back[user_option['step']][0]
        except:
            back_step = user_option['step']
        if not msg:
            print(step, back_step)
            msg = functions.generateText(user_option, back_step)
        await message.answer(msg, reply_markup=mark)
    else:
        await message.answer("Հետ գնալ հնարավոր չէ։")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting the bot...")
    asyncio.run(main())