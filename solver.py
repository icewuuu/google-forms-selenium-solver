import random
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import json

AnswerType = Dict[str, List[float] | List[str]]


def load_config(filename: str) -> Dict:
    with open(filename, 'r') as file:
        config_file = json.load(file)
    return config_file


def click_random_button(xpath_list: List[str], weights: List[float] = None) -> None:
    """
    Click a random button from the provided list of XPaths.

    Parameters:
    - xpath_list (list): List of XPaths representing buttons.
    - weights (list): Weights for each XPath, used for weighted random selection.

    Returns:
    - None
    """

    chosen_xpath = random.choices(xpath_list, weights=weights)[0] if weights else random.choice(xpath_list)

    button = browser.find_element(By.XPATH, chosen_xpath)
    button.click()


def fill_survey(questions: List[AnswerType], send_xpath: str) -> None:
    """
    Fill out a survey by clicking random buttons for each question.

    Parameters:
    - questions (list): List of dictionaries, each representing a survey question.

    Returns:
    - None
    """
    for question in questions:
        click_random_button(question['buttons'], weights=question['weights'])

    send_button = browser.find_element(By.XPATH, send_xpath)
    send_button.click()


if __name__ == "__main__":
    # Load configuration from file
    config = load_config('config.json')

    survey_url = config['survey_url']
    survey_questions = config['questions']
    answer_amount = config['answer_amount']
    send_button_xpath = config['send_button_xpath']

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("-incognito")
    chrome_options.add_experimental_option("detach", True)

    for answer in range(answer_amount):
        print(f"{answer + 1}/{answer_amount}", f"{(answer + 1 / answer_amount) * 100}%")

        # Create a Chrome WebDriver instance
        browser = webdriver.Chrome(options=chrome_options)

        # Open the survey page
        browser.get(survey_url)

        # Fill out the survey
        fill_survey(survey_questions, send_button_xpath)

        time.sleep(1)
        browser.close()
