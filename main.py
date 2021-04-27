import sys
from os import path
from PyInquirer import prompt
from styles import style
from validator import EmptyValidator, UrlValidator
from download import finder_url
from selenium import webdriver
from colorama import init, Fore

def main():
    question = [
        {
            "type": "list",
            "name": "main",
            "message": "Choose",
            "choices": [
                "Download Class",
                "Donate",
                "About",
                "Exit"
            ]
        },
    ]
    ans = prompt(question, style=style)
    if ans["main"] == "Download Class":
        choose = [
            {
                "type": "list",
                "name": "choice",
                "message": "Options",
                "choices": [
                    "Get Download link",
                    "Open browser and download"
                ]
            }
        ]
        ans = prompt(choose, style=style)
        if ans["choice"] == "Get Download link":
            getlink = [
                {
                "type": "input",
                "name": "link",
                "message": "Enter Class Link:",
                "validate": EmptyValidator
                }
            ]
            ans = prompt(getlink, style=style)
            if UrlValidator(ans["link"]) is not None:
                link = f'https://vc2.sadjad.ac.ir/{finder_url(ans["link"])}/output/{finder_url(ans["link"])}.zip?download=zip'
                print(f"{Fore.GREEN}Download Link : {Fore.BLUE}{link}")
            else:
                print("invalid url")
                sys.exit(0)
        elif ans["choice"] == "Open browser and download":
            accountInfo = [
                {
                    "type": "input",
                    "name": "username",
                    "message": "Enter Username:",
                    "validate": EmptyValidator,
                },
                {
                    "type": "password",
                    "name": "password",
                    "message": "Enter Password:",
                    "validate": EmptyValidator,
                },
                {
                    "type": "input",
                    "name": "classlink",
                    "message": "Enter Class Link:",
                    "validate": EmptyValidator
                }
            ]
            accountinformation = prompt(accountInfo, style=style)
            if UrlValidator(accountinformation["classlink"]) is not None:
                driver = webdriver.Chrome(
                    executable_path=r'./webdriver/chromedriver')
                driver.get(accountinformation["classlink"])
                driver.find_element_by_xpath('//*[@id="username"]').send_keys(accountinformation["username"])
                driver.find_element_by_xpath('//*[@id="password"]').send_keys(accountinformation["password"])
                driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
                url = finder_url(accountinformation["classlink"])
                downloadurl = f"https://vc2.sadjad.ac.ir/{url}/output/{url}.zip?download=zip"
                driver.get(downloadurl)
            else:
                print("invalid url")
                sys.exit(0)
    elif ans["main"] == "About":
        pass
    elif ans["main"] == "Donate":
        pass
    elif ans["main"] == "Exit":
        confirm = [
                {
                    "type": "confirm",
                    "message": "Do you want to exit?",
                    "name": "exit",
                    "default": False,
                },
            ]
        ans = prompt(confirm, style=style)
        if ans["exit"]:
            sys.exit(0)
        else:
            main()

if __name__ == "__main__":
    init(autoreset=True)  # Colorama autoreset terminal color True
    main()