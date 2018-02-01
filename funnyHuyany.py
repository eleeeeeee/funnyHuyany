# first need to send updates reuest to server

# inline keyboard
# sqllite for data saving
import time
import json
import requests
import os.path
import re

#+ 1) sqllite db to store lastMessageID +
#+ 2) store user info
# 3) make keyboard to make event
# 
# 4) store event info

# admin начинает событие: 
# он должен указат 2 команды и наименование события?
# игрок выбирает событие и ставит каждой команде счет


# меню админа:
# 1) Редактирование событий
# 2) Сделать ставку
# 3) Просмотреть ставки

# 1) Управление событиями:
# 1.1) Добавить
# 1.2) Завершить
# 1.1.1) Введите наименование события
# 1.1.2) Введите наименование первой команды
# 1.1.1) Введите наименование второй команды
# 1.1.1) Подтвердите добавление события



MAINURL_ = "https://api.telegram.org/bot420635280:AAHIdDrlF39Jo5WRLfVmutTozs5kwh6dJcA/"

def ReadLastUpdateID():
    updateID = -1
    if os.path.exists("lastUpdateID.dat"):
        configFIle = open("lastUpdateID.dat", "r")
        updateID = int(configFIle.read())
        configFIle.close()
    else:
        WriteLastUpdateID(updateID)
    return updateID

def WriteLastUpdateID(lastID):
    configFIle = open("lastUpdateID.dat", "w")
    if configFIle.writable():
        configFIle.write(str(lastID))
    configFIle.close()



def SendTextMessage(userID, text):
    params = {'chat_id': userID, 'text': text}
    result = requests.get(MAINURL_ + "sendMessage", params)
    


vowels = re.compile("а|у|о|ы|и|э|я|ю|ё|е")

def ChangeWord(msgText):
    # дойти до первой гласной, индекс которой > 1 и заменять на "ху"
    newText = msgText
    if len(msgText) > 2:
        firstIndex = vowels.search(msgText)
        if firstIndex == None:
            return newText
        index = firstIndex.start()
        if index > -1:
            newText = "ху" + msgText[index:]
    return newText

def ChangeText(msgText):
    indexStart = 0
    indexEnd = msgText.find(" ", indexStart)
    maxLen = len(msgText)
    if indexEnd < 0:
        indexEnd = maxLen
    outText = ""
    while indexStart < maxLen:
        textToChange = msgText[indexStart : indexEnd]
        textToSend = ChangeWord(textToChange)
        # SendTextMessage(userID, textToSend)
        indexStart += len(textToChange) + 1
        indexEnd = msgText.find(" ", indexStart)
        outText += textToSend + " "
    
    return outText[:len(outText) - 1] + "!!!"

def ParseResults(resStr):
    id = resStr['update_id']

    if resStr.get('callback_query', '0') != '0':
        id = resStr['update_id']
        WriteLastUpdateID(LASTUPDATEID_)
        userID = resStr['callback_query']['message']['chat']['id']
        messageID = resStr['callback_query']['message']['message_id']
        callbackData = resStr['callback_query']['data']
        queryID = resStr['callback_query']['id']
        #ProcessMenu(queryID, messageID, callbackData, userID)
    if resStr.get('message', '0') != '0':
        chatID =   resStr['message']['chat']['id']
        userID =   resStr['message']['from']['id']
        name =     resStr['message']['from']['first_name']
        lastName = resStr['message']['from']['last_name']

        msgText = resStr['message']['text']
        sendText = ChangeText(msgText.lower())
        SendTextMessage(userID, sendText)


    return id


LASTUPDATEID_ = ReadLastUpdateID()
print("started")
while (1):
    try:
        params = {'offset': LASTUPDATEID_ + 1}
        result = requests.get(MAINURL_ + "getUpdates", params)
        if (result.status_code == 200) :
            curResults = result.json()
            
            for res in curResults['result']:
                logFile = open("log.dat", "a")
                logFile.write(json.dumps(res) + "\n")
                logFile.close()
                print (res)
                LASTUPDATEID_ = ParseResults(res)
                
            
    except Exception as e:
        print(e)
    finally:
         time.sleep(1)
