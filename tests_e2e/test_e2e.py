import os
import time
from threading import Thread

import pytest
from selenium import webdriver
from dotenv import load_dotenv
import requests

import app

load_dotenv()
TRELLO_BASE_URL = 'https://api.trello.com/1'
TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET')


def create_trello_board():
    response = requests.post(
        url=f'{TRELLO_BASE_URL}/boards',
        params={
            'key': TRELLO_API_KEY,
            'token': TRELLO_API_SECRET,
            'name': 'Selenium Test Board'
        }
    )
    return response.json()['id']


def delete_trello_board(board_id):
    requests.delete(
        url=f'{TRELLO_BASE_URL}/boards/{board_id}',
        params={
            'key': TRELLO_API_KEY,
            'token': TRELLO_API_SECRET,
        }
    )


@pytest.fixture(scope='module')
def test_app():
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    yield driver

    # Tear Down
    driver.quit()


def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    add_new_task(driver)
    start_task(driver)
    complete_task(driver)
    mark_test_as_incomplete(driver)


def add_new_task(driver):
    new_task_input = driver.find_element_by_xpath("//*[@data-test-id='name-input']")
    new_task_input.send_keys('Test Task')

    driver.find_element_by_xpath("//button[contains(text(), 'Add Item')]").click()

    assert find_task_in_section('to-do-section', driver) is not None


def start_task(driver):
    task = find_task_in_section('to-do-section', driver)
    task.find_element_by_link_text('Start').click()

    assert find_task_in_section('doing-section', driver) is not None


def complete_task(driver):
    task = find_task_in_section('doing-section', driver)
    task.find_element_by_link_text('Complete').click()

    assert find_task_in_section('done-section', driver) is not None


def mark_test_as_incomplete(driver):
    task = find_task_in_section('done-section', driver)
    task.find_element_by_link_text('Mark as Incomplete').click()

    assert find_task_in_section('to-do-section', driver) is not None


def find_task_in_section(section_name, driver):
    section = driver.find_element_by_xpath(f"//*[@data-test-id='{section_name}']")
    tasks = section.find_elements_by_xpath("//*[@data-test-class='task']")
    return next(task for task in tasks if task.find_element_by_xpath("//*[contains(text(), 'Test Task')]") is not None)
