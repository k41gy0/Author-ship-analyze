import math
import sqlite3
from collections import Counter
import pandas as pd
import nltk
nltk.download('punkt')

con = sqlite3.connect('data.db')
cur = con.cursor()

def Initialization():
    cur.execute('''CREATE TABLE IF NOT EXISTS file (
                name TEXT NOT NULL,
                doc TEXT NOT NULL,
                newname TEXT NOT NULL)''')

def Cleanup():
    con.commit()
    con.close()

def read_corpus(text):
    tokens = nltk.word_tokenize(text)
    return Counter(tokens)

def calculate_expected(O11, O12, O21, O22):
    N = O11 + O12 + O21 + O22
    E11 = (O11 + O21) * (O11 + O12) / N
    E12 = (O12 + O22) * (O11 + O12) / N
    E21 = (O11 + O21) * (O21 + O22) / N
    E22 = (O12 + O22) * (O21 + O22) / N
    return E11, E12, E21, E22

def log_likelihood(O11, O12, O21, O22):
    E11, E12, E21, E22 = calculate_expected(O11, O12, O21, O22)
    # 各頻度が0にならないように調整
    O11 = O11 if O11 != 0 else 0.5
    O12 = O12 if O12 != 0 else 0.5
    O21 = O21 if O21 != 0 else 0.5
    O22 = O22 if O22 != 0 else 0.5
    G2 = 2 * (O11 * math.log(O11 / E11) + O12 * math.log(O12 / E12) + O21 * math.log(O21 / E21) + O22 * math.log(O22 / E22))
    return G2

def odds_ratio(O11, O12, O21, O22):
    O11 = O11 if O11 != 0 else 0.5
    O12 = O12 if O12 != 0 else 0.5
    O21 = O21 if O21 != 0 else 0.5
    O22 = O22 if O22 != 0 else 0.5
    OR = (O11 / O12) / (O21 / O22)
    return OR

def pickup(filename_list): 
    doc = []
    for name in filename_list:
        cur.execute(f"SELECT doc FROM file WHERE new_name = '{name}'")
        to_str = cur.fetchone()[0]
        doc.append(to_str)
    return doc

def display_in_chunks(df, chunk_size):
    num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size != 0 else 0)
    for i in range(num_chunks):
        print(df.iloc[i*chunk_size:(i+1)*chunk_size])
        print("\n" + "="*80 + "\n")
        key = input('If you want swho next 20 word, please enter.\nIf you do not want it, please pless q key: ')
        if(key == 'q'):
            break

def keynessTab():

    names = input('Please input the file name\n>')
    file_name_list = names.split()
    doc = pickup(file_name_list)

    target_file = doc[0]
    reference_file = doc[1]


    target_counts = read_corpus(target_file)
    reference_counts = read_corpus(reference_file)
    
    all_words = set(target_counts.keys()).union(set(reference_counts.keys()))
    
    results = []
    for word in all_words:
        O11 = target_counts.get(word, 0)
        O12 = sum(target_counts.values()) - O11
        O21 = reference_counts.get(word, 0)
        O22 = sum(reference_counts.values()) - O21
        
        G2 = log_likelihood(O11, O12, O21, O22)
        OR = odds_ratio(O11, O12, O21, O22)
        

        results.append((word, G2, OR))
    
    mode = input("Please Input sort mode\n1.Log-Likelihood DEC\n2.Log-likelihood ASC\n3.Odds ration DEC\n4.Odds ration ASC\n: ")

    if(int(mode)==1):
        # 結果を対数尤度比の降順でソート
        results.sort(key=lambda x: x[1], reverse=True)
    elif(int(mode)==2):
        # 結果を対数尤度比の昇順でソート
        results.sort(key=lambda x: x[1], reverse=False)
    elif(int(mode)==3):
        # 結果をオッズ比の降順でソート
        results.sort(key=lambda x: x[2], reverse=True)
    elif(int(mode)==4):
        # 結果をオッズ比の昇順でソート
        results.sort(key=lambda x: x[2], reverse=False)
    
    # 結果を表示
    #for word, G2, OR in results:
        #print(f"Word: {word}, Log-Likelihood: {G2:.2f}, Odds Ratio: {OR:.2f}")
    df = pd.DataFrame(results)
    df = df.rename(columns={0 : 'Word'})
    df = df.rename(columns={1 : 'Log-Likelihood'})
    df = df.rename(columns={2 : 'Odds Ratio'})

    pd.set_option('display.max_rows', None)  # 全ての行を表示
    pd.set_option('display.max_columns', None)  # 全ての列を表示
    pd.set_option('display.max_colwidth', None)  # 列の最大幅を制限なしにする
    pd.set_option('display.expand_frame_repr', False)

    display_in_chunks(df, 20)

if __name__ == "__main__":
    Initialization()
    keynessTab()
    Cleanup()