 
#=========================================================================================================
# modules
#=========================================================================================================
import atexit
import sys
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#=========================================================================================================
# globals
#=========================================================================================================
LINKS_FILE_PATH = "./links.txt"
IMGS_FOLDER_PATH = "./imgs"
TARGET_CLASS = "originalLink-Azwuo9"
TARGET_URL = "https://discord.com/channels/662267976984297473/1011408429170044928"
DRIVER_PATH = "./geckodriver.exe"
LINKS = []

#=========================================================================================================
# functions
#=========================================================================================================
def scrapeLinks(p_targetURL,p_targetClass):
    # sets up the webdriver
    driver = webdriver.Firefox(executable_path=DRIVER_PATH)
    driver.get(p_targetURL)
    driver.implicitly_wait(20)

    attemptCount=0
    # gets all links in the page which are visible with the class name "originalLink-Azwuo9"
    while (attemptCount < 200000):
        try:
            print("try getting links in 5 seconds")
            #counts down
            for x in range(5):
                print(5-x)
                time.sleep(1)
            print("attempt started")
            currentVisibleLinks = driver.find_elements(By.XPATH, '//a[@class="'+p_targetClass+'"]')

            for currentVisibleLink in currentVisibleLinks:
                # gets href attribute
                href = currentVisibleLink.get_attribute("href")
                # adds currentVisibleLink to LINKS if its not already in LINKS
                if (LINKS.__contains__(href) == False):
                    LINKS.append(href)
                    print(LINKS.__len__())
                    # for every 1000 attempt, saves LINKS to a file
                    if (attemptCount % 1000 == 0):
                        #save list to file
                        saveListToFile(LINKS)
                        print("saved LINKS to file, reseting LINKS")
                        LINKS.clear()
                # increments attemptCount
                attemptCount=attemptCount+1         
            # scroll up
            body=driver.find_element(By.XPATH, '//body')
            body.send_keys(Keys.HOME)
            time.sleep(2)
        except Exception as e:
            print(e)
            print("error")
         

# saves a list to file if item is not already in the file
def saveListToFile(p_list):
    # open file
    with open("./links.txt", "r+") as file:
        # read all lines
        linksFileContent = file.readlines()
        # for every item in the list
        for item in p_list:
            # if item is not in the file
            if (linksFileContent.__contains__(item) == False):
                # addd item to file
                file.write(item+"\n")


# downloads image into a folder from a url
def downloadImage(p_url,p_folder,p_userAgent="Mozilla/5.0"):
    # gets image name
    name = p_url.split("/")[-1]
    name = name.strip()
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', p_userAgent)]
    urllib.request.install_opener(opener)

    # finds if there is something after .jpg or .png or .jpeg
    if (name.find(".jpg") != -1):
        name = name.split(".jpg")[0]
        name = name + ".jpg"
    elif (name.find(".png") != -1):
        name = name.split(".png")[0]
        name = name + ".png"
    elif (name.find(".jpeg") != -1):
        name = name.split(".jpeg")[0]
        name = name + ".jpeg"
    elif (name.find(".GIF") != -1):
        name = name.split(".GIF")[0]
        name = name + ".GIF"
    elif (name.find(".webp") != -1):
        name = name.split(".webp")[0]
        name = name + ".webp"
    else:
        name = name + ".jpg"
    # strips names from \n
    name = name.strip()
    p_url = p_url.strip()
    # downloads image
    try:
        try:
            # decides if there is already a file with the same name in the folder
            with open(p_folder+"/"+name, "r") as file:
                print("image already exists")
                file.close()
        except IOError as e:
            # if file does not exist, downloads it
                urllib.request.urlretrieve(p_url, p_folder+"/"+name)
    except Exception as e:
        print(name)
        print(e)

# saves which line to start from in the file
def saveWhichLineToStartFrom(p_lineNo):
    with open(LINKS_FILE_PATH, "r+") as file:
        rest = file.readlines()[1:]
        file.seek(0)
        file.write(str(p_lineNo)+"\n")
        file.writelines(rest)


#=========================================================================================================
# main
#=========================================================================================================

def main():
   
    #! scrapes links from a discord channel, python imgScrape.py getlinks
    if len(sys.argv) > 1 and sys.argv[1] == "getlinks":
        scrapeLinks(TARGET_URL,TARGET_CLASS)
   
    #! gets every link from the file created by the scrapeLinks function, python imgScrape.py download
    if len(sys.argv) > 1 and sys.argv[1] == "download":
        with open(LINKS_FILE_PATH, "r") as file:
            # first line in the file should be an int showing which line to start from
            start = int(file.readline())
            # reads all links from start
            linksFileContent = file.readlines()[start:]
          
            for url in linksFileContent:
                try:
                    downloadImage(url,IMGS_FOLDER_PATH) # for every link in  downloads the image into a folder
                    print(str(start)+". url finished downloading")
                    # increments start
                    start = start + 1; 
        
                except Exception as e:
                    # if erno 403 saves 
                    if (e.errno == 403):
                        saveWhichLineToStartFrom(start)
                    print("error occured: "+str(e))
            file.close()
            print("done")
            exit(333)


if __name__ == "__main__":
    main()
