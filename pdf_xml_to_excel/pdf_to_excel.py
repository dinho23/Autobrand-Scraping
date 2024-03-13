from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import pandas as pd

elements_string = ''
for page_layout in extract_pages("AD AUTO TOTAL SRL_20241747776_2024_03_01.PDF"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            elements_string += element.get_text()


elements_list = list(elements_string.split("\n"))

item_name = ''
unit_quantity = ''
item_code = ''
item_price = ''

for index, elem in enumerate(elements_list):
    if elem == "Nume articol/Descriere articol":
        item_name = elements_list[index + 2]
        item_code = elements_list[index + 3]
    elif elem == 'VALOARE TOTALA  fara TVA':
        item_price = elements_list[index + 1].lstrip('-')
    elif elem == ' Cantitate':
        unit_quantity = elements_list[index + 2].lstrip('-')

# item_name = item_name.lstrip(f'{item_code} ')

data = {
    "Denumire Produs:": [item_name],
    "Cantitate:": [unit_quantity],
    "Cod Produs:": [item_code],
    "Pret Unitar:": [item_price]
}

df = pd.DataFrame(data)
df.to_excel('invoice_from_pdf.xlsx', index=False)
