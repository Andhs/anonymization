from collections import defaultdict
from typing import Iterable, Pattern, Callable, List, Any
import re
import cfg

from faker import Factory

class Anonymization:
    '''
    Faker wrapper providing utility functions, to map values with fakes equivalents.
    '''

    def __init__(self, locale: str):
        self.locale = locale
        self.faker = Factory.create(locale)
        self.anonDicts = {}


    def getFake(self, provider: str, match: str) -> str:
        '''
        Return the fake equivalent of match using a Faker provider
        '''
        if not provider in self.anonDicts:
            self.anonDicts[provider] = defaultdict(getattr(self.faker, provider))
        
        return self.anonDicts[provider][match]

    def replace_all(self, text: str, matchs: Iterable[str], provider: str) -> str:
        '''
        Replace all occurance in matchs in text using a Faker provider
        '''
        # И добавдяем метку, что уже обработали каким-то модулем анонимизации
        for match in matchs:
            text = text.replace(match, self.getFake(provider, match) + "PrcD")

        return text
    
    def replace_all_my(self, text: str, matchs: Iterable[str], provider: str) -> str:
        '''
        Replace all occurance in matchs in text using a Faker provider
        '''
        # Вывожу только те модули, которые что-то нашли
        if matchs:
            print(matchs)
        '''
        for match in matchs:
            text = text.replace(match[:-3], "XXXX")
        '''
        '''
        for match in matchs:
            if match[-3:] == "PER":
                text = text.replace(match[:-3], self.getFake("first_name", match))
            elif match[-3:] == "ORG":
                text = text.replace(match[:-3], self.getFake("company", match))
            elif match[-3:] == "LOC":
                text = text.replace(match[:-3], self.getFake("city", match))
            else:
                text = text.replace(match[:-3], "XXXX")
#                text = text.replace(match[:-4], self.getFake(provider, match))

        '''
        '''
Это хороший рабочий вариант, но пока использую анонимизацию только с PER и ORG
        for match in matchs:
            if match[-3:] == "PER":
                text = text.replace(match[:-3], "<PERSON>")
            elif match[-3:] == "ORG":
                text = text.replace(match[:-3], "<FIRM>")
            elif match[-3:] == "LOC":
                text = text.replace(match[:-3], self.getFake("city_name", match))
            else:
                text = text.replace(match[:-3], "<ENTITY>")
        '''
        for match in matchs:
            if match[-3:] == "PER":
                text = text.replace(match[:-3], "ХХХХХХ")
            elif match[-3:] == "ORG":
                text = text.replace(match[:-3], "ХХХХХХ")
#            elif match[-3:] == "LOC":
#                text = text.replace(match[:-3], self.getFake("city_name", match))
            else:
                text = text.replace(match[:-3], "XXXXXX")

        # Убираем метку у уже обработанных другими модулями сущностей (здесь, так как обработка модулем Spacy идет после всех)
        text = text.replace("PrcD", "")
        return text
    
    def regex_anonymizer(self, text: str, regex: Pattern, provider: str) -> str:
        '''
        Anonymize all substring matching a specific regex using a Faker provider
        '''
        #Если regex такой сложный, что получаются подшаблоны (из-за скобок), findall начинает выдавать list of tuples вместо list of strings
        matchs = ["".join(x) for x in re.findall(regex, text)]
#        matchs = re.findall(regex, text)
        # Вывожу только те модули, которые что-то нашли
        if matchs:
            print(matchs)
        cfg.NERnumber += len(matchs)
        return self.replace_all(text, matchs, provider)

    def add_provider(self, provider):
        '''
        Add a faker provider
        '''
        return self.faker.add_provider(provider)


class AnonymizerChain:
    '''
    Tool to run many anonymizers using a single anonymization context
    '''

    def __init__(self, anonymization: Anonymization):
        self.anonymization = anonymization
        self._anonymizers = []

    def add_anonymizers(self, *args: Iterable[Callable[[Anonymization], Any]]) -> None:
        '''
        Add one or many anonymizers
        '''
        for arg in args:
            self._anonymizers.append(arg(self.anonymization))

    def clear_anonymizers(self) -> None:
        '''
        Remove all anonymizers
        '''
        self._anonymizers = []

    def anonymize(self, text: str) -> str:
        '''
        Run all registered anonymizers on a text
        '''
        for anonymizer in self._anonymizers:
            text = anonymizer.anonymize(text)

        return text

    def anonymize_all(self, texts: Iterable[str]) -> List[str]:
        '''
        Run all registered anonymizers on a list of texts
        '''
        return [self.anonymize(text) for text in texts]