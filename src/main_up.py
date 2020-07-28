from os import listdir
from os.path import isfile, join
import certificate_handling as ch


def certificate(path, NumThreat):
    pass

if __name__ == '__main__':
    Path = '../certificates'
    Files = [f for f in listdir(Path) if isfile(join(Path, f))]
    
    for File in Files:
        ch.unzip_certificates(File)