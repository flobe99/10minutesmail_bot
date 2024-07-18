import dropmail
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

while True:
   try:

      mailbox = dropmail.Dropmail()

      print('List of supported domains: {}\n'.format(mailbox.supported_domains))

      email_default = mailbox.default_email

      email_random_domain = mailbox.new_email()

      email_specific_domain = mailbox.new_email('dropmail.me')
      key_specific_domain = mailbox.get_key(email_specific_domain)

      print('{} ({})\n'.format(email_specific_domain, key_specific_domain))

      service = webdriver.EdgeService(executable_path="./msedgedriver.exe")
      driver = webdriver.Edge()

      driver.get("https://www.unsere-vereinsheimwerker.de/ibt/myso/cty/area=site/de/bin/public/voting/vote.ibtsico?path=ibt:/division/myso/op/master/voting/2023/2024/673668951&cmd:viewport=1525x1039%401")
      driver.implicitly_wait(10)

      textbox = driver.find_element(By.XPATH, '/html/body/page/main/scroll/pillar/container/item/block/sequence/item[2]/form/list/table/tbody/tr[2]/td[2]/div[1]/input')
      time.sleep(2)
      textbox.send_keys(email_specific_domain+ Keys.RETURN)

      time.sleep(2)

      print("driver get")
      driver.close()

      message = mailbox.next_message()

      text = format(message['text'])

      print('To (orig): {}'.format(message['to_mail_orig']))
      print('To: {}'.format(message['to_mail']))
      print('From: {}'.format(message['from_mail']))
      print('Subject: {}'.format(message['subject']))
      print('Body:\n{}'.format(message['text']))


      url_pattern = r'(https?://\S+)'

      url = re.findall(url_pattern, text)

      url = url[0].rstrip(')')

      print(url)

      with urllib.request.urlopen(url) as response:
         html = response.read()

   except:
      print("An exception occurred")
