from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import random
import re
def main():
    uname = input("name: ")
    utag = input("tag: ")
    print(playerweight(uname, utag))

def playerweight(uname, utag):
    service = ChromeService(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    user_agents = [
        # Add your list of user agents here
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    #print("Case AND space sensitive. Write everything correctly.")
    #uname = (input("Username? (not the #): ")).replace(" ", "%20")
    #utag = input("Tag? (the #): ")
    unameorig = uname
    uname = unameorig.replace(" ", "%20")
    utag = utag

    link = f"https://tracker.gg/valorant/profile/riot/{uname}%23{utag}/overview"
    print(link)

    driver.get(link)
    
    # Wait for page to load
    while driver.execute_script("return document.readyState") != "complete":
        pass

    html = driver.page_source

    '''
    try:
        with open('yo.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("HTML content successfully written to yo.html")
    except Exception as e:
        print("Error occurred while writing HTML content:", e)
    '''

    result = re.split(r'<div class="label" data-v-5884c23b="">Tracker Score</div><div class="value" data-v-5884c23b="">', html)
    value = int((((result[1])[0:4]).replace(" ","")).replace("<",""))

    #print(value)

    weight = value/1000
    #print(weight)
    driver.quit()

    return unameorig, weight
    # Close browser

if __name__ == "__main__":
    main()
