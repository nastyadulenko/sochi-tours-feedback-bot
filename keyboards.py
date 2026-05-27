from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оставить отзыв")],
        [KeyboardButton(text="Админ-панель")]
    ],
    resize_keyboard=True
)

def tours_keyboard():
    tours = ["Ахун", "Водопады", "Роза Пик", "Дегустация"]
    buttons = []
    for tour in tours:
        buttons.append([InlineKeyboardButton(text=tour, callback_data=f"tour_{tour}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def rating_keyboard():
    buttons = []
    row = []
    for i in range(1, 6):
        row.append(InlineKeyboardButton(text=str(i), callback_data=f"rating_{i}"))
    buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="Отзывы", callback_data="admin_reviews")]
    ])