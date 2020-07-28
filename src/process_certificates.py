import traceback

def process_certificates(CertificateData):
        
    DataFile = open('../data/complete_data.csv', 'a')
    ModulusFile = open('../data/rsa_data.csv', 'a')
    ECPubKeyFile = open('../data/ec_data.csv', 'a')
    LogFile = open('../data/log.csv', 'a')

    Size = len(CertificateData)
    # for Certificate in range(len(CertificateData)):
    for Domain in CertificateData[0]:
        try:
            # print(Domain)

            # print('Process PID: %s - %d of %d\n\
            #     Domain: %s' % (os.getpid(), size, len(self.domains), domain[0]))
            # self.lock.acquire()
            
            if CertificateData[1] == 'rsa':
                # print(str(CertificateData[1])+','+str(CertificateData[2])+','\
                #     +str(CertificateData[3])+','+str(CertificateData[6]))
                DataFile.write(str(Domain)+','+str(CertificateData[1])+','+str(CertificateData[2])+','\
                    +str(CertificateData[3])+','+str(CertificateData[6])+','+str(CertificateData[7])+','\
                    +str(CertificateData[8])+','+str(CertificateData[9])+','+str(CertificateData[10])+','\
                    +str(CertificateData[11])+','+str(CertificateData[12])+','+str(CertificateData[13])+','\
                    +str(CertificateData[14])+','+str(CertificateData[15])+'\n')
                ModulusFile.write(str(CertificateData[2])+'\n')
            if CertificateData[1] == 'ec':
                # print(str(Domain[0])+','+str(CertificateData[1])+str(CertificateData[4])+','\
                #     +str(CertificateData[5])+','+str(CertificateData[6]))
                DataFile.write(str(Domain)+','+str(CertificateData[1])+str(CertificateData[4])+','\
                    +str(CertificateData[5])+','+str(CertificateData[6])+','+str(CertificateData[7])+','\
                    +str(CertificateData[8])+','+str(CertificateData[9])+','+str(CertificateData[10])+','\
                    +str(CertificateData[11])+','+str(CertificateData[12])+','+str(CertificateData[13])+','\
                    +str(CertificateData[14])+','+str(CertificateData[15])+'\n')
                ECPubKeyFile.write(str(CertificateData[5])+'\n')  
            # self.lock.release()
            Size -= 1
        except Exception:
            #pass
            error = traceback.format_exc()
            ErrorLine = error.split('\n')
            LogFile.write('[ERROR] -  to obtain the certificate\nDomain: %s\nType of error: %s\n'\
                    % (Domain[0], ErrorLine[-2]))
            Size -= 1
            continue
        
    DataFile.close()
    ModulusFile.close()
    ECPubKeyFile.close()
    LogFile.close()