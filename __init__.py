# import requests

# response = requests.get("https://api.thecatapi.com/v1/images/search")
# cat_list = response.json()

# print('cat_list: ',cat_list)

# print("url: ",cat_list[0].get("url"))

# from the_cat_api.wet_dry_rest_adapter import RestAdapter
from the_cat_api.wet_dry_rest_adapter import RestAdapter

cat_api =RestAdapter('api.thecatapi.com')
cat_list = cat_api.get('images/search/')
# print("Number of kitten: ",len(cat_list))
# kitty = cat_list.pop()
# print("Kitty url: ", kitty.get("url"))

print(cat_list)