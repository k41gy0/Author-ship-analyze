import sqlite3
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
        print("<"+row[i][1]+">",end="")
        print(" "*(empty-1),end="")
    print()
    
    
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
        TextData = [[] for i in range(number_row)]
        
        i = -1
        for text_file in row:
            i += 1   #index for TextData[i]
            pre_list_word_list = text_file[0].split()
            word_list = set(text_file[0].split())
            for word in word_list:
                word_count = searchWord(word,pre_list_word_list)
                TextData[i].append(WordCount(word=word,count=word_count))
                
        for data in TextData: #sort focus on word count
            data.sort(key=lambda x: x.count,reverse=True)
        
        max_cols = []
        for word_list in TextData: #calc for table
            max_cols.append(get_max_col(word_list))
            
        display_header(TextData,max_cols,row)
        
        min_range = 100000
        for item in TextData:
            L = len(item)
            if L < min_range:
                min_range = L
                
        for display_number in range(min_range):
            print("|",end="")
            for i in range(len(TextData)):
                print(TextData[i][display_number].word,end="")
                number_empty = max_cols[i] - len(TextData[i][display_number].word)-len(str(TextData[i][display_number].count))
                print(" " * number_empty ,end="")
                print(str(TextData[i][display_number].count)+ " | ",end="")
            print()
            if (display_number+1)%20 == 0:
                enter = input("Please enter to continue.\nenter \"q\" if not continue\n>")
                if enter != "q":
                    display_header(TextData,max_cols,row)
                else:
                    break
            
    
    
    except KeyboardInterrupt:
        print("Exit")
            
    
if __name__ == '__main__':
    Initialization()
    comparisonTab()
    Cleanup()