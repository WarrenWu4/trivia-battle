import requests
import time
import random

def get_trivia_data(question_num, category, difficulty):
    url = f'https://opentdb.com/api.php?amount={question_num}&category={category}&difficulty={difficulty.lower()}&type=multiple&encode=base64'
    questions, answers, correct_answers = [], [], []
    response = requests.get(url)
    data = response.json()
    while data.get('response_code') == 5:
        time.sleep(5)
        response = requests.get(url)
        data = response.json()
    if data.get('response_code') != 0:
        return None, None, None
    for result in data.get('results'):
        questions.append(result.get('question'))
        answers.append(
            random.choice([result.get('incorrect_answers') + [result.get('correct_answer')]])
        )
        correct_answers.append(result.get('correct_answer'))
    return questions, answers, correct_answers