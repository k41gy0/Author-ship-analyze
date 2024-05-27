import sqlite3
from collections import Counter
import pandas as pd


con = sqlite3.connect('data.db')
cur = con.cursor()


def Initialization():
    cur.execute('''CREATE TABLE IF NOT EXISTS file (
                name TEXT NOT NULL,
                doc TEXT NOT NULL,
                new_name TEXT NOT NULL)''')
    
def Cleanup():
    con.commit()
    con.close()

def AllVocabularyList(docs):
    word_frequencies = [Counter(text.split()) for text in docs]
    all_words = set(word_frequencies[0].keys())
    for wf in word_frequencies[1:]:
        all_words.update(wf.keys())
    word_occurrences = {word: [wf[word] for wf in word_frequencies] for word in all_words}
    sorted_word_occurrences = sorted(word_occurrences.items(), key=lambda x: (-sum(x[1])))
    return sorted_word_occurrences

def create_comparison_table(sorted_word_occurrences, filenames):
    data = {'Word': [item[0] for item in sorted_word_occurrences]}
    for i, label in enumerate(filenames):
        data[label] = [item[1][i] if item[1][i] > 0 else '-' for item in sorted_word_occurrences]

    df = pd.DataFrame(data)
    return df

def display_in_chunks(df, chunk_size):
    num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size != 0 else 0)
    for i in range(num_chunks):
        print(df.iloc[i*chunk_size:(i+1)*chunk_size])
        print("\n" + "="*80 + "\n")
        key = input('If you want swho next 20 word, please enter.\nIf you do not want it, please pless q key: ')
        if(key == 'q'):
            break


def consistency():
    print("\n")
    print("There are some files for consistency.\n")
    cur.execute("SELECT name,new_name FROM file")
    row  = cur.fetchall()
    
    for item in row:
        print(item)

    cur.execute("SELECT new_name,doc FROM file")
    row  = cur.fetchall()

    filenames = []
    docs = []

    for name, doc in row:
        filenames.append(name)
        docs.append(doc)

    print('all text word list')
    WordList = AllVocabularyList(docs)

    print('consistency all files!\n')
    table = create_comparison_table(WordList, filenames)

    pd.set_option('display.max_rows', None)  # 全ての行を表示
    pd.set_option('display.max_columns', None)  # 全ての列を表示
    pd.set_option('display.max_colwidth', None)  # 列の最大幅を制限なしにする
    pd.set_option('display.expand_frame_repr', False)

    display_in_chunks(table, 20)

    






if __name__ == '__main__':
    Initialization()
    consistency()
    Cleanup()
