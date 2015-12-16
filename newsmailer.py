import smtplib,urllib,json,datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Date strings for proper wiki queries and email subject
subject_date_string = datetime.datetime.now().strftime("%A %b %-d, %Y - %I:%M %p")
wiki_today_string = datetime.datetime.now().strftime("%Y_%B_%-d")
wiki_yesterday_string = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y_%B_%-d")

news_urls = [
"https://en.wikipedia.org/w/api.php?action=query&titles=Portal:Current_events/Headlines&prop=revisions&rvprop=content&format=json&rvparse=",
"https://en.wikipedia.org/w/api.php?action=query&titles=Portal:Current%20events/"+wiki_today_string+"&prop=revisions&rvprop=content&format=json&rvparse=",
"https://en.wikipedia.org/w/api.php?action=query&titles=Portal:Current%20events/"+wiki_yesterday_string+"&prop=revisions&rvprop=content&format=json&rvparse="
]

final_display = ""

for url in news_urls:
    json_content = json.load(urllib.urlopen(url))
    final_display += json_content["query"]["pages"][json_content["query"]["pages"].keys()[0]]["revisions"][0]["*"]

#Fix links in wiki content (normally relative instead of absolute links)
final_display = final_display.replace("href=\"/wiki/","href=\"http://en.wikipedia.org/wiki/")

#Email the news
FROM = 'sending_email_address'
TO = ['recipient_email_address','recipient2_email_address']
MSG = MIMEMultipart('alternative')
MSG['Subject'] = "Newsmailer for "+subject_date_string
MSG['From'] = FROM
MSG['To'] = ", ".join(TO)
MSG.attach(MIMEText(final_display.encode('utf-8'),'html'))

mailer = smtplib.SMTP_SSL('smtp_server_address')
mailer.login(FROM,r"password")
mailer.sendmail(FROM,TO,MSG.as_string())
mailer.quit()
