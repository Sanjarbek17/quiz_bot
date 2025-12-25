
import asyncio
import json
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, PollHandler, ContextTypes, PollAnswerHandler
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

active_quiz = {}
user_correct = {}  # user_id -> correct_count
user_names = {}    # user_id -> user_name

with open('input/quiz_questions.json', 'r') as f:
    QUIZ_QUESTIONS = json.loads(f.read())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to the Quiz Bot! Type /quiz to start the quiz.')

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in active_quiz:
        await update.message.reply_text('A quiz is already active in this chat. Please wait for it to finish.')
        return
    active_quiz[chat_id] = {'poll_ids': [], 'results': []}

    # 🔥 DO NOT await
    context.application.create_task(
        run_quiz_flow(context, chat_id)
    )


# Run the quiz: send each poll, wait for open_period, then show statistics
async def run_quiz_flow(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    open_period = 10
    stop = 10
    start = random.randint(0, len(QUIZ_QUESTIONS) - stop)

    for q in QUIZ_QUESTIONS[start:start + stop]:
        message = await context.bot.send_poll(
            chat_id=chat_id,
            question=q['question'],
            options=q['options'],
            type='quiz',
            correct_option_id=q['correct_option_id'],
            is_anonymous=False,
            open_period=open_period
        )

        active_quiz[chat_id]['poll_ids'].append(message.poll.id)

        # wait ONLY for this poll
        await asyncio.sleep(open_period + 1)

    await show_quiz_statistics(context, chat_id)
    del active_quiz[chat_id]


# PollHandler: called when a poll is closed (open_period ends)
async def handle_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Poll closed or updated')
    poll = update.poll
    # Find which chat this poll belongs to
    chat_id = None
    for cid, quiz in active_quiz.items():
        if poll.id in quiz['poll_ids']:
            chat_id = cid
            break
    if chat_id is None:
        return
    # Save poll results
    active_quiz[chat_id]['results'].append(poll)
    
async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Poll answer received', update.poll_answer)
    global user_correct, user_names
    answer = update.poll_answer
    user_id = answer.user.id
    user_names[user_id] = answer.user.full_name if hasattr(answer.user, 'full_name') else str(user_id)
    # Find which poll/question this answer is for
    for chat_id, quiz in active_quiz.items():
        for idx, poll_id in enumerate(quiz['poll_ids']):
            if poll_id == answer.poll_id:
                q = QUIZ_QUESTIONS[idx]
                if answer.option_ids and q['correct_option_id'] in answer.option_ids:
                    user_correct[user_id] = user_correct.get(user_id, 0) + 1
                return


# Show quiz statistics/leaderboard for a chat (by user, not by question)
async def show_quiz_statistics(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    print('user correct:', user_correct)
    leaderboard = [(user_id, user_names.get(user_id, str(user_id)), count) for user_id, count in user_correct.items()]
    leaderboard.sort(key=lambda x: x[2], reverse=True)
    result_text = '🏆 User Leaderboard (by correct answers) 🏆\n\n'
    for rank, (user_id, name, count) in enumerate(leaderboard, 1):
        result_text += f"{rank}. {name}: {count} correct\n"
    if not leaderboard:
        result_text += 'No answers recorded.'
    await context.bot.send_message(chat_id=chat_id, text=result_text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('quiz', quiz))
    app.add_handler(PollAnswerHandler(handle_poll_answer))
    app.add_handler(PollHandler(handle_poll))
    app.run_polling(
        allowed_updates=[
            Update.MESSAGE,
            Update.POLL,
            Update.POLL_ANSWER,
        ]
    )

if __name__ == '__main__':
    main()
