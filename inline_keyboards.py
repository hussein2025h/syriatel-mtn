from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="MTN", callback_data="mtn")],
        [InlineKeyboardButton(text="Syriatel", callback_data="syriatel")]
    ])

def confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تأكيد الإرسال", callback_data="confirm_send")]
    ])

def admin_response_keyboard(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="تم التنفيذ", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton(text="رفض", callback_data=f"reject_{user_id}")
        ]
    ])
