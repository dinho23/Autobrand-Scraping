import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('4196436573.xml')
root = tree.getroot()

ns = {'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
      'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'}

invoice_line = root.find('.//cac:InvoiceLine', ns)

item_name = invoice_line.find('.//cbc:Name', ns).text
unit_quantity = invoice_line.find(
    './/cbc:InvoicedQuantity', ns).text.lstrip('-')
item_code = invoice_line.find(
    './/cac:SellersItemIdentification/cbc:ID', ns).text
item_price = invoice_line.find('.//cbc:PriceAmount', ns).text

# item_name = item_name.lstrip(f'{item_code} ')

data = {
    "Denumire Produs:": [item_name],
    "Cantitate:": [unit_quantity],
    "Cod Produs:": [item_code],
    "Pret Unitar:": [item_price]
}

df = pd.DataFrame(data)
df.to_excel('invoice_from_xml.xlsx', index=False)
