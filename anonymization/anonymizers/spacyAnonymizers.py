import spacy
import cfg

from ..Anonymization import Anonymization

# Список исключений, на которых без надобности срабатывают модели NER
stopList = ["БИК", "ИНН", "НДС", "К/c"]

class _NamedEntitiesAnonymizer():
    '''
    Replace all named entities with fake ones

    This class requires spacy and a spacy model:
    $ pip install spacy
    $ python -m spacy download <model>

    Call NamedEntitiesAnonymizer if you want to pass an instance to an AnonymizerChain
    '''

    def __init__(self, anonymization: Anonymization, model: str):
        self.anonymization = anonymization
        self.processor = spacy.load(model)

    def anonymize(self, text: str) -> str:
        doc = self.processor(text)
        # remove whitespace entities and trim the entities
        ents = [ent.text.strip() for ent in doc.ents if not ent.text.isspace()]

        return self.anonymization.replace_all(text, ents, 'first_name')

def NamedEntitiesAnonymizer(model: str) -> _NamedEntitiesAnonymizer:
    '''
    Context wrapper for _NamedEntitiesAnonymizer, takes a spacy model.
    '''

    return lambda anonymization: _NamedEntitiesAnonymizer(anonymization, model)
    
class _NamedEntitiesAnonymizer1():
    '''
    Replace all named entities with fake ones

    This class requires spacy and a spacy model:
    $ pip install spacy
    $ python -m spacy download <model>

    Call NamedEntitiesAnonymizer if you want to pass an instance to an AnonymizerChain
    '''

    def __init__(self, anonymization: Anonymization, model: str):
        self.anonymization = anonymization
        self.processor = spacy.load(model)

    def anonymize(self, text: str) -> str:
        doc = self.processor(text)
        # remove whitespace entities and trim the entities
        ents = []
        for ent in doc.ents:
            if (ent.text[-4:] == "PrcD") or (ent.text in stopList): #Уже обработанные случаи, если они поймались и Spacy, или случаи, которые мы специально исключили, пропускаем
                continue
            elif ent.label_ == "PER" and not ent.text.isspace():
                ents.append(ent.text.strip() + "PER")
            elif ent.label_ == "ORG" and not ent.text.isspace():
                ents.append(ent.text.strip() + "ORG")
            elif ent.label_ == "LOC" and not ent.text.isspace():
                ents.append(ent.text.strip() + "LOC")
            else:
                ents.append(ent.text.strip() + "MSC")
                
#        ents = [ent.text.strip() for ent in doc.ents if not ent.text.isspace()]

        return self.anonymization.replace_all_my(text, ents, 'name')



def NamedEntitiesAnonymizer1(model: str) -> _NamedEntitiesAnonymizer1:
    '''
    Context wrapper for _NamedEntitiesAnonymizer, takes a spacy model.
    '''

    return lambda anonymization: _NamedEntitiesAnonymizer1(anonymization, model)
    
    
class _NamedEntitiesAnonymizer2():
# Попытка использовать модель ru2
    '''
    Replace all named entities with fake ones

    This class requires spacy and a spacy model:
    $ pip install spacy
    $ python -m spacy download <model>

    Call NamedEntitiesAnonymizer if you want to pass an instance to an AnonymizerChain
    '''

    def __init__(self, anonymization: Anonymization, model: str):
#        import ru2
        self.anonymization = anonymization
#        self.processor = spacy.load(model)
#Если нужна модель с pymorphy2 в качестве лемматизатора и POS: 
        self.processor = spacy.load(model, disable=['tagger', 'parser', 'NER'])
#        self.processor = ru2.load_ru2(model)
        self.processor.add_pipe(self.processor.create_pipe('sentencizer'), first=True)

    def anonymize(self, text: str) -> str:
        doc = self.processor(text)
        # remove whitespace entities and trim the entities
        ents = []
        for ent in doc.ents:
            if (ent.text[-4:] == "PrcD") or (ent.text in stopList): #Уже обработанные случаи, если они поймались и Spacy, или случаи, которые мы специально исключили, пропускаем
                continue
            elif ent.label_ == "PER" and not ent.text.isspace():
                ents.append(ent.text.strip() + "PER")
            elif ent.label_ == "ORG" and not ent.text.isspace():
                ents.append(ent.text.strip() + "ORG")
            elif ent.label_ == "LOC" and not ent.text.isspace():
                ents.append(ent.text.strip() + "LOC")
            else:
                ents.append(ent.text.strip()+ "MSC")
                
#        ents = [ent.text.strip() for ent in doc.ents if not ent.text.isspace()]

        return self.anonymization.replace_all_my(text, ents, 'name')



def NamedEntitiesAnonymizer2(model: str) -> _NamedEntitiesAnonymizer2:
    '''
    Context wrapper for _NamedEntitiesAnonymizer, takes a spacy model.
    '''

    return lambda anonymization: _NamedEntitiesAnonymizer2(anonymization, model)
    
class _NamedEntitiesAnonymizer3():
# Попытка использовать модель stanza ru
    '''
    Replace all named entities with fake ones

    This class requires spacy and a spacy model:
    $ pip install spacy
    $ python -m spacy download <model>

    Call NamedEntitiesAnonymizer if you want to pass an instance to an AnonymizerChain
    '''

    def __init__(self, anonymization: Anonymization, model: str):
        import stanza
        from spacy_stanza import StanzaLanguage
        
        stanza.download('en', processors='tokenize,pos,lemma,depparse,ner')  # will take a while - один раз достаточно запустить
        stanza.download('ru', processors='tokenize,pos,lemma,depparse,ner')  # will take a while - один раз достаточно запустить
        
        self.anonymization = anonymization
        self.snlp = stanza.Pipeline(lang=model, processors='tokenize,ner')
        self.processor = StanzaLanguage(self.snlp)


    def anonymize(self, text: str) -> str:
        doc = self.processor(text)
        # remove whitespace entities and trim the entities
        ents = []
        for ent in doc.ents:
            if (ent.text[-4:] == "PrcD") or (ent.text in stopList): #Уже обработанные случаи, если они поймались и Spacy, или случаи, которые мы специально исключили, пропускаем
                continue
            elif ent.label_ == "PER" and not ent.text.isspace():
                ents.append(ent.text.strip() + "PER")
            elif ent.label_ == "ORG" and not ent.text.isspace():
                ents.append(ent.text.strip() + "ORG")
            elif ent.label_ == "LOC" and not ent.text.isspace():
                ents.append(ent.text.strip() + "LOC")
            else:
            # Слишком много лишнего ловится на MSC, попробуем буз этого
                continue
#                ents.append(ent.text.strip()+ "MSC")
                
#        ents = [ent.text.strip() for ent in doc.ents if not ent.text.isspace()]
        cfg.NERnumber += len(ents)

        return self.anonymization.replace_all_my(text, ents, 'name')


def NamedEntitiesAnonymizer3(model: str) -> _NamedEntitiesAnonymizer2:
    '''
    Context wrapper for _NamedEntitiesAnonymizer3, takes a stanza model.
    '''

    return lambda anonymization: _NamedEntitiesAnonymizer3(anonymization, model)


class _NamedEntitiesAnonymizer4():
# Попытка использовать модель stanza ru, только PER и ORG анонимизируем (для анонимизации параллельных корпусов)
    '''
    Replace all named entities with fake ones

    This class requires spacy and a spacy model:
    $ pip install spacy
    $ python -m spacy download <model>

    Call NamedEntitiesAnonymizer if you want to pass an instance to an AnonymizerChain
    '''

    def __init__(self, anonymization: Anonymization, model: str):
        import stanza
        from spacy_stanza import StanzaLanguage
        
#        stanza.download('en', processors='tokenize,pos,lemma,depparse,ner')  # will take a while - один раз достаточно запустить
        
        self.anonymization = anonymization
        self.snlp = stanza.Pipeline(lang=model, processors='tokenize,ner')
        self.processor = StanzaLanguage(self.snlp)


    def anonymize(self, text: str) -> str:
        doc = self.processor(text)
        # remove whitespace entities and trim the entities
        ents = []
        for ent in doc.ents:
            if (ent.text[-4:] == "PrcD") or (ent.text in stopList): #Уже обработанные случаи, если они поймались и Spacy, или случаи, которые мы специально исключили, пропускаем
                continue
            elif ent.label_ == "PER" and not ent.text.isspace():
                ents.append(ent.text.strip() + "PER")
            elif ent.label_ == "ORG" and not ent.text.isspace():
                ents.append(ent.text.strip() + "ORG")
            # Для параллельных корпусов не анонимизирует географию
#            elif ent.label_ == "LOC" and not ent.text.isspace():
#                ents.append(ent.text.strip() + "LOC")
            else:
            # Слишком много лишнего ловится на MSC, попробуем буз этого
                continue
#                ents.append(ent.text.strip()+ "MSC")
                
#        ents = [ent.text.strip() for ent in doc.ents if not ent.text.isspace()]
        cfg.NERnumber += len(ents)

        return self.anonymization.replace_all_my(text, ents, 'name')


def NamedEntitiesAnonymizer4(model: str) -> _NamedEntitiesAnonymizer2:
    '''
    Context wrapper for _NamedEntitiesAnonymizer3, takes a stanza model.
    '''

    return lambda anonymization: _NamedEntitiesAnonymizer4(anonymization, model)



