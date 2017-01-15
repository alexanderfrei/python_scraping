# Scraping web with python
It's based partly on this book:
http://shop.oreilly.com/product/0636920034391.do

##argedrez.com.ar
Download of free chess tournaments databases with Selenium WebDriver.

http://argedrez.com.ar is a beautiful chess site with a broad range of tournaments.

Parse_chess.py script download tournaments PGN bases by the predetermined condition.  
There is the chromedriver.exe for Chrome webdriver.

## flashscore
Parse statistics, bookmaker coefficient and description of games from http://www.flashscore.com with Selenium WebDriver for statistical purpose.

Return txt comma delimited file in output.

*id_parse.py* contains functions for waiting and load page + class for one game parsing.

January 2017: list of bookmakers has updated on site, therefore this part of code require revision.
