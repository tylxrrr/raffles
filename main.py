import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

def entry(entryEmail, names):
    
    #webhook
    webhookUrl = ''
    
    #session
    r = requests.session()
    
    #link of raffle
    link = "https://stress95.typeform.com/app/form/submit/qN2qfq"
    #link of token
    token_link = "https://stress95.typeform.com/app/form/result/token/qN2qfq/default"
    
    #just some headers
    headers = {

        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

    }

    #token grabber
    res = r.get(token_link, headers=headers)
    token = res.text
    
    #splitting full name into first and last
    firstName = names.split(' ')[0]
    lastName = names.split(' ')[1]
    
    #epoch time for info
    epochTime = int(time.time())

    #the payload
    info = {

        'form[textfield:ZOaTbj6ogKYw]': firstName, 
        'form[textfield:y77C0LHxMyjS]': lastName, 
        'form[email:dKaPhlkbgjfn]': entryEmail, #
        'form[dropdown:jxTNcLWyKxYk]': 'United States of America', #Country
        'form[token]':token, 
        'form[landed_at]':str(epochTime) 
        
    }

    #entry post request
    post = r.post(link, data=info, headers=headers)
    
    #success reporter
    if "success" in (post.text):
        print("You just entered account " + entryEmail + " with first name: " + firstName + " and last name: " + lastName)
        webhookSuccess = DiscordWebhook(url=webhookUrl, username="Successful Entry!")
        embedS = DiscordEmbed(title='Email', description=entryEmail, color=65280)
        embedS.set_footer(text='raffle script by tyler')
        embedS.set_timestamp()
        embedS.add_embed_field(name='First Name', value=firstName)
        embedS.add_embed_field(name='Last Name', value=lastName)
        webhookSuccess.add_embed(embedS)
        webhookSuccess.execute()
        
    #fail reporter
    else:
        print("Something went wrong. Please restart script!")
        webhookFail = DiscordWebhook(url=webhookUrl, username="Failed Entry!")
        embedF = DiscordEmbed(title='Something went wrong.', description="Please restart script!", color=16711680)
        embedF.set_footer(text='raffle script by tyler')
        embedF.set_timestamp()
        webhookFail.add_embed(embedF)
        webhookFail.execute()
        exit()

#names
nameList = ['Tyler Test', 'Bread Pudding', 'Rice Beans']
#emails
emails = ["meatpie@gmail.com", "ducunu@gmail.com", "tamales@gmail.com"]
for entryEmail, names in zip(emails, nameList):
    entry(entryEmail, names)