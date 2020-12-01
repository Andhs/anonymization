import re
from ..Anonymization import Anonymization

class INNAnonymizer():

    #Замена чисел после ИНН, КПП, ОГРН, ОКВЭД 

    def __init__(self, anonymization: Anonymization):
        self.anonymization = anonymization
    
    def anonymize(self, text: str) -> str:
        formats = ['(?<=ИНН\s)\d+', '(?<=КПП\s)\d+', '(?<=ОГРН\s)\d+', '(?<=ОКВЭД\s)\d+', '(?<=ИНН:\s)\d+', '(?<=КПП:\s)\d+', '(?<=ОГРН:\s)\d+', '(?<=ОКВЭД:\s)\d+']

        for format_i in formats:
            regex = re.compile('\\b' + format_i.replace('_', '\d') + '\\b')
            
            text = self.anonymization.regex_anonymizer(text, regex, 'ean8')

        return text