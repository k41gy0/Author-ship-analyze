import data_management
import search

def main():
    mode = input("1.regist dataset\n2.search word token\nPlease Input your choice number: ")
    if(int(mode) == 1):
        data_management.Initialization()
        data_management.datamanagement()
        data_management.Cleanup()
    elif(int(mode) == 2):
        search.Initialization()
        search.searchTab()
        search.Cleanup()
    

if __name__ == '__main__':
    main()
