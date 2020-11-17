from readability import Document
import requests

response = requests.get('http://localhost:63342/qartnewsurfer/onge-1.html?_ijt=j20v6is0m12glfk2oek935unob')
doc = Document(response.text)
print(doc.title())
print(doc.summary())
# 'full_title': doc.title()
