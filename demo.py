from qartnewsurfer.page_setup import OnGe

page_setup = OnGe
onge = page_setup()
url = onge.get_url(category=0, page=1)
print(url)
# https://on.ge/category/პოლიტიკა?page=150
