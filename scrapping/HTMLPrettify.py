from bs4 import BeautifulSoup

with open('scrapping/webdata/data.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

formatted_html = soup.prettify()

with open('scrapping/webdata/formatted_table.html', 'w', encoding='utf-8') as file:
    file.write(formatted_html)

print("Le fichier HTML a été formaté et sauvegardé dans 'formatted_table.html'.")
