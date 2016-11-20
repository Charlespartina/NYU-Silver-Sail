import os
import threading
import selenium
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# I/O
def IO_Start():
  
  # Input
  info_line = []
  myusername = []
  mypassword = []
  mymonth = []
  mydate = []
  mytime = []
  myidentifier = []
  myroom = ['Bobst LL2-07','Bobst LL2-08','Bobst LL2-22','Bobst LL2-09','Bobst LL1-20']
  mynext = []
  
  f = open('credential/userinfo.txt','r+')
  for i in f:
    info_line.append(i)
  for i in info_line:
    if len(i) < 6:
      break
    print(i)
    split = i.split(' ')
    myusername.append(split[0])
    mypassword.append(split[1])
    mymonth.append(change_to_text(split[2]))  # Change number to string
    mydate.append(split[3])
    mytime.append(split[4])
    myidentifier.append(split[5][0:2])


  # Start
  start_threads(myusername,mypassword,mymonth,mydate,mytime,myidentifier,myroom)
  
  # Output
  f.seek(0,0)
  for i in range(len(mydate)):
    month_number = change_to_number(mymonth[i])
    mydate[i], month_number = update(mydate[i],month_number)
    f.write(myusername[i]+' '+mypassword[i]+' '+month_number+' '+mydate[i]+' '+mytime[i]+' '+myidentifier[i]+' \n')

  
  f.close()   
def update(inputdate, inputmonth):
  day = int(inputdate)
  month = int(inputmonth)
  
  # Change the value to determine the date of the next reservation
  day+=2
  # Set to the day after Tomorrow
  if day>31 and (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):   
     day=day%31
     month+=1 
  elif day>30 and (month==4 or month==6 or month==9 or month==11):
     day=day%30
     month+=1
  elif day>28 and month==2:
      day=day%28
      month+=1
  if month>12:
      month=1
  return str(day), str(month)
      
# Choose Multi-processes or Multi-threads to start the reservation at the bottom of the code

def change_to_text(month_number):
  month_word = '0'
  if month_number == '1':
    month_word = 'January'
  if month_number == '2':
    month_word = 'February'
  if month_number == '3':
    month_word = 'March'
  if month_number == '4':
    month_word = 'April'
  if month_number == '5':
    month_word = 'May'
  if month_number == '6':
    month_word = 'June'
  if month_number == '7':
    month_word = 'July'
  if month_number == '8':
    month_word = 'August'
  if month_number == '9':
    month_word = 'September'
  if month_number == '10':
    month_word = 'October'
  if month_number == '11':
    month_word = 'November'
  if month_number == '12':
    month_word = 'December'
  
  return month_word
    
    

def change_to_number(month_word):
  month_number = '0'
  if month_word=='January':
      month_number = '1'
  elif month_word=='February':
      month_number = '2'
  elif month_word=='March':
      month_number = '3'
  elif month_word=='April':
      month_number = '4'
  elif month_word=='May':
      month_number = '5'
  elif month_word=='June':
      month_number = '6'
  elif month_word=='July':
      month_number = '7'
  elif month_word=='August':
      month_number = '8'
  elif month_word=='September':
      month_number = '9'
  elif month_word=='October':
      month_number = '10'
  elif month_word=='November':
      month_number = '11'
  elif month_word=='December':
      month_number = '12'
  return month_number
  
  
def start_threads(username, password, month, date, time_hour, ampm_identifier, room):
  amount = 0
  for k in username:
    amount = amount+1
  threads = []
  for i in range(amount):
    t = threading.Thread(name = username[i], target = reservation, args=(username[i], password[i], month[i], date[i], time_hour[i], ampm_identifier[i], room))
    threads.append(t)
    t.start()

def reservation(username, password, month, date, time_hour, ampm_identifier, room):
  
  try:
    browser = webdriver.Chrome()
    browser.get('https://rooms.library.nyu.edu')
    assert "BobCat" in browser.title
    assert 'nyu_shibboleth-login' in browser.page_source
    print 'Portal Page Access Complete. pid=', os.getpid(), 'NetID=', username
    #ele = browser.find_element_by_id('nyu_shibboleth-login')
    ele = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "nyu_shibboleth-login"))
    )
    
    # print browser.title
    ele.click();
    assert "Login" in browser.title
    print 'Login Page Access Complete. pid=', os.getpid(), 'NetID=', username

    # Login
    browser.find_element_by_id("netid").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_xpath("//input[@type='submit']").click()
    assert 'Room' in browser.title
    print 'Login into Room Reservation System',username
    # Fill in reservation info
    hour = browser.find_element_by_name('reservation[hour]')
    minute = browser.find_element_by_name('reservation[minute]')
    ampm = browser.find_element_by_name('reservation[ampm]')
    howlong = browser.find_element_by_name('reservation[how_long]')
    hour.send_keys(time_hour)
    minute.send_keys('00')
    ampm.send_keys(ampm_identifier)
    howlong.send_keys('2 hours')
    print 'Reservation Time Info Complete ',username
    
    # Find appropriate date
    #icon = browser.find_element_by_id('room_reservation_which_date')

    WebDriverWait(browser, 100).until(
        EC.element_to_be_clickable((By.ID, "room_reservation_which_date"))
    ).click();
    # Click the next button
    while(True):
      monthgrid = browser.find_elements_by_class_name('ui-datepicker-month')
      nextgrid = browser.find_element_by_css_selector('span.ui-icon-circle-triangle-e')
      if monthgrid[1].text == month:   
        break
      nextgrid.click()

    # Click the date
    lastgrid = browser.find_element_by_css_selector('div.ui-datepicker-group-last')
    datebutton = lastgrid.find_element_by_link_text(date)
    datebutton.click()
    generate_grid =  browser.find_element_by_id('generate_grid')
    generate_grid.click()
    print 'Reservation Date Info Complete ',username
    
    # Calendar View
    content = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.ID, "new_reservation"))
    )
    footer = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='modal-footer']"))
    )
    print 'Calendar View is Opened', username
    body = content.find_element_by_css_selector('tbody')

    # Fill in email info
    email = footer.find_element_by_name('reservation[cc]')
    email.send_keys('tangziyi001@gmail.com')
    optionaltitle = footer.find_element_by_name('reservation[title]')
    optionaltitle.send_keys('Silver Sail Reservation for ',username)

    print 'Basic Info Filled', username
    #Choose time slot
    tr = body.find_elements_by_css_selector('tr')
    slot = 0;
    for room_number in room:
      for i in tr:
        roomtitle = i.find_element_by_class_name('room_title_text')
        if roomtitle.text == room_number:
          slot = i.find_element_by_css_selector('td.timeslot_preferred_first')
          break
      # Check if available
      slot_attribute = slot.get_attribute('class')
      if 'timeslot_unavailable' not in slot_attribute.split():
        print 'Time Slot Available', username
        newSlot = WebDriverWait(browser, 1000).until(
          EC.presence_of_element_located((By.XPATH, "//td[contains(@class, 'timeslot_preferred_first')]"))
        )
        newSlot.click()
        break
    print 'Choose Time Slot ', username

    # Click Button
    WebDriverWait(browser, 100).until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')]"))
    ).click()
    print 'Submition Complete',username
  
    #Check Status
    alert = WebDriverWait(browser, 1000).until(
      EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert')]"))
    )
    alert_attribute = alert.get_attribute('class')
    #print (alert_attribute.split())
    if 'alert-success' in alert_attribute.split():
      print 'Reservation Successful for NetID: ',username
    
    else:
      print 'Reservation Failed at the Final Stage for NetID: ', username
      
  except:
      print 'Reservation Failed for NetID: ',username,'\n',sys.exc_info()[0]
  finally:
    browser.quit()

if __name__ == "__main__":
  IO_Start()

  #start_threads(myusername, mypassword, mymonth, mydate, mytime, myidentifier, myroom)




