import data_management
import search
import comparison
import consistency
import keyness

def main():
    while True:
        mode = input("1.regist dataset\n2.search word token\n3.comparison\n4.consistency\n5.keyness\n6.Exit\nPlease Input your choice number: ")
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
        elif(int(mode) == 4):
            consistency.Initialization()
            consistency.consistency()
            consistency.Cleanup()
        elif(int(mode) == 5):
            keyness.Initialization()
            keyness.keynessTab()
            keyness.Cleanup()
        else:
            break

if __name__ == '__main__':
    main()
