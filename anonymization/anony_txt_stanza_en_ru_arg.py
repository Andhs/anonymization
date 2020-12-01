#!/usr/bin/python

import sys
import logging
from anonymization import Anonymization, AnonymizerChain, EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer3

def anony_txt(txtFile):
    anon_en = AnonymizerChain(Anonymization('en_US'))
    anon_en.add_anonymizers(EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer3('en'))

    anon_ru = AnonymizerChain(Anonymization('ru_RU'))
    anon_ru.add_anonymizers(EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer3('ru'))

    with open(txtFile, 'r', encoding='utf-8-sig') as f:
        anfile = open(txtFile[:-4] + "_anonymized.txt", 'w', encoding='utf-8')
        line = f.readline()
        while line:
            anline_en = anon_en.anonymize(line.split("\t")[0])
            anline_ru = anon_ru.anonymize(line.split("\t")[1])
            anfile.write(anline_en + "\t" + anline_ru)
            line = f.readline()
        anfile.close()
    
def main() :
    if len(sys.argv) != 1 :
        logging.info("Anonymization of bilingual txt file")
        logging.info("")
        logging.info("Usage: anony_txt_stanza_en_ru_arg bilingual_txt_file")
        sys.exit(-1)

    else:
        txtFile = sys.argv[1]

    anony_txt(txtFile)



if __name__ == '__main__': 
    main()