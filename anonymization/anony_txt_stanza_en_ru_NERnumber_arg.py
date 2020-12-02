#!/usr/bin/python

import sys
from anonymization import Anonymization, AnonymizerChain, EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer4
import cfg

def anony_txt(txtFile):
    anon_en = AnonymizerChain(Anonymization('en_US'))
    anon_en.add_anonymizers(EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer4('en'))

    anon_ru = AnonymizerChain(Anonymization('ru_RU'))
    anon_ru.add_anonymizers(EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer4('ru'))

    with open(txtFile, 'r', encoding='utf-8-sig') as f:
        anfile = open(txtFile[:-4] + "_anonymized.txt", 'w', encoding='utf-8')
        rejfile = open(txtFile[:-4] + "_rejected_anonymization.txt", 'w', encoding='utf-8')
        line = f.readline()
        while line:
            cfg.NERnumber = 0
            anline_en = anon_en.anonymize(line.split("\t")[0])
            NERnumber_en = cfg.NERnumber
            cfg.NERnumber = 0
            anline_ru = anon_ru.anonymize(line.split("\t")[1])
            NERnumber_ru = cfg.NERnumber
            if NERnumber_en == NERnumber_ru:
                anfile.write(anline_en + "\t" + anline_ru)
            else:
                anfile.write(line)
                rejfile.write(anline_en + "\t" + anline_ru)
            line = f.readline()
        anfile.close()
        rejfile.close()
    
def main() :
    if len(sys.argv) != 2 :
        logging.error("Anonymization of bilingual txt file")
        logging.error("")
        logging.error("Usage: anony_txt_stanza_en_ru_arg bilingual_txt_file")
        sys.exit(-1)

    else:
        txtFile = sys.argv[1]

    anony_txt(txtFile)



if __name__ == '__main__': 
    main()