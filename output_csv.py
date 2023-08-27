from CsvCreator import CsvCreator

if CsvCreator('wagahaiwa_nekodearu_3.txt').output_data('wagahaiwa_nekodearu_3.csv'):
    print('正常に出力されました。')
else:
    print('出力に失敗しました。')
