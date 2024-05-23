import sqlite3

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

def pickup(filename_list): 
    doc = []
    for name in filename_list:
        cur.execute(f"SELECT doc FROM file WHERE name = '{name}'")
        to_str = cur.fetchone()[0]
        doc.append(to_str)
    return doc

def presentation(i, word_list):
    x = i - 10
    if x < 0:
        x = 0
    y = i + 10
    if y > len(word_list):
        y = len(word_list) - 1    
    if i > 0:
       i =  i - 1
    word_list = word_list.split()
    word_list[i] = " \" " + word_list[i] + " \" "
    word_list_new = word_list[x:y]
    word_list_new = "  ".join(word_list_new)
    print(word_list_new)

def count_token(doc):
    key_word = input('Please Input key word\n>')
    for item in doc:
        counter = 0
        word = item.split()
        for i in word:
            counter +=1
            if i.lower().replace(",","") == key_word.lower():
                presentation(counter, item)

def searchTab():
    print("\n")
    cur.execute("SELECT * FROM file")

    row = cur.fetchall()
    for item in row:
        print(item)

    names = input('Please input the file name\n>')
    file_name_list = names.split()
    doc = pickup(file_name_list)
    count_token(doc)

if __name__ == '__main__':
    Initialization()
    searchTab()
    Cleanup() 

#task2へメッセージを送信
