import os
import re
import time
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from filters.is_digit import IsDigit
from filters.user_access import UserAccess
from keyboards.default.public_olx import kb_public
from states import PublicStates
from data import config
from loader import dp
from selenium.webdriver.chrome.options import Options
load_dotenv()


@dp.message_handler(UserAccess(), commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}\n'
                         f'Чтобы запустить активацию нажми на комманду /public\n'
                         f'Чтобы остановить активация нажми на комманду /unpublic')


@dp.message_handler(UserAccess(), commands=['unpublic'], state='*')
async def start(message: types.Message, state=FSMContext):
    await message.answer('Активация остановлена.')
    await state.update_data(public=False)


@dp.message_handler(UserAccess(), commands=['public'])
async def start(message: types.Message, state=FSMContext):
    await message.answer('Выберите аккаунт для активации', reply_markup=kb_public)
    await PublicStates.Public_Q1.set()


@dp.message_handler(UserAccess(), state=PublicStates.Public_Q1)
async def start(message: types.Message, state=FSMContext):
    if message.text.strip().lower() == 'tiny_m':
        await state.update_data(public_login=os.getenv("OLX_LOGIN_TINY_M"))
        await state.update_data(public_password=os.getenv("OLX_PASSWORD_TINY_M"))

    elif message.text.strip().lower() == 'donmiklroze':
        await state.update_data(public_login=os.getenv("OLX_LOGIN_DONMIKLROZE"))
        await state.update_data(public_password=os.getenv("OLX_PASSWORD_DONMIKLROZE"))

    elif message.text.strip().lower() == '+998901757121':
        await state.update_data(public_login=os.getenv("OLX_LOGIN_+998901757121"))
        await state.update_data(public_password=os.getenv("OLX_LOGIN_998901757121"))

    await message.answer('Введите интервал в секундах (не менее 20)')
    await PublicStates.Public_Q2.set()


@dp.message_handler(UserAccess(), IsDigit(), state=PublicStates.Public_Q2)
async def start(message: types.Message, state=FSMContext):
    await message.answer('Активация запущена.')
    await state.update_data(public=True)
    await state.update_data(interval_time=message.text)

    # Функция активации
    with webdriver.Chrome(executable_path=os.getenv("PATH_CHROMIUM"),
                          options=Options().add_argument("--headless")) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.olx.uz/account/")

        values = await state.get_data()
        login = values['public_login']
        password = values['public_password']

        try:
            driver.find_element(By.ID, "userEmail").send_keys(login)
            driver.find_element(By.ID, "userPass").send_keys(password + Keys.ENTER)
            time.sleep(10)
        except:
            print("Не удалось войти в аккаунт")

        while True:
            value = await state.get_data()
            activate = value['public']
            interval_time = value['interval_time']

            if activate:
                try:
                    driver.get("https://www.olx.uz/myaccount/archive/")
                    time.sleep(5)
                    try:
                        title = driver.find_element(By.CSS_SELECTOR, '[class="myoffersnew__item"]'). \
                            find_element(By.TAG_NAME, "h3"). \
                            get_attribute("title")
                        try:
                            driver.find_element(By.CSS_SELECTOR, '[title="Активировать"]').send_keys(Keys.ENTER)
                            try:
                                id_active = re.findall(r'[А-Я]+\d{6}', title)
                                await dp.bot.send_message(chat_id=config.ACTIVATION_GROUP_ID,
                                                          text=f'Объект {id_active[0]} активирован.')
                                driver.refresh()
                                time.sleep(20)
                            except:
                                print("Не удалось получить ID объекта из регулярного выражения заголовка")
                                await dp.bot.send_message(f"ID не найден.\n"
                                                          f"Активирован объект с заголовком:\n"
                                                          f"{title}")
                                time.sleep(int(interval_time))
                                driver.refresh()
                        except:
                            print("Не удалось найти кнопку Активировать")
                            await message.answer("Ошибка: Не удалось найти кнопку Активировать")
                            await state.reset_state()
                            break
                    except:
                        print("Заголовок не найден")
                        await message.answer('Неактивные объекты закончились')
                        await state.reset_state()
                        break
                except:
                    print('Не получилось загрузить страницу https://www.olx.uz/myaccount/archive/')
                    break
            else:
                print("Активация остановлена")
                driver.quit()
                await state.reset_state()
                await state.reset_data()
                break
