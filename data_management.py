import sqlite3
import os

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

def Count_K_files():
    cur.execute("SELECT * FROM file WHERE new_name LIKE 'K%'")
    K_files_list = cur.fetchall()
    sum = 0
    for item in K_files_list:
        sum += 1

    return str(sum)

def Create_file(path, types):
	
	if types == 0:
		new_name = 'Q'
	elif types == 1:
		new_name = 'K' + Count_K_files()


	f = open(path)
	doc = f.read()
	f.close()

	name = os.path.basename(path)

	cur.execute('INSERT INTO file (name, doc, new_name) VALUES(?, ?, ?)', (name, doc, new_name))

def Retrieve_file(file_name):
    if file_name != "*":
        cur.execute(f"SELECT * FROM file WHERE name = '{file_name}'")
    else:
        cur.execute("SELECT * FROM file")

    row = cur.fetchall()
    for item in row:
        print(item)

def Update_file(types, which_file_changed, new_filename):
    if types == 0:
        cur.execute(f"UPDATE file SET name = '{new_filename}' WHERE name = '{which_file_changed}'")
    elif types == 1:
        cur.execute(f"UPDATE file SET new_name = '{new_filename}' WHERE name = '{which_file_changed}'")
    print(which_file_changed + " -> " + new_filename)

    con.commit()


def Delete_file(file_name):
     cur.execute("DELETE FROM file WHERE name = ?", (file_name,))
     print('Success!')
  

def main():
    try:
        while True:
            mode = input("1.Create files\n2.Retrieve files\n3.Update files\n4.Delete files\n5.Exit\n")
            if int(mode) == 1:
                print('Create files\n')
                types = input('Please input the file type\nQuestioned document 0: \nKnown document 1: \n')
                path = input('Input file path\n')
                Create_file(path, int(types)) 
            
            elif int(mode) == 2:
                file_name = input("Please input file name\n*** all files will be displayed if input -> *\n")
                Retrieve_file(file_name)
            elif int(mode) == 3:
                types = input("Please input the type\noriginal file name 0:\nnew file name 1:\n")
                print("\n\n")
                cur.execute("SELECT * FROM file")
                list = cur.fetchall()
                for item in list:
                    print(item)

                which_file_changed = input("Please input the filename you wanna change\n ->")
                new_filename = input("Please input new file name\n-> ")
                Update_file(types, which_file_changed, new_filename)
            elif int(mode) == 4:
                 file_name = input("Please input file name that you want to delete\n")
                 Delete_file(file_name)

            elif int(mode) == 5:
                 print('Exit\n')
                 break
            else:
                 print('Invalid Input!\n')

            print("\n\n")
        
    except KeyboardInterrupt:
        Cleanup()

if __name__ == "__main__":
	Initialization()
	main()
	Cleanup()