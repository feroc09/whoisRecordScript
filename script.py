import schedule
import time
import requests
import json
import smtplib


def main():
    
    #ideally credentials are to be kept apart of the code, this bad practice is performed since it's a proof of concept.
    URL = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_Sg5uJOlmx3cfHln9hjftAGJG9mha7&domainName=google.com&outputFormat=JSON";
    
    #File that will contain the last day's registered data. Default data will be test data so that it stores the first execution data persistently.
    #Txt alternative is just for persistent storage demonstration purposes.
    #Using persistent storage, we don't need to keep the script running 24/7.
    file = open('yesterdayData.txt')
    lines = ''
    with file as f:
        lines = f.read().splitlines()

    response = requests.get(URL)
    try:
        if (response.status_code == 200):
            jsonObject = response.json()
            whoisRecord = jsonObject['WhoisRecord']
            todaysData = []
            todaysData.append(whoisRecord['createdDate'])
            todaysData.append(whoisRecord['updatedDate'])
            todaysData.append(whoisRecord['expiresDate'])
            todaysData.append(whoisRecord['contactEmail'])
            
            #We compare the values  from the text file with the data from the WhoisRecord
            for i in todaysData:
                if i in lines:
                    print(i + " was found in yesterday's data")
                    continue
                else:
                    print(i + " was NOT found in yesterday's data.")
                    #sendEmail()
                    print("Email sent")


            #Regardless if data changed, the file must be updated for these values to be considered "yesterday data" in 24hrs.
            file = open('yesterdayData.txt','r+') 
            file.truncate()

            for i in todaysData:
                file.write(i)
                file.write("\n")
            file.close()
            
        elif (response.status_code == 404):
            print ("Request failed")
    except:
        print ("Exception ocurred")

def sendEmail():
    sender = "senderEmail@gmail.com"
    receiver = "receiverEmail@gmail.com"

    message = "Information has changed"

    try:
        smtp_obj = smtplib.SMTP('localhost')
        smtp_obj.sendmail(sender, receivers, message)         
        print("Email sent")
    except smtplib.SMTPException:
        print("Unable to send email")



#We program a scheduler for every 86400 seconds (a day).
#This scheduler will run the main method as specified on the .do() parameter.
#If uninterrupted runtime is to be avoided, alternatives such as cron jobs on bash can be considered. 
#The business logic presented would work since it uses persistent data and runtime interrumptions do not cause data loss.
 
schedule.every(3).seconds.do(main)

while 1:
    schedule.run_pending()
