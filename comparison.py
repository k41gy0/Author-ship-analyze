import sqlite3
import pandas as pd
from dataclasses import dataclass

@dataclass
class WordCount:
    word: str
    count: int

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

def searchWord(word,list):
    count = 0
    for i in list:
        if i == word:
            count += 1
            
    return count

def get_max_col(word_list):
    max = 0
    count = 0
    for item in word_list:
        length = len(item.word) + len(str(item.count)) + 1
        if length > max:
            max = length
        count += 1
        if count >= 200:
            return max
    
    return max

def display_header(TextData,max_cols,row):
    for i in range(len(TextData)):
        empty = int(max_cols[i]/2)
        print(" "*empty,end="")
        print("<"+TextData[i][1]+">",end="")
        print(" "*(empty-1),end="")
    print()
    
    # return list type
def make_Q_list(text_file): # taple -> list -> set
    Q_list = []
    text = text_file[0].split() #list
    words = set(text)    #set
    
    for word in words:
        count = count_word(text,word)
        Q_list.append(WordCount(word=word,count=count))
        
    Q_list.sort(key=lambda x: x.count,reverse=True)
    return (Q_list, "Q")

def count_word(data_file,word):
    count = 0
    for item in data_file:
        if word == item:
            count += 1
    return count
     
def has_Q(row):
    for name in row:
        if name[1] == 'Q':
            return name
    return False

def isQ_text(text):
    if text[1] == "Q":
        return True
    else:
        return False
    
def make_Kn_list(Q_list, text):
    Kn = []
    word_list_Kn = text[0].split()
    name_Kn = text[1]
    for item in Q_list:
        word = item.word
        count = count_word(word_list_Kn,word)
        Kn.append(WordCount(word=word,count=count))
    return (Kn,name_Kn)

def make_dataFrame(TextData):
    data = {}
    for file in TextData:
        array = []
        counts = [wc.count for wc in file[0]]
        words = [wc.word for wc in file[0]]
        for i in range(len(counts)):
            if counts[i] == 0:
                counts[i] = "-"
           
        array.append(words)
        array.append(counts)
        if file[1] == "Q":
            data[file[1]] = words
        else:
            data[file[1]] = counts
        
    return data    
    
    
def comparisonTab():    
    try:
        print("\n")
        print("There are some files for comparison.\n")
        cur.execute("SELECT name,new_name FROM file")
        row  = cur.fetchall()
        
        for item in row:
            print(item)
            
        cur.execute("SELECT doc, new_name FROM file")
        row = cur.fetchall()
        number_row = len(row)
        TextData = []
        
        Q_list = has_Q(row)
        if Q_list == False: #there is no Q 
            print("!!! There is no Q file !!!\nPlease create Q file!!\n>")
            return False
        
        Q_list = make_Q_list(Q_list)
        TextData.append(Q_list)
     #TextData[Q~Kn][]
        
        #compute how much each text_file has specific word.
        for text in row:
            if isQ_text(text) == False:
                TextData.append(make_Kn_list(Q_list[0], text))
        #print(TextData[0][1][0],TextData[1][1],TextData[2][1])
        
        df = make_dataFrame(TextData)
        df = pd.DataFrame(df)
        for i in range(0, len(df), 20):
            print(df.iloc[i:i+20])
            print("=============================================================")
            x = input("Please enter to continue.\nIf not continue input \"q\".\n>")
            if x == "q":
                break
            print("=============================================================")

    
    
    except KeyboardInterrupt:
        print("Exit")
            
    
if __name__ == '__main__':
    Initialization()
    comparisonTab()
    Cleanup()