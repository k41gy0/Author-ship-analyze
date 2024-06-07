import sqlite3

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

def pickup(filename_list): 
    doc = []
    for name in filename_list:
        cur.execute(f"SELECT doc FROM file WHERE new_name = '{name}'")
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
    word_list[i] = word_list[i]
    word_list_new = word_list[x:y]
    word_list_new = "  ".join(word_list_new)
    return word_list_new
    
    
def calc_max_col(detected_file,keyword):
    max = 0
    for text in detected_file:
        left_text = text.lower().split(keyword.lower())[0]
        if max < len(left_text):
            max = len(left_text)
    
    return max

def get_left_len(text,keyword):
    return len(text.lower().split(keyword.lower())[0])

def count_token(doc):
    key_word = input('Please Input key word\n>')
    detected_file = []
    for item in doc:
        counter = 0
        word = item.split()
        for i in word:
            counter +=1
            if i.lower().replace(",","") == key_word.lower():
                detected_file.append(presentation(counter, item))
    max_col = calc_max_col(detected_file,key_word)
    for item in detected_file:
        length = get_left_len(item,key_word)
        print(" "*int(max_col-length),end="")
        print(item)

def searchTab():
    print("\n")
    cur.execute("SELECT name,new_name FROM file")
    row = cur.fetchall()
    for item in row:
        print(item)

    names = input('Please input Q or K_n\n>')
    file_name_list = names.split()
    doc = pickup(file_name_list)
    count_token(doc)

if __name__ == '__main__':
    Initialization()
    searchTab()
    Cleanup()