import umail
import network
import time

# Your email details
sender_email = 'gaspard.derruine@gmail.com'
sender_name = 'RaspberryPiPico'
sender_app_password = 'bvst fwkq kohj hcxn'
recipient_email ='gaspard.derruine@gmail.com'
email_subject ='Email from RPiPico'

# Your network credentials
ssid = 'linksysed'
password = 'tototiti'

#Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection to establish
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
            break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Manage connection errors
if wlan.status() != 3:
    raise RuntimeError('Network Connection has failed')
else:
    print('connected')


# Send email once after MCU boots up
smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
smtp.login(sender_email, sender_app_password)
smtp.to(recipient_email)
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
smtp.write("This is an email from Raspberry Pi Pico")
smtp.send()
smtp.quit()