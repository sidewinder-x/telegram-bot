import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from keyboards import main_menu, back_button, order_services_kb
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dp = Dispatcher(storage=MemoryStorage())

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

ADMIN_ID = 1102002634  # ← Замени на свой Telegram ID

@dp.message(F.text, F.text.in_({"start", "/start"}))
async def start(message: Message):
    photo = FSInputFile("welcome2.png")
    await message.answer_photo(
        photo,
        caption=(
            "<b>👋 ¡Hola! Soy Sergio Aldman</b>\n\n"
            "Ayudo a pequeños negocios a <b>entrar al mundo online</b>\n"
            "a través de <b>sitios web</b>, <b>bots</b> y <b>diseño de redes sociales</b>.\n\n"
            "Estás dentro de mi <b>portafolio en Telegram</b> 💼"
        )
    )
    await message.answer("👇 ¿Con qué te gustaría empezar?", reply_markup=main_menu)

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 <b>Estás en el menú principal</b>\n\n"
        "¿Qué te interesa? Elegí una opción abajo 👇",
        reply_markup=main_menu
    )

@dp.callback_query(F.data == "services")
async def services(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🛠 Servicios que ayudarán a tu negocio a estar online</b>\n\n"
        "<b>📲 Diseño para redes sociales — desde $25 USD</b>\n"
        "• Foto de perfil, portada, highlights\n"
        "• Plan de contenido para 15 días\n"
        "• 5 plantillas para posts\n"
        "• Checklist de gestión\n\n"

        "<b>🤖 Bot de Telegram personalizado — desde $40 USD</b>\n"
        "• Pedidos, reservas, respuestas automáticas\n"
        "• Notificaciones y conexión a Google Sheets\n\n"

        "<b>🌐 Landing page — desde $60 USD</b>\n"
        "• Diseño moderno y adaptable\n"
        "• Formularios, botones, analíticas\n\n"

        "<b>🔑 Pack completo — desde $99 USD</b>\n"
        "• Landing + bot + redes sociales\n"
        "• Estrategia personalizada\n",

        reply_markup=back_button
    )

@dp.callback_query(F.data == "portfolio")
async def portfolio(callback: CallbackQuery):
    await callback.message.edit_text(
        "📂 <b>Portafolio</b>\n\n"
        "🧠 <b>Este bot</b> en el que estás ahora — <b>@aldman_bot</b> — es parte de mi trabajo.\n"
        "Lo diseñé como una forma simple y efectiva de presentar mis servicios, automatizar respuestas y tomar pedidos.\n\n"
        "🌐 Además, podés ver un ejemplo de sitio web que hice:\n"
        "https://surl.li/wjczqw\n\n"
        "Estoy trabajando en más ejemplos visuales que subiré pronto 😉",
        reply_markup=back_button,
        disable_web_page_preview=True
    )

@dp.callback_query(F.data == "why")
async def why(callback: CallbackQuery):
    await callback.message.edit_text(
        "💡<b> ¿Por qué lo necesitas?</b>\n\n"
        "Muchos negocios ofrecen buenos servicios, pero:\n"
        "— No aparecen en Google\n"
        "— No tienen redes activas\n"
        "— Nadie los encuentra\n\n"
        "Están perdiendo clientes todos los días sin darse cuenta.\n\n"
        "Con una web simple, redes ordenadas y respuestas automáticas,\n"
        "tu negocio empieza a parecer más profesional, confiable y activo.\n\n"
        "Así más personas te encuentran, te eligen y vuelven.",
        reply_markup=back_button
    )

@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.edit_text(
        "👋<b> Me llamo Sergey y soy consultor digital</b>\n\n"
        "Trabajo con pequeños negocios que quieren verse más profesionales y ser encontrados online.\n\n"
        "Creo sitios web simples que se ven bien y funcionan.\n"
        "Conecto WhatsApp, organizo tus redes y automatizo respuestas.\n\n"
        "Trabajo rápido, sin vueltas raras. Soluciones claras, accesibles y enfocadas en resultados reales.\n\n"
        "🌐 Mi sitio: https://surl.li/wjczqw\n"
        "✉️ Contacto: @sidewinder_x",
        reply_markup=back_button,
        disable_web_page_preview=True
    )

@dp.message(F.text == "/start order")
async def start_order_from_link(message: Message, state: FSMContext):
    await message.answer(
        "🛍️ ¿Qué servicio te interesa?",
        reply_markup=order_services_kb
    )
    await state.set_state(OrderSteps.waiting_for_service)
class OrderSteps(StatesGroup):
    waiting_for_service = State()
    waiting_for_name = State()
    waiting_for_contact = State()


@dp.callback_query(F.data == "order")
async def start_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🛍️ ¿Qué servicio te interesa?",
        reply_markup=order_services_kb
    )
    await state.set_state(OrderSteps.waiting_for_service)

@dp.callback_query(F.data.startswith("service_"))
async def service_chosen(callback: CallbackQuery, state: FSMContext):
    service = callback.data.replace("service_", "").capitalize()
    await state.update_data(service=service)
    await callback.message.answer("✍️ Escribí tu nombre y apellido:")
    await state.set_state(OrderSteps.waiting_for_name)


@dp.message(OrderSteps.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📱 Ahora dejá tu número de contacto o usuario de Facebook:")
    await state.set_state(OrderSteps.waiting_for_contact)

@dp.message(OrderSteps.waiting_for_contact)
async def get_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    user = message.from_user

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📥 <b>Nueva solicitud</b>\n\n"
            f"🛍️ Servicio: <b>{data['service']}</b>\n"
            f"👤 Nombre: <b>{data['name']}</b>\n"
            f"📱 Contacto: <b>{data['contact']}</b>\n\n"
            f"🔗 Telegram: @{user.username or 'Sin usuario'}\n"
            f"🆔 ID: <code>{user.id}</code>"
        ),
        parse_mode="HTML"
    )

    await message.answer("✅ ¡Tu solicitud fue enviada! Me pondré en contacto contigo pronto.")
    await state.clear()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())