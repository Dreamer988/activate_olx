import os

from dotenv import load_dotenv

# Подгружаем переменные окружения
load_dotenv()

# Берем токен бота из переменных окруженмя
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID группы в тг для отправки активированных объектов на OLX
ACTIVATION_GROUP_ID = '-668180865'

# Пользователи с доступом
USER_ACCESS = ['535176521', '389654095']
