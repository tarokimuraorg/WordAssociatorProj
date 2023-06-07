import os
import csv
import re
import MeCab
import ErrorMessageBuilder

class CsvCreator:

    def __init__(self, text_file_name: str):

        os.makedirs('text', exist_ok=True)
        os.makedirs('csv', exist_ok=True)

        self._text_file_path = ''

        if text_file_name.endswith('.txt'):
            self._text_file_path = f'text/{text_file_name}'

    def output_data(self, csv_file_name: str) -> bool:

        if csv_file_name.endswith('.csv'):

            csv_file_path = f'csv/{csv_file_name}'
            data = self.__input_data()

            if len(data) > 0:
                
                with open(csv_file_path, mode='w', encoding='utf-8') as f:
                    
                    writer = csv.writer(f)
                    writer.writerows(data)
                
                return True
            
            print(ErrorMessageBuilder.message('CsvCreator', 'output_data', 'Input Error', 'the text file has no useful data.'))
            return False
        
        print(ErrorMessageBuilder.message('CsvCreator', 'output_data', 'Value Error', 'csv file extention is .csv'))
        
    def __input_data(self):

        if len(self._text_file_path) > 0:

            with open(self._text_file_path, mode='r', encoding='utf-8') as f:
                text = f.read()

            if len(text) > 0:

                # 前処理
                text = text.replace('｜', '')
                text = re.sub('《.+?》', '', text)
                text = re.sub('［＃.+?］', '', text)
                text = text.replace('　', '')
                text = re.sub('。|「|」', '\n', text)

                sentences = text.splitlines()
                sentences = filter(lambda line: len(line) > 0 and \
                                                    not('※' in line) and \
                                                    not('○' in line) and \
                                                    not('―' in line), sentences)
                
                data = []

                # 形態素解析
                m = MeCab.Tagger("-Ochasen")

                for sentence in sentences:
                    
                    nouns = [line.split()[0] for line in m.parse(sentence).splitlines() if "名詞" in line.split()[-1]]

                    if len(nouns) > 1:

                        pairs = []

                        for cnt in range(len(nouns)):

                            if len(nouns) > cnt + 2:
                                pairs = [nouns[cnt], nouns[cnt+1]]
                                data.append(pairs)

                return data

            print(ErrorMessageBuilder.message('CsvCreator', 'input_data', 'Input Error', 'cannot read the text file.'))
            return []

        print(ErrorMessageBuilder.message('CsvCreator', 'input_data', 'Value Error', 'text file extention is .txt'))
        return []
