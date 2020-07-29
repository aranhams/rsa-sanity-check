import gmpy2
import time
import math
import os
import graphic as g


def ffmethod(ModulusFile = '../data/rsa_data_uniq.csv'):
        
    print("[Fermat's factorization method]\n")

    with open(ModulusFile) as f:
        Size = sum(1 for _ in f)

    RSAData = open(ModulusFile, 'r')
    RSADataFac = open('../data/rsa_data_fac.csv', 'a')

    TStart = time.time()
    ax = 0

    g.print_progress_bar(ax, Size, prefix='Progress:', suffix='Complete', length = 50)

    for Module in RSAData:
        n = gmpy2.mpz(Module, base=16)
        a = gmpy2.isqrt(n)+1
        b2 = a*a-n
        count = 0
        while (not(gmpy2.is_square(b2))) & (count <= 100):
            a += 1
            b2 = a*a-n
            count += 1

        b = gmpy2.isqrt(b2)
        if gmpy2.is_square(b2):
            p = a-b
            q = a+b
            RSADataFac.write('%x' %str(n)+","+'%x' %str(p)+","+'%x' %str(q)+"\n")
        ax += 1
        
        g.print_progress_bar(ax, Size, prefix='Progress:', suffix='Complete', length = 50)
    
    TEnd = time.time()
    print("Time used: ", TEnd-TStart)

    RSAData.close()
    RSADataFac.close()


def calc_gcd(ModulusFile = '../data/rsa_data_uniq.csv'):
    
    print("\n[Calculating GCD]")

    Modulus = []
    Size = 0

    with open(ModulusFile, 'r') as f:
        for domain in f:
            Size += 1
            Modulus.append(gmpy2.mpz(domain.strip(), 16))

    compute_gcd(Modulus, Size)


def compute_gcd(Modulus, Size):
        
    TStart = time.time()

    S = []
    for i in range(len(Modulus)):
        S.append(Modulus[i])
    S = Modulus[:]

    T = product_tree(Modulus, Size)

    TempOutput = open('../data/output.csv', 'a')

    k = 0
    Tr = []

    [subfolders] = os.walk('../data/tree')

    h = len(subfolders[2])-1
    height = h-1

    while h >= 0:
        URL = '../data/tree/'+str((h))+'.txt'
        #print(url)
        Tree = open(URL, 'r')
        TLines = Tree.readlines()
        
        if k == 0:
            k += 1
            a = TLines[0].strip().split('\t')

            for i in range(len(a)):
                a[i] = gmpy2.mpz(a[i])

            Tr.append(a)
        else:
            a = TLines[0].strip().split(',')

            for i in range(len(a)):
                a[i] = gmpy2.mpz(a[i])
            Tr.append(a)

            MStart = time.time()  

            print("\n[Merging \t Level %d of %d]" % (k-1,height))
            g.print_progress_bar(0, len(Tr[k]), prefix = 'Progress:', suffix = 'Complete', length = 50)

            for j in range(len(Tr[k])):
                m = int(j/2)
                Tr[k][j] = gmpy2.f_mod(Tr[k-1][m], Tr[k][j]**2)

                g.print_progress_bar(j+1, len(Tr[k]), prefix = 'Progress:', suffix = 'Complete', length = 50)

            MEnd = time.time()
            print("Time used: ", MEnd-MStart)

            del Tr[k-1][:]
            k+=1

        Tree.close()

        os.remove(URL)

        h -= 1
    os.rmdir('../data/tree')

    print("\n[Calculating GCD]")
    g.print_progress_bar(0, len(Tr[len(Tr)-1]), prefix = 'Progress:', suffix = 'Complete', length = 50)  

    for i in range(len(Tr[len(Tr)-1])):
        Tr[len(Tr)-1][i] = gmpy2.f_div(Tr[len(Tr)-1][i], S[i])
        if gmpy2.gcd(Tr[len(Tr)-1][i], S[i]) != 1:
            a = '%x' %str(S[i])
            b = '%x' %str(gmpy2.gcd(Tr[len(Tr)-1][i], S[i]))
            TempOutput.write(a+","+b+"\n")

        g.print_progress_bar(i+1, len(Tr[len(Tr)-1]), prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    TempOutput.close()
    TEnd = time.time()
    print("Time used: ", TEnd-TStart)


def product_tree(Modulus, Size):

    TStart = time.time()

    T = []
    os.mkdir('../data/tree')

    URL = '../data/tree/'+str((0))+'.txt'

    Tree = open(URL,'w')

    for i in range(len(Modulus)):
        a = Modulus[i]    
        Tree.write(str(a)+'\t')
    Tree.write('\n')

    Tree.close() 

    T.append(Modulus)

    print("[Tree height: %i]" % (int(math.ceil(math.log(Size, 2)))-1))
    for i in range(int(math.ceil(math.log(Size, 2)))):
        print("\t[Level %d of %d]" % (int(math.ceil(math.log(Size,2)))-1 - i,int(math.ceil(math.log(Size,2)))-1))
        m = []
        j = 0
        h = 2*int(math.ceil(len(T[i])/2))

        g.print_progress_bar(j, h, prefix = 'Progress:', suffix = 'Complete', length = 50)

        while j < len(T[i]):
            if j + 1 >(len(T[i])-1) :
                m.append(T[i][j])
            else:
                m.append(T[i][j]*T[i][j+1])
            j += 2

            g.print_progress_bar(j, h, prefix = 'Progress:', suffix = 'Complete', length = 50)

        URL = '../data/tree/'+str((i+1))+'.txt'

        Tree = open(URL, 'w')

        for k in range(len(m)):
            a = m[k]    
            Tree.write(str(a)+'\t')
        Tree.write('\n')

        Tree.close()       

        T.append(m)

        del T[i][:]

    
    TEnd = time.time()
    print("Time used (Building the Tree): ", TEnd-TStart)
        
    return T