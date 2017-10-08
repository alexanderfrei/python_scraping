login_url = 'http://demo.en.cx/Login.aspx'
res_url = "http://moscow.en.cx/Addons.aspx?aid=16726"

# browser = webdriver.PhantomJS(executable_path='../selenium_drivers/phantomjs.exe')
# browser.get(bond_iframe)
# bond_source = browser.page_source
# browser.quit()
# soup = BeautifulSoup(bond_source,"html.parser")
#
# for div in soup.findAll('div',attrs={'class':'qs-note-panel'}):
# print div

# credentials = {'Login': '',
#                'Password': '',
#                'persistent': '1'}
#
# with requests.Session() as s:
#
#     # login
#     r = s.post(login_url, data=credentials)
#     res_page = s.get(res_url)
#     soup = BeautifulSoup(res_page.text, "lxml")
#     tb = soup.find_all('table')
#
#     with open('tb.txt', 'w', encoding='utf-8') as fl:
#         fl.write('\n'.join([t.text for t in tb]))
