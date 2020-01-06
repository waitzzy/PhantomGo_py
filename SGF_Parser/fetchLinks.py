from bs4 import BeautifulSoup
f = open('u-go.net.html', 'r')
html=f.read()
soup=BeautifulSoup(html,"html.parser")
for link in soup.find_all('a'):
    if 'zip' in link.get('href'):
        print(link.get('href'))