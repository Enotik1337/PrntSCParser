import random
import string
import time
import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
HEADERS = {"User-Agent": USER_AGENT}
BASE_URL = "https://prnt.sc/"
SAVE_FOLDER = "images"
DELAY = 0.1

# Создать папку, если её нет
import os
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def generate_random_code():
    length = random.randint(6, 8)
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_image_url(page_url):
    response = requests.get(page_url, headers=HEADERS)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    img_tag = soup.find("img")
    if img_tag and "src" in img_tag.attrs:
        img_url = img_tag["src"]
        if img_url.startswith("https://"):
            return img_url
    return None

def download_image(img_url, code):
    try:
        img_data = requests.get(img_url, headers=HEADERS).content
        file_path = os.path.join(SAVE_FOLDER, f"{code}.jpg")
        with open(file_path, "wb") as img_file:
            img_file.write(img_data)
        print(f"[+] Downloaded: {file_path}")
    except Exception as e:
        print(f"[-] Error downloading {img_url}: {e}")

def main():
    while True:
        code = generate_random_code()
        page_url = BASE_URL + code
        print(f"[*] Checking: {page_url}")
        img_url = get_image_url(page_url)
        if img_url:
            download_image(img_url, code)
        else:
            print("[-] No image found.")
        time.sleep(DELAY)  # Чтоб не забанили мгновенно

if __name__ == "__main__":
    main()