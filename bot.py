import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

API_URL = "http://127.0.0.1:8000"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Токен Telegram-бота не найден. Проверь файл .env")

# Логи
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)



# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /start")
    await update.message.reply_text(
        "Привет! Я бот для управления задачами.\nИспользуй /help для списка команд."
    )


# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /help")
    help_text = (
        "/add_task <title> - Добавить задачу\n"
        "/list_tasks - Показать все задачи\n"
        "/get_task <id> - Показать задачу по ID\n"
        "/update_task <id> <title> - Обновить задачу\n"
        "/delete_task <id> - Удалить задачу\n"
    )
    await update.message.reply_text(help_text)


# /add_task
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /add_task")
    if len(context.args) == 0:
        await update.message.reply_text("Укажи название задачи. Пример: /add_task Купить молоко")
        return

    task_title = " ".join(context.args)
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(f"{API_URL}/tasks/", json={"title": task_title})
            logger.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                await update.message.reply_text(f"Задача добавлена: {task_title}")
            else:
                await update.message.reply_text("Ошибка при добавлении задачи.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка при подключении к API.")


# Команда /list_tasks
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /list_tasks")
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"{API_URL}/tasks/")
            logger.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                tasks = response.json()
                tasks_text = "\n".join([f"{task['id']}: {task['title']}" for task in tasks])
                await update.message.reply_text(tasks_text or "Список задач пуст.")
            else:
                await update.message.reply_text("Ошибка при получении списка задач.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка при подключении к API.")


# /get_task
async def get_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /get_task")
    if len(context.args) == 0:
        await update.message.reply_text("Укажи ID задачи. Пример: /get_task 1")
        return

    task_id = context.args[0]
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"{API_URL}/tasks/{task_id}")
            logger.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                task = response.json()
                await update.message.reply_text(f"Задача {task['id']}: {task['title']}")
            else:
                await update.message.reply_text("Задача не найдена.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка при подключении к API.")


# /update_task
async def update_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /update_task")
    if len(context.args) < 2:
        await update.message.reply_text("Укажи ID и новое название задачи. Пример: /update_task 1 Новое название")
        return

    task_id, task_title = context.args[0], " ".join(context.args[1:])
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.put(f"{API_URL}/tasks/{task_id}", json={"title": task_title})
            logger.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                await update.message.reply_text(f"Задача обновлена: {task_title}")
            else:
                await update.message.reply_text("Ошибка при обновлении задачи.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка при подключении к API.")


# /delete_task
async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /delete_task")
    if len(context.args) == 0:
        await update.message.reply_text("Укажи ID задачи. Пример: /delete_task 1")
        return

    task_id = context.args[0]
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(f"{API_URL}/tasks/{task_id}")
            logger.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                await update.message.reply_text("Задача удалена.")
            else:
                await update.message.reply_text("Ошибка при удалении задачи.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка при подключении к API.")


2
def main():
    logger.info("Инициализация бота...")
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_task", add_task))
    application.add_handler(CommandHandler("list_tasks", list_tasks))
    application.add_handler(CommandHandler("get_task", get_task))
    application.add_handler(CommandHandler("update_task", update_task))
    application.add_handler(CommandHandler("delete_task", delete_task))

    logger.info("🚀 Бот запущен и ожидает команды!")
    application.run_polling()


if __name__ == "__main__":
    main()
