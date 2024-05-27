import data_management
import search
import comparison

def main():
    while True:
        mode = input("1.regist dataset\n2.search word token\n3.comparison\n4.consistency\nPlease Input your choice number: ")
        if(int(mode) == 1):
            data_management.Initialization()
            data_management.datamanagement()
            data_management.Cleanup()
        elif(int(mode) == 2):
            search.Initialization()
            search.searchTab()
            search.Cleanup()
        elif(int(mode) == 3):
            comparison.Initialization()
            comparison.comparisonTab()
            comparison.Cleanup()
    

if __name__ == '__main__':
    main()
