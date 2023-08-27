from WordAssociator import WordAssociator

if __name__ == "__main__":

    results = WordAssociator('wagahaiwa_nekodearu.csv').output()

    for result in results:
        print(result)
