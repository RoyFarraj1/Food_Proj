import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


driver = webdriver.Chrome()

base_url = 'https://www.bbcgoodfoodme.com'

folder_path = '/Users/carlafarraj/Documents/Food_imgs/asian cuisine'

for i in range(1, 5):
    url = f'https://www.bbcgoodfoodme.com/collections/asian/page/{i}/'
    driver.get(url)
    
    
    page_contents = driver.page_source
    
    
    doc_type = BeautifulSoup(page_contents, 'html.parser')
   
    img_elements = doc_type.find_all('img')
    
    for img in img_elements:
        img_src = img.get('src')
        if img_src and img_src.endswith('.jpg'):
           
            if img_src.startswith('/'):
                img_src = base_url + img_src

            
            img_content = requests.get(img_src).content
            img_name = os.path.basename(img_src)
            img_path = os.path.join(folder_path, img_name)
            
            with open(img_path, 'wb') as img_file:
                img_file.write(img_content)
                print(f'Saved: {img_name}')
    

driver.quit()




