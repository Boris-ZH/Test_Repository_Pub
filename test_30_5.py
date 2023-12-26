import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome('E:\chromedriver-win64\chromedriver.exe')
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_all_pets(driver):
    # Проверяем, что представлены все питомцы, количество питомцев в статистике соответствует реальному
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('bobos@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Настраиваем неявные ожидания:
    driver.implicitly_wait(5)

    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    # Нажимаем на кнопку Мои питомцы
    driver.find_element(By.CSS_SELECTOR, '#navbarNav > ul > li:nth-child(1) > a').click()
    # Проверяем, что количество питомцев в статистике соответствует реальному
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)


def test_check_names_types_age(driver):
    # Проверяем, что указаны имена, тип и возраст питомцев
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('bobos@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 5)
    # Ожидаем в течение 5с, что на странице есть тег h1 с текстом "PetFriends"
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
    #images = driver.find_elements(By.CSS_SELECTOR, '.text-center.card-img-top')
    #names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    #descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    # Ищем в теле таблицы все имена питомцев и проверяем, что у всех есть имя:
    name_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]')
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Ищем в теле таблицы тип питомцев и проверяем, что у всех есть тип:
    type_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[2]')
    for i in range(len(name_my_pets)):
        assert type_my_pets[i].text != ''

    # Ищем в теле таблицы возраст питомцев и проверяем, что у всех есть возраст:
    age_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[3]')
    for i in range(len(name_my_pets)):
        assert age_my_pets[i].text != ''


def test_check_image(driver):
    # Проверяем, что представлены все питомцы, количество питомцев в статистике соответствует реальному
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('bobos@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Настраиваем неявные ожидания:
    driver.implicitly_wait(5)

    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    # Нажимаем на кнопку Мои питомцы
    driver.find_element(By.CSS_SELECTOR, '#navbarNav > ul > li:nth-child(1) > a').click()

    # Ищем на странице /my_pets всю статистику пользователя,
    # и вычленяем из полученных данных количество питомцев пользователя:
    all_statistics = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])
    image_my_pets = driver.find_elements(By.CSS_SELECTOR('img[style="max-width: 100px; max-height: 100px;"]')
    # Проверяем, что хотя бы у половины питомцев есть фото:
    m = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            m += 1
    assert m >= all_my_pets / 2

    # Проверяем, что у всех питомцев разные имена:
    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
    set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
    assert len(list_name_my_pets) == len(
        set_name_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
    list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
    set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
    assert len(list_data_my_pets) == len(
        set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

