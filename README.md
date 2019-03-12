# Sensitive-File-Explorer

Upload this script in your VPS or server and run it in background

`$ nohup python sensitive.py -u domain_list.txt &`

domain list should be like
```
http://example.com/
example.com
https://example.com
example.com:8080
```

If Sensitive file or directory found it will be sent to your telegram bot.

_Note: just create your own telegram bot first_

-----------------------------
# Creating Telegram Bot
* Download and install Telegram
* Create or Login your Account
* click the search icon and search for **BotFather**
* now message **BotFather**
* type in `/newbot` and hit enter
* it will ask a bot name
* Next, it will ask for bot username
* after setting up bot name and username. BotFather will give you the api token of your bot and make sure to read the message carefully.
* Go to sensitive.py file, line `47` and paste the api token
* In line `48` just find a way on how to discover your own telegram id.

_Note: i forgot on how to discover your telegram profile ID. maybe google can answer that :)_

-----------------------------
# Dependency Installations:

`$ pip install BeautifulSoup os sys commands argparse base64`

-----------------------------

Log file is also greppable

`$ cat spade~domain_list.log | grep "[200]"`

or

`$ cat spade~domain_list.log | grep "Location"`

-----------------------------
# Basic Commands

if you like not to run this in background you can just run it.

`$ python sensitive.py -u domain_list.txt`

and it will scan the files if the ff is existing in the target domains:

```
.git/config
.travis.yml
.DS_Store
.htaccess
.htpasswd
Makefile
Dockerfile
package.json
gulpfile.js
composer.json
web.config
.env
```

_Note: feel free to improve the array list if you have a suggestion. just the famous and common files to find._

or if you have a file/directory list you can just run

`$ python sensitive.py -u domain_list.txt -w your_own_file_or_directory_list.txt`

## I admit that there are still a false positive scan results and if you can suggest a fix for it, you can contact me via twitter (@phspades) :)
_My python coding still a beginner level but it still works :)_
