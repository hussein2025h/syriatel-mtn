from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.inline_keyboards import admin_response_keyboard
from database import update_status

ADMIN_ID = 782280301
admin_router = Router()

# قائمة لتخزين الطلبات مؤقتًا
requests = {}

@admin_router.message(Command("panel"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("غير مصرح لك بالدخول.")
    if not requests:
        return await message.answer("لا توجد طلبات حالياً.")
    
    for user_id, req in requests.items():
        await message.answer(
            f"طلب من @{req['username'] or 'مستخدم بدون معرف'}:
"
            f"المشغل: {req['operator']}
"
            f"الرقم: {req['number']}
"
            f"المبلغ: {req['amount']}",
            reply_markup=admin_response_keyboard(user_id)
        )

@admin_router.callback_query(F.data.startswith("approve_"))
async def approve_request(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("ليس لديك صلاحية.")
    
    user_id = int(callback.data.split("_")[1])
    await callback.bot.send_message(chat_id=user_id, text="تم تنفيذ طلبك بنجاح. شكراً لاستخدامك خدمتنا.")
    await callback.message.answer("تم إعلام المستخدم بالتنفيذ.")
    requests.pop(user_id, None)
    update_status(user_id, 'تم')
    await callback.answer()

@admin_router.callback_query(F.data.startswith("reject_"))
async def reject_request(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("ليس لديك صلاحية.")
    
    user_id = int(callback.data.split("_")[1])
    await callback.bot.send_message(chat_id=user_id, text="عذراً، تم رفض طلبك. يرجى المحاولة لاحقاً.")
    update_status(user_id, "مرفوض")
    await callback.message.answer("تم إعلام المستخدم بالرفض.")
    requests.pop(user_id, None)
    update_status(user_id, 'تم')
    await callback.answer()
