import ssl
import os
import traceback
from asn1crypto.x509 import Certificate
from gmpy2 import mpz, gcd

class CertificateSanityCheck:

    def __init__(self, domains, lock=0, database=False):
        self.domains = domains
        self.lock = lock
        self.database = database

    def get_cert_info(self, hostname, port=443, cert_file_name='cert.der'):

        f = open(str(cert_file_name), 'wb')
        certificate = ssl.get_server_certificate((hostname, port))
        f.write(ssl.PEM_cert_to_DER_cert(certificate))

        with open(str(cert_file_name), "rb") as f:
            certificate = Certificate.load(f.read())

        modulus = certificate.public_key.native["public_key"]["modulus"]
        pub_exp = certificate.public_key.native["public_key"]["public_exponent"]
        sig_algorithm = certificate.signature_algo
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
        self_signed = certificate.self_signed
        hash_algo = certificate.hash_algo
        domains = certificate.valid_domains

        return('{0:02x}'.format(modulus), pub_exp, sig_algorithm,
               cert_issuer_country, cert_issuer_name, cert_issuer_common_name,
               self_signed, hash_algo, domains)

    def process_cert(self):

        data_file = open('./complete_output.txt', 'a')
        modulus_file = open('./modulus_file.txt', 'a')
        log_file = open('./log.txt', 'a')
        size = len(self.domains)

        for domain in self.domains:
            try:
                print('Process PID: %s - %d of %d\n\
                    Domain: %s' % (os.getpid(), size, len(self.domains), domain))
                cert = self.get_cert_info(domain)

                data_file.write(str(domain)+'\t'+str(cert[0])+'\t'+str(cert[1])
                                + '\t'+str(cert[2])+'\t' +
                                str(cert[3])+'\t'+str(cert[4])
                                + '\t'+str(cert[5])+'\t' +
                                str(cert[6])+'\t'+str(cert[7])
                                + '\t'+str(cert[8])+'\n')
                modulus_file.write(str(cert[0])+'\n')
                size -= 1
            except Exception:
                error = traceback.format_exc()
                linesoferror = error.split('\n')
                log_file.write('[ERROR] -  to obtain the certificate \n\
                                Domain: %s\n\
                                Type of error: %s\n' % (domain, linesoferror[-2])
                               )
                size -= 1
                continue
        
        data_file.close()
        modulus_file.close()
        log_file.close()

        print('Sorting and removing duplicate items...\nThis process may take some time.')
        os.system("sort modulus_file.txt | uniq -u > modulus.txt")

    def verify_modulus(self, modulus_file='./modulus_file.txt'):

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
                line2 = f.readline()

            f.seek(pos)
            line = f.readline()
            print("%d of %d" % (count, size))
            count += 1

        f.close()
        out.close()
