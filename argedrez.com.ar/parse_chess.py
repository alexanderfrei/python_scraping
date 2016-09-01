from selenium import webdriver

dt = ""
page = 0
forward = ""
parse_stop = False

driver = webdriver.Chrome()
driver.get("http://www.argedrez.com.ar")
driver.find_element_by_xpath('//*[@id="lnkEventosAnteriores"]').click()

while not parse_stop:
    print("----------------------- page #" + str(page) + "-----------------------")
    for i in range(1,55):
        try:
            driver.find_element_by_xpath('//*[@id="gvTorneos"]/tbody/tr[' + str(i) + ']/td[1]/a').click()
            dt = driver.find_element_by_xpath('//*[@id="gvTorneos"]/tbody/tr[' + str(i) + ']/td[5]').text;
            if int(dt.split('/')[0]) < 11 and dt.split('/')[2] == '2013':
                parse_stop = True
                break
            print(dt, dt.split('/')[0], dt.split('/')[2])
        except:
            continue
    if page == 0:
        forward = '// *[ @ id = "gvTorneos"] / tbody / tr[52] / td / table / tbody / tr / td[1] / input';
    else:
        forward = '// *[ @ id = "gvTorneos"] / tbody / tr[52] / td / table / tbody / tr / td[3] / input';
    page += 1
    driver.find_element_by_xpath(forward).click()

driver.close()
