from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = 'https://www.bbcgoodfoodme.com'

titles_list = []
links_list = []
Nutrition_list = []

for i in range(1, 8):
    url = f'https://www.bbcgoodfoodme.com/collections/middle-eastern/page/{i}/'

    r = requests.get(url)
    page_contents = r.text
    doc_type = BeautifulSoup(page_contents, 'html.parser')

    titles = doc_type.findAll('h4', class_='entry-title')

    for title in titles:
        link_tag = title.find('a')
        link = link_tag['href']
        title_text = link_tag.text

        titles_list.append(title_text)
        links_list.append(link)

        link_r = requests.get(link)
        link_contents = link_r.text
        link_doc_type = BeautifulSoup(link_contents, 'html.parser')
        Nutrition_element = link_doc_type.find('ul', class_='nutrition-list clearfix')

        if Nutrition_element:
            nutrition_items = Nutrition_element.find_all('li')
            nutrition_dict = {}
            for item in nutrition_items:
                fact_name = item.find('div', class_='text').find('span').text
                fact_value = item.find('div', class_='text').find('span', class_='number').text
                nutrition_dict[fact_name] = fact_value
            nutrition_text = '\n'.join([f"{fact}: {value}" for fact, value in nutrition_dict.items()])
        else:
            nutrition_text = "Nutrition information not found"

        Nutrition_list.append(nutrition_text)

df = pd.DataFrame({'Title': titles_list, 'Ingerdients': Nutrition_list, 'Link': links_list})
print(df)

excel_file_path = 'Food_Items3.xlsx'

df.to_excel(excel_file_path, index=False)

print(f'DataFrame has been saved to {excel_file_path}')
