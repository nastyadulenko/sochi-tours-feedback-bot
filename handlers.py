from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database as db
import keyboards as kb
from config import ADMIN_ID

router = Router()

class ReviewState(StatesGroup):
    waiting_tour = State()
    waiting_rating = State()
    waiting_text = State()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Поделитесь впечатлениями о туре.",
        reply_markup=kb.main_keyboard
    )

@router.message(F.text == "Оставить отзыв")
async def start_review(message: Message, state: FSMContext):
    await message.answer("Выберите тур:", reply_markup=kb.tours_keyboard())
    await state.set_state(ReviewState.waiting_tour)

@router.callback_query(ReviewState.waiting_tour, F.data.startswith("tour_"))
async def process_tour(callback: CallbackQuery, state: FSMContext):
    tour_name = callback.data.replace("tour_", "")
    await state.update_data(tour=tour_name)
    await callback.message.edit_text("Оцените от 1 до 5:", reply_markup=kb.rating_keyboard())
    await state.set_state(ReviewState.waiting_rating)
    await callback.answer()

@router.callback_query(ReviewState.waiting_rating, F.data.startswith("rating_"))
async def process_rating(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.replace("rating_", ""))
    await state.update_data(rating=rating)
    await callback.message.edit_text("Напишите ваш отзыв:")
    await state.set_state(ReviewState.waiting_text)
    await callback.answer()

@router.message(ReviewState.waiting_text)
async def process_feedback(message: Message, state: FSMContext):
    data = await state.get_data()
    
    db.save_review(
        tour_name=data['tour'],
        rating=data['rating'],
        feedback=message.text,
        username=message.from_user.username or "no_name",
        user_id=message.from_user.id
    )
    
    await message.answer("Спасибо за отзыв!")
    await state.clear()

@router.message(F.text == "Админ-панель")
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Админ-панель", reply_markup=kb.admin_keyboard())
    else:
        await message.answer("Нет доступа")

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа")
        return
    
    stats = db.get_stats()
    text = f"Всего отзывов: {stats['total']}\nСредний рейтинг: {stats['avg']}"
    await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data == "admin_reviews")
async def admin_reviews(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа")
        return
    
    reviews = db.get_reviews(5)
    if not reviews:
        await callback.message.edit_text("Нет отзывов")
        return
    
    text = "Последние отзывы:\n\n"
    for rev in reviews:
        text += f"{rev['username']}: {rev['rating']}/5\n{rev['feedback'][:50]}\n---\n"
    
    await callback.message.edit_text(text)
    await callback.answer()