from os import path

#Проверят создан ли файл chatids.txt
if not path.exists("chatids.txt"):
    open("chatids.txt", "w").close()
#Загрузка массива с файла в SET (Разсылка идет по SET, не по файлу (файл выступает в роли истории))
chatids_file = open("chatids.txt", "r")
chatids_users = set ()
for line in chatids_file:
    chatids_users.add(line.strip())
chatids_file.close()