import time, math
import os, sys
import numpy as np
from multiprocessing import Process, Lock
import cert_information as ci


dir  = "./"+sys.argv[1].strip()
[subfolders] = os.walk(dir)

start = time.time()
for file in subfolders[2]:
    domains = []
    lock = Lock()
    p = 10   # Number of threads
    arq = open(dir+'/'+file, "r")
    for domain in arq:
        domains.append(domain.split(","))
    arq.close()
    if len(domains) > 0:
        n = int(math.ceil(len(domains)/p))
        Domains = [domains[i * n:(i + 1) * n] for i in range((len(domains) + n - 1) // n )]
        domains.clear()
        for i in range(len(Domains)):
            ts = ci.CertificateSanityCheck(Domains[i], lock)
            Process(target=ts.process_cert(), args=(lock,Domains[i],)).start()
            
print('Sorting and removing duplicate items...\nThis process may take some time.')
os.system("sort modulus_file.txt | uniq -u > modulus.txt")
os.system("sort ec_public_key_file.txt | uniq -u > ec_public_key.txt")

end = time.time()
print("Time used: ",end - start)

ts.ffmethod()
ts.calc_gcd()
