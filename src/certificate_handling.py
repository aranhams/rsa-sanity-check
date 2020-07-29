import gzip
import math
import ssl
import os
import asn1crypto.x509 as x509
import process_certificates as pc

FileName = 'cert.der'

def unzip_certificates(certificate):

    with gzip.open('../certificates/' + certificate,'rt') as f:
        for line in f:
            CertificateHasExpired = update_certificate(line.split(',')[1])
            extract_info_certificates(CertificateHasExpired)

def update_certificate(Certificate):

    Certificate = "-----BEGIN CERTIFICATE-----\n" + Certificate + "-----END CERTIFICATE-----\n"

    f = open(str(FileName), 'wb')

    try:
        NewCertificate = crypto.load_certificate(crypto.FILETYPE_PEM, Certificate.encode())
    except:
        NewCertificate = 'none'

    try:
        CertificateHasExpired = NewCertificate.has_expired()
    except:
        CertificateHasExpired = 'none'

    f.write(ssl.PEM_cert_to_DER_cert(Certificate))
    f.close()

    return CertificateHasExpired

def extract_info_certificates(CertificateHasExpired):

    with open(str(FileName), "rb") as f:
        Certificate = x509.Certificate.load(f.read())      

        CertificateAlgorithm  = Certificate.public_key.native["algorithm"]["algorithm"]
        if CertificateAlgorithm == 'rsa' :
            CertificateCurve = 'none' # apenas para EC 
            CertificatePubKey = 0 # apenas para EC
            CertificateModulus = Certificate.public_key.native["public_key"]["modulus"]
            CertificatePubExp = Certificate.public_key.native["public_key"]["public_exponent"]
            CertificateKeySize = int(math.fabs(Certificate.public_key.bit_size))
        elif CertificateAlgorithm == 'ec' :
            CertificateCurve = Certificate.public_key.native["algorithm"]["parameters"]
            CertificatePubKey = Certificate.public_key.native["public_key"].hex()
            CertificateModulus = 0
            CertificatePubExp = 0
            CertificateKeySize = int(Certificate.public_key.bit_size)
        else:
            try:
                CertificateCurve = Certificate.public_key.native["algorithm"]["parameters"]
            except:
                CertificateCurve = 'none'
            try:
                CertificatePubKey = Certificate.public_key.native["public_key"].hex()
            except:
                CertificatePubKey = 'none'
            try:
                CertificateModulus = Certificate.public_key.native["public_key"]["modulus"]
            except:
                CertificateModulus = 0
            try:
                CertificatePubExp = Certificate.public_key.native["public_key"]["public_exponent"]
            except:
                CertificatePubExp = 0
            try:
                CertificateKeySize = int(Certificate.public_key.bit_size)
            except:
                CertificateKeySize = 0 
        try:
            CertificateIssuerCountry = Certificate.issuer.native["country_name"]
        except:
            CertificateIssuerCountry = "Empty"
        try:
            CertificateIssuerName = Certificate.issuer.native["organization_name"]
        except:
            CertificateIssuerName = "Empty"
        try:
            CertificateIssuerCommonName = Certificate.issuer.native["common_name"]
        except:
            CertificateIssuerCommonName = "Empty"

        CertificateSigAlgorithm = Certificate.signature_algo
        CertificateSelfSigned = Certificate.self_signed
        CertificateHashAlgorithm = Certificate.hash_algo
        CertificateDomains = Certificate.valid_domains
        try:
            CertificateNotValidBefore = Certificate.native['tbs_certificate']['validity']['not_before']
        except:
            CertificateNotValidBefore = "Empty"
        try:
            CertificateNotValidAfter = Certificate.native['tbs_certificate']['validity']['not_after']
        except:
            CertificateNotValidAfter = "Empty"
        
        os.remove(str(FileName))

        CertificateData = [CertificateDomains, CertificateAlgorithm, '{0:02x}'.format(CertificateModulus), 
          CertificatePubExp, CertificateCurve, CertificatePubKey, CertificateKeySize, CertificateNotValidBefore, 
          CertificateNotValidAfter, CertificateHasExpired, CertificateSigAlgorithm, CertificateIssuerCountry, 
          CertificateIssuerName, CertificateIssuerCommonName, CertificateSelfSigned, CertificateHashAlgorithm]

        pc.process_certificates(CertificateData)