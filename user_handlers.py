from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline_keyboards import main_menu_keyboard, confirm_keyboard
from database import add_request

ADMIN_ID = 782280301
user_router = Router()

@user_router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "أهلاً بك في بوت تحويل الرصيد:
اختر نوع التحويل:",
        reply_markup=main_menu_keyboard()
    )

@user_router.callback_query(F.data.in_({"mtn", "syriatel"}))
async def operator_selected(callback: CallbackQuery):
    operator = "MTN" if callback.data == "mtn" else "Syriatel"
    await callback.message.answer(f"أدخل رقم الهاتف المراد تحويل الرصيد إليه ({operator}):")
    await callback.answer()
    await callback.message.bot.session.storage.set_data(callback.from_user.id, {"operator": operator, "step": "get_number"})

@user_router.message()
async def process_input(message: Message):
    data = await message.bot.session.storage.get_data(message.from_user.id)
    if not data:
        return await message.answer("يرجى اختيار نوع التحويل أولاً بالضغط على /start")
    
    if data.get("step") == "get_number":
        data["number"] = message.text
        data["step"] = "get_amount"
        await message.bot.session.storage.set_data(message.from_user.id, data)
        return await message.answer("أدخل المبلغ المراد تحويله:")
    
    if data.get("step") == "get_amount":
        data["amount"] = message.text
        await message.bot.session.storage.set_data(message.from_user.id, {})  # Clear session
        await message.answer("هل ترغب بإرسال الطلب؟", reply_markup=confirm_keyboard())
        await message.bot.session.storage.set_data(message.from_user.id, {"confirm_data": data})

@user_router.callback_query(F.data == "confirm_send")
async def confirm_send(callback: CallbackQuery):
    data = await callback.message.bot.session.storage.get_data(callback.from_user.id)
    info = data.get("confirm_data", {})
    text = f"طلب تحويل جديد:
المشغل: {info.get('operator')}
الرقم: {info.get('number')}
المبلغ: {info.get('amount')}
من: @{callback.from_user.username or callback.from_user.full_name}"
            # إضافة الطلب إلى قائمة الطلبات
        from handlers import admin_handler
        admin_handler.requests[message.from_user.id] = {
            "operator": data["operator"],
            "number": data["number"],
            "amount": data["amount"],
            "username": message.from_user.username
        }

                add_request(
            user_id=message.from_user.id,
            username=message.from_user.username,
            number=data["number"],
            amount=data["amount"],
            operator=data["operator"]
        )
        await callback.message.bot.send_message(chat_id=ADMIN_ID, text=text)
    await callback.message.answer("تم إرسال طلبك للإدارة، سيتم تنفيذ العملية قريبًا.")
    await callback.message.bot.session.storage.set_data(callback.from_user.id, {})
    await callback.answer()
