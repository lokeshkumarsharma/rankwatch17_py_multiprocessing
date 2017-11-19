import multiprocessing						
import csv
import os
import sys
import smtplib													#smtplib module use to define an SMTP client session object
from email.MIMEMultipart import MIMEMultipart					#This module provides a parser for the multipart/form-data format
from email.MIMEText import MIMEText



# SMTP server details.
SMTPserver = 'smtp.gmail.com'

# Server port.
serverPort = 587

# Username for mail server.
username = ""

# Password for mail server.
password = ""

# Sender mail for mailgun.
sender=""

#get the current directory
mail_csv_file = os.getcwd() + '/mail_details.csv'


def main():
  #Reads mail information from csv file.
  mail_list = []								#create a empty list
  print mail_csv_file							#print the csv file 
  with open(mail_csv_file, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      process = multiprocessing.Process(target=send_mail, args=(row))
      mail_list.append(process)
      process.start()

  for job in mail_list:
    job.join()
    print '%s.exitcode = %s' % (job.name, job.exitcode)


def send_mail(receiver, subject, message):
	 # Sends mail.
	 #  receiver: Mail receiver.
     # subject: Mail subject.
     #message: Mail content.
  
  try:
    msg = MIMEMultipart()
    msg['From'] = username										
    msg['To'] = receiver										
    msg['Subject'] = subject									

    msg.attach(MIMEText(message))				# Create a text/plain message

    mailserver = smtplib.SMTP(SMTPserver, serverPort)
    mailserver.ehlo()					#used to Identify yourself to an ESMTP server
    mailserver.starttls()				#Put the SMTP connection in TLS (Transport Layer Security) mode
    mailserver.ehlo()					
    mailserver.login(username, password)						

    try:
      mailserver.sendmail(username, receiver, msg.as_string())	#send an email where msg.as_string converts to msg into email
    finally:													#finally block that will execute whether the error occurred or not							
      mailserver.quit()											#quit to mail server
  except Exception, exc:										#catch an exception		
      sys.exit( "mail failed; %s" % str(exc) )


if __name__ == '__main__':
  main()														#call to main() function

