import contextlib
import os
import sys
import dropmail
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tempfile
import time


@contextlib.contextmanager
def suppress_output():
   with open(os.devnull, 'w') as devnull:
      old_stdout = sys.stdout
      old_stderr = sys.stderr
      sys.stdout = devnull
      sys.stderr = devnull
      try:
         yield
      finally:
         sys.stdout = old_stdout
         sys.stderr = old_stderr


def setup_mailbox():
   mailbox = dropmail.Dropmail()
   # print(f'List of supported domains: {mailbox.supported_domains}\n')
   email_specific_domain = mailbox.new_email('dropmail.me')
   key_specific_domain = mailbox.get_key(email_specific_domain)
   print(f'mail address: {email_specific_domain} ({key_specific_domain})\n')
   return mailbox, email_specific_domain


def setup_driver():
   options = webdriver.EdgeOptions()
   user_data_dir = tempfile.mkdtemp()
   options.add_argument(f"--user-data-dir={user_data_dir}")
   options.add_argument("--remote-debugging-port=9222")
   driver = webdriver.Edge(options=options)
   driver.implicitly_wait(10)
   return driver

def vote_for_team(driver, email):
    driver.get("https://unsere-vereinsheimwerker.de/ibt/bin/public/voting/overview.ibtsico")
    search_field = driver.find_element(By.XPATH, '/html/body/page/main/block/pillar/item/block/container/item/block/tbl/div/div[2]/div/span/input[2]')
    search_field.send_keys("SV Baustetten")
    time.sleep(2)
    search_field.send_keys(Keys.RETURN)
    time.sleep(2)
    button = driver.find_element(By.XPATH, '/html/body/page/main/block/pillar/item/block/container/item/block/tbl/container/div/div[2]/div[1]/div/table/tbody/tr[3]/td[1]/button')
    button.click()
    time.sleep(2)
    textbox = driver.find_element(By.XPATH, '/html/body/page/main/scroll/pillar/container/item/block/sequence/item[2]/form/list/table/tbody/tr[2]/td[2]/div[1]/input')
    time.sleep(2)
    textbox.send_keys(email + Keys.RETURN)
    time.sleep(2)

def process_message(mailbox):
    message = mailbox.next_message()
    text = message['text']
    print(f'To (orig): {message["to_mail_orig"]}')
    print(f'To: {message["to_mail"]}')
    print(f'From: {message["from_mail"]}')
    print(f'Subject: {message["subject"]}')
    print(f'Body:\n{text}')
    return text

def extract_url(text):
    url_pattern = r'(https?://\S+)'
    url = re.findall(url_pattern, text)[0].rstrip(')')
    print(url)
    return url

def fetch_html(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html


def main():
    while True:
      try:
         time.sleep(2)
         mailbox, email_specific_domain = setup_mailbox()
         driver = setup_driver()
         # vote_for_team(driver, email_specific_domain)
         
         # driver.close()
         # text = process_message(mailbox)
         # url = extract_url(text)
         # html = fetch_html(url)
         # time.sleep(2)
         
      except KeyboardInterrupt:
         print("Program terminated by user")
         exit()
      except Exception as e:
         print(f"An exception occurred: {e}")
         time.sleep(10)

if __name__ == "__main__":
    main()
