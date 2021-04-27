import sys
from os import path
from PyInquirer import prompt
from styles import style
from validator import EmptyValidator, UrlValidator
from selenium import webdriver
from colorama import init, Fore
import webbrowser
from helper import back, screencls, finder_url
from datetime import datetime

def main():
    screencls()
    question = [
        {
            "type": "list",
            "name": "main",
            "message": "Choose",
            "choices": [
                "Download Class",
                "Create issues",
                "Donate",
                "About",
                "Help",
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
                with open("DownloadLinks.txt", "a") as fp:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    fp.write(f"Link: {link}\nDate and Time: {dt_string}\n{30*'='}\n")
                if back():
                    main()
            else:
                print("invalid url")
                if back():
                    main()
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
                with open("DownloadLinks.txt", "a") as fp:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    fp.write(f"Link: {url}\nDate and Time: {dt_string}\n{30*'='}\n")
                if back():
                    main()
            else:
                print("invalid url")
                if back():
                    main()
    elif ans["main"] == "About":
        pass
    elif ans["main"] == "Donate":
        pass
    elif ans["main"] == "Create issues":
        question = [
            {
                "type": "list",
                "name": "report",
                "message": "Choose",
                "choices": [
                    "Bug report",
                    "Feature request"
                ]
            }
        ]
        ans = prompt(question, style=style)
        if ans["report"] == "Bug report":
            webbrowser.open("https://github.com/Epic-R-R/Sadjad-Uni/issues/new?assignees=Epic-R-R&labels=bug&template=bug_report.md&title=")
        elif ans["report"] == "Feature request":
            webbrowser.open("https://github.com/Epic-R-R/Sadjad-Uni/issues/new?assignees=&labels=&template=feature_request.md&title=")
    elif ans["main"] == "Help":
        print(f"""
        {Fore.GREEN}Download Class:
            {Fore.LIGHTGREEN_EX}Get download link: {Fore.BLUE}give you link for download class video and save into DownloadLinks.txt file, 
                                    after download you must login into your account in vu.sadjad.ac.ir then use link for download
            {Fore.LIGHTGREEN_EX}Open browser and download: {Fore.BLUE}Automatic open your browser and login into your account then download video

        {Fore.GREEN}Create issues:
            {Fore.LIGHTGREEN_EX}Bug report: {Fore.BLUE}If you found a bug in code, you can report the bug and we fix it in next version
            {Fore.LIGHTGREEN_EX}Feature request: {Fore.BLUE}If you want to add a new feature, you can report to us through this option
        """)
        if back():
            main()
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
    init(autoreset=True)
    main()