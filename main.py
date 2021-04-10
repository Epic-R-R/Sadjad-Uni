from selenium import webdriver
from os import path


def finder_url(link):
    st = link.find("url")
    fst = st + 4
    st = st+3
    active = True
    while active:
        if link[st] == "&":
            active = False
            continue
        st += 1

    complete = link[fst:st]
    return(complete)


def main():
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\LENOVO\Desktop\sajad uni\Sadjad-Uni\webdriver\chromedriver.exe')
    username = "96440153"
    password = "Ss_13774635"
    # username = input("Enter username: ")
    # password = input("Enter password: ")
    link = input("please enter link : ")
    driver.get(link)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
    url = finder_url(link)
    driver.get(
        f"https://vc2.sadjad.ac.ir/{url}/output/class{url}.zip?download=zip")
    active = True
    while active:
        if path.isfile(f'C:\\Users\\LENOVO\\Downloads\\class{url}.zip'):
            active = False


if __name__ == "__main__":
    main()
