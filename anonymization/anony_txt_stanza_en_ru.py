from tkinter.filedialog import askopenfilename, mainloop
import tkinter.messagebox
from anonymization import Anonymization, AnonymizerChain, EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer3

anon_en = AnonymizerChain(Anonymization('en_US'))
anon_en.add_anonymizers(EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer3('en'))

anon_ru = AnonymizerChain(Anonymization('ru_RU'))
anon_ru.add_anonymizers(EmailAnonymizer, UriAnonymizer, MacAddressAnonymizer, PhoneNumberAnonymizer, INNAnonymizer, NamedEntitiesAnonymizer3('ru'))

# Получение файла для преобразования
input_file_path = askopenfilename(title="Open bilingual EN-RU TXT file for anonymization", filetypes=[("TXT files", "*.txt")])

# В готовые теги target вставляем текст из source после анонимизации 
with open(input_file_path, 'r', encoding='utf-8-sig') as f:
    anfile = open(input_file_path[:-4] + "_anonymized.txt", 'w', encoding='utf-8')
    line = f.readline()
    while line:
        anline_en = anon_en.anonymize(line.split("\t")[0])
        anline_ru = anon_ru.anonymize(line.split("\t")[1])
        anfile.write(anline_en + "\t" + anline_ru)
        line = f.readline()
    anfile.close()
    
tkinter.messagebox.showinfo("Title", "Success!")

mainloop()