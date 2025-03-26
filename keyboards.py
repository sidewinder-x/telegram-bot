from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню на испанском + структурировано красиво
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📌 Servicios", callback_data="services"),
        InlineKeyboardButton(text="📂 Portafolio", callback_data="portfolio")
    ],
    [
        InlineKeyboardButton(text="ℹ️ Sobre mí", callback_data="about"),
        InlineKeyboardButton(text="💡¿Por qué importa?", callback_data="why")
    ],
    [
        InlineKeyboardButton(text="📝 Hacer pedido", callback_data="order")
    ]
])
# Кнопка назад
back_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Volver", callback_data="back")]
])

order_services_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎨 Diseño", callback_data="service_diseño")],
    [InlineKeyboardButton(text="🤖 Bot de Telegram", callback_data="service_bot")],
    [InlineKeyboardButton(text="🌐 Landing Page", callback_data="service_landing")],
    [InlineKeyboardButton(text="🔑 Pack completo", callback_data="service_pack")]
])