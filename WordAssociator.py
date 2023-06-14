import csv
import random
from collections import Counter
import numpy
from numpy.random import rand
from Flashcard import Flashcard
import ErrorMessageBuilder

class WordAssociator:

    def __init__(self, csv_file_name : str):

        self._flashcards = []

        if csv_file_name.endswith('.csv'):

            csv_file_path = f'csv/{csv_file_name}'
            self._flashcards = self.__create_data(csv_file_path)

    def output(self, first_word : str = '') -> list[str]:

        results = []

        if len(first_word) > 0:

            results.append(first_word)

        else:

            words = list(map(lambda card: card.head_word, self._flashcards))
            index = random.randint(0, len(words) - 1)
            results.append(words[index])

        for i in range(100):

            new_word = self.__next_word(results)

            if len(new_word) > 0:
                results.append(new_word)
            else:
                break

        return results

    def __next_word(self, words : list[str]) -> str:

        matched_cards = list(filter(lambda card: card.head_word == words[-1], self._flashcards))

        if len(matched_cards) == 0:

            print(ErrorMessageBuilder.message(
                                                'WordAssociator', \
                                                'next_word', \
                                                'Output Error', \
                                                f'No matched generator for "{words[-1]}".'
                                             ))
            
            return ''
        
        probs = [c.weight for c in matched_cards]
        weight_list = rand(len(matched_cards)) * probs

        return matched_cards[numpy.argmax(weight_list)].tail_word

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
