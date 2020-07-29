from os import listdir, system
from os.path import isfile, join
import certificate_handling as ch


def menu():
    
    print("[1] - Process certificate data\n[2] -  Calculate the GCD between moduli")
    Option = input("Select an option: ")

    return Option


if __name__ == '__main__':

    Option = menu()

    if (Option == '1'):
        print("Processing the certificate data, wait a minute.")

        Path = '../certificates'
        Files = [f for f in listdir(Path) if isfile(join(Path, f))]
        
        for File in Files:
            ch.unzip_certificates(File)

        print("Sorting and removing duplicate items...\nThis process may take some time.")
        system("sort ../data/rsa_data.csv | uniq -u > ../data/rsa_data_uniq.csv")
        system("sort ../data/ec_data.csv | uniq -u > ../data/ec_data_uniq.csv")
        print("Done")
    elif (Option == '2'):
        pass
    else:
        print("Invalid option")