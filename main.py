import os
import re
import iso639

Alpha = 0.5

list_directories_languages = os.listdir()
list_directories_languages.remove("venv")
list_directories_languages.remove(".idea")

for item in list_directories_languages:
    if item.endswith(".py"):
        list_directories_languages.remove(item)


def create_weight_vector():
    weight_vector = []
    i = 0
    while i < 26:
        i += 1
        weight_vector.append(0.1)
    return weight_vector


dict_lang_percept = {}


def create_perceptrons():
    global dict_lang_percept
    theta = 0.1
    for language in list_directories_languages:
        dict_lang_percept[language] = [create_weight_vector(), theta]


create_perceptrons()


def delta_rule(array_letters_by_all, language):
    global dict_lang_percept
    dict_dir_answer = {}
    for directory in list_directories_languages:
        answer = 0
        w = dict_lang_percept[directory][0]
        theta = dict_lang_percept[directory][1]
        for i in range(len(array_letters_by_all)):
            answer += array_letters_by_all[i]*w[i]
        answer -= theta

        dict_dir_answer[directory] = answer
    max_key_item = max(dict_dir_answer, key=dict_dir_answer.get)

    for directory in list_directories_languages:
        if directory == language:
            d = 1
        else:
            d = 0

        y = function_y(max_key_item)[directory]
        w = dict_lang_percept[directory][0]

        for index_w_to_change in range(len(w)):
            w[index_w_to_change] = w[index_w_to_change]+(d-y)*Alpha*array_letters_by_all[index_w_to_change]
        dict_lang_percept[directory][0] = w
        theta = dict_lang_percept[directory][1]+(d-y)*Alpha*(-1)
        dict_lang_percept[directory][1] = theta


def get_answer(array_letters_by_all):
    global dict_lang_percept
    array_answers_to_compare = {}

    for directory in list_directories_languages:
        net = 0
        w = dict_lang_percept[directory][0]
        theta = dict_lang_percept[directory][1]
        for i in range(len(array_letters_by_all)):
            net += w[i]*array_letters_by_all[i]
        net -= theta

        array_answers_to_compare[directory] = net
    answer = max(array_answers_to_compare, key=array_answers_to_compare.get)
    language = iso639.to_name(answer)
    return language


def function_y(max_language):

    global list_directories_languages
    dict_lang_y = {}

    for language in list_directories_languages:
        if max_language == language:
            dict_lang_y[language] = 1
        else:
            dict_lang_y[language] = 0
    return dict_lang_y


def read_from_dir_languages():
    global list_directories_languages

    for directory in list_directories_languages:
        language_files = os.listdir(directory)

        for file in language_files:
            path = directory+"/"+file
            with open(path, "r") as file_text:
                lines = file_text.read()
                cleaned_text = re.sub(r"[^a-zA-Z]", "", lines).lower()
                array_letters_by_all = []
                i = 0
                while i < 26:
                    array_letters_by_all.append(0)
                    i += 1
                for char in cleaned_text:
                    ascii_code_letter = ord(char)-97
                    if 0 <= ascii_code_letter < 26:
                        array_letters_by_all[ord(char)-97] += 1

                for charNumber in range(len(array_letters_by_all)):
                    array_letters_by_all[charNumber] = array_letters_by_all[charNumber]/len(cleaned_text)
                delta_rule(array_letters_by_all, directory)


for i in range(500):
    read_from_dir_languages()


def work_with_text():
    test_from_user = input("Provide the text to classify the language")
    cleaned_text = re.sub(r"[^a-zA-Z]", "", test_from_user).lower()
    array_letters_by_all = []
    i = 0
    while i < 26:
        array_letters_by_all.append(0)
        i += 1
    for char in cleaned_text:
        ascii_code_letter = ord(char) - 97
        if 0 <= ascii_code_letter < 26:
            array_letters_by_all[ord(char) - 97] += 1

    for charNumber in range(len(array_letters_by_all)):
        array_letters_by_all[charNumber] = array_letters_by_all[charNumber] / len(cleaned_text)

    answer = get_answer(array_letters_by_all)

    print(f"The language is {answer}")


work_with_text()
