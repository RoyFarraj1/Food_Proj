from bs4 import BeautifulSoup
import requests
import pandas as pd


base_url = 'https://www.bbcgoodfoodme.com'

titles_list = []
links_list = []
ingredients_list=[]

for i in range(1, 6):
    url = f'https://www.bbcgoodfoodme.com/collections/asian/page/{i}/'
    
    
    r =requests.get(url)
    page_contents=r.text
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
        ingredients_element = link_doc_type.find('h3', class_='bubble')
        
        if ingredients_element:
            ingredients = ingredients_element.find_next('ul').findAll('li')
            ingredients_text = '\n'.join([ingredient.get_text() for ingredient in ingredients])
        else:
            ingredients_text = "Ingredients not found"
        
        ingredients_list.append(ingredients_text)


df = pd.DataFrame( {'Title':titles_list, 'Ingerdients':ingredients_list,'Link':links_list})
print(df)

excel_file_path = 'Food_Items3.xlsx'

df.to_excel(excel_file_path, index=False)


print(f'DataFrame has been saved to {excel_file_path}')
  
    
   


    
    
