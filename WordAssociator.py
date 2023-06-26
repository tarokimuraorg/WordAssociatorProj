import copy
import csv
import random
from collections import Counter
import numpy
import ErrorMessageBuilder
from Flashcard import Flashcard

class WordAssociator:

    def __init__(self, csv_file_name : str):

        self._flashcards = []

        if csv_file_name.endswith('.csv'):

            csv_file_path = f'csv/{csv_file_name}'
            self._flashcards = self.__create_data(csv_file_path)

    def output(self, first_word : str = '', number_of_branches: int = 10000) -> list[str]:

        stem = []
        branches = []

        if len(first_word) > 0:

            stem.append(first_word)

        else:

            words = list(map(lambda card: card.head_word, self._flashcards))
            index = random.randint(0, len(words) - 1)
            stem.append(words[index])

        branches.append(stem)

        print('----------------------------------------------------')
        print('-------------the processing was started-------------')
        print('----------------------------------------------------')

        for branch in branches:

            new_words = self.__next_words(branch)

            for new_word in new_words:

                new_branch = list(copy.deepcopy(branch))
                new_branch.append(new_word)
                branches.append(new_branch)

            print(f'now thinking... : {len(branches)}')

            if len(branches) > number_of_branches:
                break

        print('-----------------------------------------------------')
        print('-------------the processing was finished-------------')
        print('-----------------------------------------------------')
        print()

        number_of_elements = list(map(lambda branch: len(branch), branches))

        return branches[numpy.argmax(number_of_elements)]

    def __next_words(self, words : list[str]) -> list[str]:

        matched_cards = list(filter(lambda card: card.head_word == words[-1], self._flashcards))

        return list(map(lambda card: card.tail_word, matched_cards))

    def __create_data(self, csv_file_path : str) -> list[Flashcard]:

        if len(csv_file_path) > 0:

            csv_data = []

            with open(csv_file_path, mode='r', encoding='utf-8', newline='') as f:
                lines = csv.reader(f)

                csv_data = [(line[0], line[1]) for line in lines]

            if len(csv_data) > 0:
                
                dic_data = Counter(csv_data)
                list_data = list(zip(dic_data.keys(), dic_data.values()))

                return list(map(lambda d: Flashcard(d[0][0], d[0][1], d[1]), list_data))

            print(ErrorMessageBuilder.message('CsvReader', 'create_data', 'Input Error', 'cannot read the csv file.'))
            return []

        print(ErrorMessageBuilder.message('CsvReader', 'create_data', 'Value Error', 'csv file extention is .csv'))
        return []
