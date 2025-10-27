import requests 
import pandas as pd
base_url="https://rickandmortyapi.com/api/"
endpoint="character"



def get_characters_per_page(base_url,endpoint,page):
    characters_data=[]
    try:
        response=requests.get(f"{base_url}{endpoint}?page={page}")
        response.raise_for_status()  # Raise an error for HTTP errors
        data=response.json()
        for character in data["results"]:
            characters_data.append({
                "id": character["id"],
                "name": character["name"],
                "episodes_count": len(character["episode"])
            })
        return characters_data
    except requests.RequestException as e:
        print(f"Error fetching characters: {e}")
        return {"error": str(e)}

def get_number_of_pages(base_url,endpoint):
    try:
        response=requests.get(f"{base_url}{endpoint}")
        response.raise_for_status()
        data=response.json()
        return data['info']['pages']
    except requests.RequestException as e:
        print(f"Error fetching number of pages: {e}")
        return 0

def get_full_characters_data(base_url, endpoint):
    full_characters_data=[]
    total_pages=get_number_of_pages(base_url,endpoint)
    for page in range(1,total_pages+1):
        page_data=get_characters_per_page(base_url,endpoint,page)
        full_characters_data.extend(page_data)
    return full_characters_data

def convert_to_csv():
    df=pd.DataFrame(get_full_characters_data(base_url,endpoint))
    df.to_csv("rick_and_morty_characters.csv",index=False)

convert_to_csv()