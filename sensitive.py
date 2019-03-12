#!/usr/bin/python
from bs4 import BeautifulSoup
import argparse, os, sys, commands, requests, base64
import os.path
from requests.exceptions import ConnectionError

class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

protocols = ["http","https"]

def code(url):
    codex = commands.getoutput('curl -s -o /dev/null -w "%{http_code}" '+url+' --max-time 10')
    return codex

def false_positive(url):
        response = requests.get(url)
        try:
                if len(response.content) == 0:
                        return False
                else:
                        errors = ["Not Found", "not found", "error", "Error"]
                        if any(error in response.content for error in errors):
                                return False
                        else:
                                return True
        except ConnectionError:
                return False

def get_title(content):
    soup = BeautifulSoup(content, "lxml")
    title = soup.find('title')
    if title is None:
        return "Blank Title"
    else:
        titlex = str(title).replace("\n", " ")
        return titlex

def bot(message):
        token = '' ##make your own token faggot
        chat_id = '' ## This is where shits will send :D
        cmd = commands.getoutput('curl -g "https://api.telegram.org/bot'+token+'/sendmessage?chat_id='+chat_id+'&text='+message+'"')
        return cmd

def trimsu(url):
        url1 = url.rstrip("/")
        if 'https://' in url1:
                final_url = url1[8:]
        elif 'http://' in url1:
                final_url = url1[7:]
        else:
                final_url = url1
        return final_url
        #just in case you want to scan a domain list with protocol

parser = argparse.ArgumentParser(description='')
parser.add_argument('-u', '--url', help='URL Lists File')
parser.add_argument('-w', '--wordlist', nargs='?', action="store", help="Custom Wordlist file")
args = parser.parse_args()


if __name__ == '__main__':

        try:
                if args.url:
                        if os.path.isfile(args.url) == True:
                                urls = open(args.url, "r")
                                counts = len(open(args.url).readlines())
                                print bc.HEADER+"URL Count :: "+str(counts)+" from "+args.url+bc.ENDC
                        else:
                                print bc.FAIL+"Not a File"+bc.ENDC
                                exit(2)
                       
                        for url in urls:
                            try:
                                urlx = url.split('\n')
                                final_url = trimsu(urlx[0])
                                for pro in protocols:
                                        test = pro+"://"+final_url
                                        print "-------------- "+test+" --------------"
                                        # If the lazy shitty assholes wants to provide a ton shit of file list or directory
                                        wordlist = args.wordlist
                                        if wordlist:
                                                if os.path.isfile(wordlist) == True:
                                                    files = open(wordlist, "r")
                                                else:
                                                    print bc.FAIL+"Not a File"+bc.ENDC
                                                    exit(2)
                                        else:
                                            files = [".gitignore",".svn/wc.db",".git/config", "phpmyadmin/", ".travis.yml",".DS_Store",".htaccess",".htpasswd","Makefile","Dockerfile","package.json","gulpfile.js","composer.json","web.config",".env",".idea","nbproject/","bower.json","package-lock.json",".gitlab-ci.yml","database.yml"]
                                        for filex in files:
                                            filey = filex.split()
                                            file = str(filey[0])
                                            c = code(test+"/"+file)
                                            logfile = open('spade~'+base64.b64encode(args.url)+'.log', 'a')
                                            if c == '000':
                                                print bc.FAIL+str(test+"/"+file)+" :: Connection Error!" +bc.ENDC
                                                logfile.write(str(test+"/"+file)+" :: Connection Error!\n")
                                                continue
                                            r = commands.getoutput('curl -L '+str(test+"/"+file)+' --connect-timeout 10')
                                            l = commands.getoutput('curl -I -L '+str(test+"/"+file)+' --silent | grep -Fi Location')
                                            if c == '200':
                                                    if false_positive(test+"/"+file) == True:
                                                            print bc.BOLD+'['+str(c)+'] '+str(test+"/"+file)+' :: '+get_title(r)+bc.ENDC
                                                            bot("[FOUND] "+str(test+"/"+file)+' :: '+get_title(r))
                                                            logfile.write('['+str(c)+'] '+str(test+"/"+file)+' :: '+get_title(r)+"\n")
                                                    else:
                                                            print bc.FAIL+'['+str(c)+'] False Positive:: '+str(test+"/"+file)+' :: '+get_title(r)+bc.ENDC
                                            elif c == '301' or c == '302':
                                                    print bc.HEADER+'['+str(c)+'] '+str(test+"/"+file)+'\n--- Redirect ---\n'+str(l)+'\n'+get_title(r)+'\n----------------\n'+bc.ENDC
                                                    logfile.write('['+str(c)+'] '+str(test+"/"+file)+'\n--- Redirect ---\n'+str(l)+'\n'+get_title(r)+'\n----------------\n\n')
                                            elif 'SSL: no alternative certificate' in r:
                                                    print bc.WARNING+'['+str(c)+'] '+str(test+"/"+file)+' :: Certificate Error: Insecure Connection!' +bc.ENDC
                                                    logfile.write('['+str(c)+'] '+str(test+"/"+file)+' :: Certificate Error: Insecure Connection!\n')
                                            else:
                                                    print bc.OKBLUE+'['+str(c)+'] '+str(test+"/"+file)+' :: '+get_title(r) +bc.ENDC
                                                    logfile.write('['+str(c)+'] '+str(test+"/"+file)+' :: '+get_title(r)+'\n')
                                        print "------------------------------------------\r\n"
                            except ConnectionError:
                                continue
                        bot("Done Scanning: "+args.url)
                        
                else:
                        print bc.WARNING+"Invalid Argument!, Please check -h or --help options."+bc.ENDC
                        exit(2)
        except KeyboardInterrupt:
                print bc.FAIL+'\nKeyboard Interrupt...\nExiting!'+bc.ENDC
                try:
                        sys.exit(0)
                except SystemExit:
                        os._exit(0)
