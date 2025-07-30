from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query
import time
load_dotenv()

db = TinyDB('db.json')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Quiz Bot! Use /quiz to start a quiz.')

def quiz(update: Update, context: CallbackContext) -> None:
    """Shows list of available quizzes."""
    chat_id=update.message.chat.id
    reply_markup=ReplyKeyboardMarkup(
        [[KeyboardButton('matematika'),KeyboardButton('tarix'),KeyboardButton('fizika')]],
        resize_keyboard=True
    )
    context.bot.send_message(chat_id=chat_id,text='quiz',reply_markup=reply_markup)
s=0
button={
    "a":"A",
    "b":"B",
    "c":"C",
    "d":"D"
}
def handle_quiz(update, context):
    global s
    record = db.all()
    
    if s >= len(record):
        if update.callback_query:
            chat_id = update.callback_query.message.chat.id
        else:
            chat_id = update.message.chat.id
        
        context.bot.send_message(
            chat_id=chat_id,
            text=f"Test tugadi!\nTo'g'ri javoblar: {togri_javob}\nNoto'g'ri javoblar: {notogri_javob}"
        )
        return
    

    if update.callback_query:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    a = InlineKeyboardButton(text=f"{button['a']}", callback_data='a')
    b = InlineKeyboardButton(text=f"{button['b']}", callback_data='b')
    c = InlineKeyboardButton(text=f"{button['c']}", callback_data='c')
    d = InlineKeyboardButton(text=f"{button['d']}", callback_data='d')
    reply_markup = InlineKeyboardMarkup([[a, b, c, d]])

    context.bot.send_message(
        chat_id=chat_id,
        text=f"{record[s]['savoli']}\nA) {record[s]['a']}\nB) {record[s]['b']}\nC) {record[s]['c']}\nD) {record[s]['d']}",
        reply_markup=reply_markup
    )
    s += 1


def handle_quiz_selection(update: Update, context: CallbackContext) -> None:
    global s
    text = update.message.text
    if text.lower() == 'matematika':
        handle_quiz(update, context)
togri_javob=0
notogri_javob=0
def Answer(update: Update, context: CallbackContext) -> None:
    """
    Handle user answers to quiz questions(a,b,c,d).
    This function will check the user's answer against the correct answer
    and gives next question or end the quiz.
    """
    l='✅'
    l1='❌'
    global s,button,togri_javob,notogri_javob
    query=update.callback_query
    chat_id=query.message.chat.id  
    ansver=db.all()[s-1]
    if query.data==ansver["j"]:
        button[query.data]+=l
        togri_javob+=1
        a = InlineKeyboardButton(text=f"{button['a']}", callback_data='a')
        b = InlineKeyboardButton(text=f"{button['b']}", callback_data='b')
        c = InlineKeyboardButton(text=f"{button['c']}", callback_data='c')
        d = InlineKeyboardButton(text=f"{button['d']}", callback_data='d')
        reply_markup = InlineKeyboardMarkup([
            [a, b, c, d]
        ])
        response_text=f"{ansver['savoli']}\nA) {ansver['a']}\nB) {ansver['b']}\nC) {ansver['c']}\nD) {ansver['d']}"
    elif query.data!=ansver["j"]:
        button[query.data]+=l1
        button[ansver['j']]+=l
        notogri_javob+=1
        a = InlineKeyboardButton(text=f"{button['a']}", callback_data='a')
        b = InlineKeyboardButton(text=f"{button['b']}", callback_data='b')
        c = InlineKeyboardButton(text=f"{button['c']}", callback_data='c')
        d = InlineKeyboardButton(text=f"{button['d']}", callback_data='d')
        reply_markup = InlineKeyboardMarkup([
            [a, b, c, d]
        ])
        response_text=response_text=f"{ansver['savoli']}\nA) {ansver['a']}\nB) {ansver['b']}\nC) {ansver['c']}\nD) {ansver['d']}"
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text=response_text,
        reply_markup=reply_markup,
    )
    button={
    "a":"A",
    "b":"B",
    "c":"C",
    "d":"D"
    }
    handle_quiz(update, context)

    

def main() -> None:
    token = os.getenv('token')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        return
    
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("quiz",quiz ))
    dispatcher.add_handler(MessageHandler(filters=Filters.all,callback=handle_quiz_selection))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    dispatcher.add_handler(CallbackQueryHandler(Answer))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
