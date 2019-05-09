import os, sys,time, math, ssl, traceback, gmpy2
from asn1crypto.x509 import Certificate
from gmpy2 import mpz, gcd
from OpenSSL import crypto

class CertificateSanityCheck:

    def __init__(self, domains,lock=0, database=False):
        self.domains = domains
        self.lock = lock
        self.database = database
    
    # Print iterations progress
    def printProgressBar(self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()
    
    def get_cert_info(self,cert,cert_file_name='cert.der'):

        cert = "-----BEGIN CERTIFICATE-----\n"+cert+"-----END CERTIFICATE-----\n"
        #print(cert)
        f = open(str(cert_file_name), 'wb')
        try:
            certificate1 = crypto.load_certificate(crypto.FILETYPE_PEM, cert.encode())
        except:
            certificate1 = 'none'

        try:
            has_expired = certificate1.has_expired()
        except:
            has_expired = 'none'
        
        f.write(ssl.PEM_cert_to_DER_cert(cert))
        f.close()
        
        with open(str(cert_file_name), "rb") as f:
            certificate = Certificate.load(f.read())          

        
        algorithm  = certificate.public_key.native["algorithm"]["algorithm"]
        if algorithm == 'rsa' :
            curve      = 'none' # apenas para EC 
            public_key = 0 # apenas para EC
            modulus    = certificate.public_key.native["public_key"]["modulus"]
            pub_exp    = certificate.public_key.native["public_key"]["public_exponent"]
            key_size   = int(certificate.public_key.bit_size)

        elif algorithm == 'ec' :
            curve      = certificate.public_key.native["algorithm"]["parameters"]
            public_key = certificate.public_key.native["public_key"].hex()
            modulus    = 0
            pub_exp    = 0
            key_size   = int(certificate.public_key.bit_size)
        else:
            try:
                curve      = certificate.public_key.native["algorithm"]["parameters"]
            except:
                cert_issuer_country = 'none'
            try:
                public_key = certificate.public_key.native["public_key"].hex()
            except:
                public_key = 'none'
            try:
                modulus    = certificate.public_key.native["public_key"]["modulus"]
            except:
                modulus    = 0
            try:
                pub_exp    = certificate.public_key.native["public_key"]["public_exponent"]
            except:
                pub_exp    = 0
            try:
                key_size   = int(certificate.public_key.bit_size)
            except:
                key_size   = 0 

        try:
            cert_issuer_country = certificate.issuer.native["country_name"]
        except:
            cert_issuer_country = "Empty"
        try:
            cert_issuer_name = certificate.issuer.native["organization_name"]
        except:
            cert_issuer_name = "Empty"
        try:
            cert_issuer_common_name = certificate.issuer.native["common_name"]
        except:
            cert_issuer_common_name = "Empty"
        sig_algorithm = certificate.signature_algo
        self_signed = certificate.self_signed
        hash_algo = certificate.hash_algo
        domains = certificate.valid_domains
        not_valid_before = certificate.native['tbs_certificate']['validity']['not_before']
        not_valid_after  = certificate.native['tbs_certificate']['validity']['not_after']
        
        os.remove(str(cert_file_name))
        return('{0:02x}'.format(modulus), pub_exp, algorithm,curve,public_key,key_size,
               not_valid_before,not_valid_after,has_expired,sig_algorithm,cert_issuer_country, 
               cert_issuer_name, cert_issuer_common_name,self_signed, hash_algo, domains)

    def process_cert(self):
        
        data_file = open('./complete_output.txt', 'a')
        modulus_file = open('./modulus_file.txt', 'a')
        ec_public_key_file = open('./ec_public_key_file.txt', 'a')
        log_file = open('./log.txt', 'a')
        size = len(self.domains)
        for domain in self.domains:
            try:
                print('Process PID: %s - %d of %d\n\
                    Domain: %s' % (os.getpid(), size, len(self.domains), domain[0]))
                cert = self.get_cert_info(domain[1])

                self.lock.acquire()
                if cert[2] == 'rsa':
                    data_file.write(str(domain[0])+'\t'+str(cert[0])+'\t'+str(cert[1])
                                    + '\t'+str(cert[2])+'\t' +
                                    str(cert[5])+'\t'+                                    
                                    str(cert[6])+'\t'+str(cert[7])
                                    + '\t'+str(cert[8])+'\t' +
                                    str(cert[9])+'\t'+str(cert[10])
                                    + '\t'+str(cert[11])+'\t'+
                                    str(cert[12])+'\t'+str(cert[13])
                                    +'\t'+str(cert[14])+'\t'+str(cert[15])+'\n')
                                            
                    modulus_file.write(str(cert[0])+'\n')
                if cert[2] == 'ec':
                    data_file.write(str(domain[0])+'\t'+str(cert[3])+'\t'+str(cert[4])
                                    + '\t'+str(cert[2])+'\t' +
                                    str(cert[5])+'\t'+
                                    str(cert[6])+'\t'+str(cert[7])
                                    + '\t'+str(cert[8])+'\t' +
                                    str(cert[9])+'\t'+str(cert[10])
                                    + '\t'+str(cert[11])+'\t'+
                                    str(cert[12])+'\t'+str(cert[13])
                                    +'\t'+str(cert[14])+'\t'+str(cert[15])+'\n')
                    
                    ec_public_key_file.write(str(cert[4])+'\n')  
                self.lock.release()
                size -= 1
            except Exception:
                error = traceback.format_exc()
                linesoferror = error.split('\n')
                log_file.write('[ERROR] -  to obtain the certificate \n\
                                Domain: %s\n\
                                Type of error: %s\n' % (domain[0], linesoferror[-2])
                               )
                size -= 1
                continue
        
        data_file.close()
        modulus_file.close()
        log_file.close()
        ec_public_key_file.close()
        
    def verify_modulus(self, modulus_file='./modulus.txt'):
        with open(modulus_file) as f:
            size = sum(1 for _ in f)

        f = open(modulus_file, 'r')
        out = open('./output.txt', 'a')

        count = 1
        line = f.readline()
        while line:
            a = mpz(line, base=16)
            pos = f.tell()
            line2 = f.readline()
            while line2:
                b = mpz(line2, base=16)
                if gcd(a,b)>1:
                    print(a,b)
                    out.write(str(a)+","+str(b)+"\n")
                line2 = f.readline()

            f.seek(pos)
            line = f.readline()
            print("%d of %d" % (count, size))
            count += 1

        f.close()
        out.close()


    def ffmethod(self, modulus_file='./modulus.txt'):
        print("\n\n\n\t\t   Fermat's factorization method\n\n")

        with open(modulus_file) as f:
            size = sum(1 for _ in f)
        print("Number of Moduli: %d \n\n" % size)
        f = open(modulus_file, 'r')
        out = open('./modulus_fac.txt', 'a')
        start_t = time.time()
        i = 0
        self.printProgressBar(i, size, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for module in f:
            n = mpz(module, base=16)
            a = gmpy2.isqrt(n)+1
            b2 = a*a - n
            count = 0
            while (not(gmpy2.is_square(b2))) & (count <= 100):
                a = a+1
                b2 = a*a - n
                count +=1

            b = gmpy2.isqrt(b2)
            if gmpy2.is_square(b2):
                p = a-b
                q = a+b
                out.write('%x' %str(n)+"\t"+'%x' %str(p)+"\t"+'%x' %str(q)+"\n")
            i+=1
            self.printProgressBar(i, size, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        end_t= time.time()
        print("Time used: ",end_t - start_t)
        f.close()
        out.close()

    
    def productTree(self,modulus,size):
        T = []
        start_t = time.time()
        os.mkdir('Tree')
        url = './Tree/'+str((0))+'.txt'
        Tree = open(url,'w')
        for i in range(len(modulus)):
            a = modulus[i]    
            Tree.write(str(a)+'\t')
        Tree.write('\n')
        Tree.close() 
        T.append(modulus)

        print("Tree height: %i \n\n" % (int(math.ceil(math.log(size,2)))-1))
        for i in range(int(math.ceil(math.log(size,2)))):
            print("\t\t\t   Level %d of %d"%(int(math.ceil(math.log(size,2)))-1 - i,int(math.ceil(math.log(size,2)))-1))
            m = []
            j = 0
            h = 2*int(math.ceil(len(T[i])/2))
            self.printProgressBar(j, h, prefix = 'Progress:', suffix = 'Complete', length = 50)
            while j < len(T[i]):
                if j + 1 >(len(T[i])-1) :
                    m.append(T[i][j])
                else:
                    m.append(T[i][j]*T[i][j+1])
                j += 2
                self.printProgressBar(j , h, prefix = 'Progress:', suffix = 'Complete', length = 50)
            url = './Tree/'+str((i+1))+'.txt'
            Tree = open(url,'w')
            for k in range(len(m)):
                a = m[k]    
                Tree.write(str(a)+'\t')
            Tree.write('\n')
            Tree.close()       
            T.append(m)
            del T[i][:]

        
        end_t= time.time()
        print("Time used (Building the Tree): ",end_t - start_t)
            
        return T

    def computeGCDs(self,modulus,size):
        
        start_t = time.time()
        S = []
        for i in range(len(modulus)):
            S.append(modulus[i])
        S = modulus[:]
        T = self.productTree(modulus,size)
        out = open('./output.txt', 'a')
        k = 0
        Tr = []
        [subfolders] = os.walk('./Tree')
        h = len(subfolders[2])-1
        height = h - 1
        while h >=0:
            url = './Tree/'+str((h))+'.txt'
            #print(url)
            Tree = open(url,'r')
            T_lines = Tree.readlines()
            
            if k == 0:
                k +=1
                a = T_lines[0].strip().split('\t')
                for i in range(len(a)):
                    a[i] = mpz(a[i])
                Tr.append(a)
            else:
                a = T_lines[0].strip().split('\t')
                for i in range(len(a)):
                    a[i] = mpz(a[i])
                Tr.append(a)
                start_m = time.time()
                
                print("\nMerging... \t\t   Level %d of %d"%(k-1,height))
                self.printProgressBar(0, len(Tr[k]), prefix = 'Progress:', suffix = 'Complete', length = 50)
                for j in range(len(Tr[k])):
                    m = int(j/2)
                    Tr[k][j]        =  gmpy2.f_mod(Tr[k-1][m],Tr[k][j]**2)
                    self.printProgressBar(j+1, len(Tr[k]), prefix = 'Progress:', suffix = 'Complete', length = 50)
                end_m= time.time()
                print("Time used: ",end_m - start_m)
                del Tr[k-1][:]
                k+=1
            Tree.close()
            os.remove(url)
            h-=1
        os.rmdir('Tree')
        #print(str(len(Tr))+"\n")
        print("\n\t\t\t   Calculating GCD\n")
        self.printProgressBar(0, len(Tr[len(Tr)-1]), prefix = 'Progress:', suffix = 'Complete', length = 50)       
        for i in range(len(Tr[len(Tr)-1])):
            Tr[len(Tr)-1][i] = gmpy2.f_div(Tr[len(Tr)-1][i],S[i])
            if gcd(Tr[len(Tr)-1][i],S[i]) != 1:
                a = '%x' %str(S[i])
                b = '%x' %str(gcd(Tr[len(Tr)-1][i],S[i]))
                out.write(a+","+b+"\n")
            self.printProgressBar(i+1, len(Tr[len(Tr)-1]), prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        out.close()
        end_t= time.time()
        print("Time used: ",end_t - start_t)

    def calc_gcd(self, modulus_file='./modulus.txt'):
        print("\n\n\n\t\t\t   Calculating GCD's\n\n")
        modulus = []
        size = 0
        with open(modulus_file) as f:
            for domain in f:
                size += 1
                modulus.append(mpz(domain.strip(),16))
        self.computeGCDs(modulus,size)