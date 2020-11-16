import os
import sys
import time
import requests
import shutil
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='driver/chromedriver')


def get_img_urls(slides_live_id):
    img_url_list = []
    source_url = 'https://slideslive.com/{}'.format(slides_live_id)
    print('Crawling slides on `{}`'.format(source_url))
    driver.get(source_url)
    while True:
        # Get url of current page image
        slide_content = driver.find_element_by_class_name('slp__slidesPlayer__content')
        img = slide_content.find_element_by_tag_name('img')
        img_source = img.get_attribute('src')
        if img_url_list and img_url_list[0] == img_source:
            break
        img_url_list.append(img_source)
        # Next page
        try:
            next_button = driver.find_element_by_class_name('slp__bigButton--next')
            next_button.click()
        except ElementClickInterceptedException:
            close_button = driver.find_element_by_class_name('presentation-overlay__close')
            close_button.click()
            time.sleep(2)
            next_button = driver.find_element_by_class_name('slp__bigButton--next')
            next_button.click()
        # WebDriverWait(driver, 10, 0.2).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, 'slp__slidesPlayer__content')))
        time.sleep(2.5)
    print(img_url_list)
    return img_url_list, driver.title


def download_img(slides_live_id, img_url_list):
    img_folder = 'slide_{}'.format(slides_live_id)
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    img_file_list = []
    for idx, url in enumerate(img_url_list):
        img_name = '{}/{}.jpg'.format(img_folder, idx)
        img_file_list.append(img_name)
        if os.path.exists(img_name):
            continue
        print('downloading slide_38926923:', idx)
        response = requests.get(url, stream=True)
        with open(img_name, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    return img_file_list


def merge_img(img_file_list, title):
    im0 = Image.open(img_file_list[0])
    im_list = [Image.open(img_name) for img_name in img_file_list[1:]]
    pdf = title + '.pdf'
    im0.save(pdf, "PDF", resolution=100.0, save_all=True, append_images=im_list)


def download(slides_live_id):
    img_url_list, title = get_img_urls(slides_live_id)
    img_file_list = download_img(slides_live_id, img_url_list)
    merge_img(img_file_list, title)
    print('PDF {} downloaded.'.format(title))


if __name__ == '__main__':
    slides_id = sys.argv[1]
    download(int(slides_id))
