import requests
import json

class anilistAPI:
    def __init__(self):
        self.url = 'https://graphql.anilist.co'


    def cleanDescription(self, description:str) -> str:
        return description.split("<br>")[0]


    def cleanDate(self, startDate: dict) -> str:
        return f"{startDate["month"]}/{startDate["year"]}"
    

    def getAnimeByID(self, id: int) -> dict: 
        query = '''
            query ($id: Int) { # Define which variables will be used in the query (id)
                Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
                    id
                    title {
                    romaji
                    english
                    native
                    }
                    startDate {
                    month
                    year
                    }
                    coverImage {
                    medium
                    large
                    extraLarge
                    color
                    }
                    description
                }
            }
            '''


        # Define our query variables and values that will be used in the query request
        variables = { 'id': id }

        # Make the HTTP Api request
        response = requests.post(self.url, json={'query': query, 'variables': variables})

        # Retrieve and Parse json
        jsonData = response.json()["data"]["Media"]
        jsonData["description"] = self.cleanDescription(jsonData["description"])
        jsonData["startDate"] = self.cleanDate(jsonData["startDate"])

        with open("byId.json", "w") as file:
            json.dump(jsonData, file)

        return jsonData


    def browseAnimeByName(self, name: str) -> list[dict]:
        query = '''
            query ($search: String!) {
                Page {
                    media(search: $search, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    coverImage {
                        medium
                        large
                        extraLarge
                        color
                    }
                    }
                }
            }
        '''

            # Define our query variables and values that will be used in the query request
        variables = {'search': name }

        # Make the HTTP Api request
        response = requests.post(self.url, json={'query': query, 'variables': variables})
        
        with open("browse.json", "w") as file:
            json.dump(response.json()["data"]["Page"]["media"], file)

        return response.json()["data"]["Page"]["media"]

           
    def getAnimeByName(self, name: str) -> dict:
        animeList = self.browseAnimeByName(name)
        if animeList:
            anime = self.getAnimeByID(animeList[0]["id"])
            return anime
        # with open("byName.json", "w") as file:
        #     json.dump(anime, file)

        print("No shows found")
        return None

    def createTestData(self, shows: list[int]) -> list[dict]:
        result = []
        for show in shows:
            result.append(self.getAnimeByID(show))

        with open("myShows.json", "w") as file:
            json.dump(result, file)

        return result

if __name__ == "__main__":
    animeAPI = anilistAPI()
    # animeAPI.getAnimeByID(20920)
    animeAPI.browseAnimeByName("gravity falls")
    # animeAPI.getAnimeByName(" is it wrong to pick up girls in ")
    # animeAPI.createTestData([150672, 151807, 153518, 101280, 196187, 21613, 155907, 126403, 154587, 21827, 21660])