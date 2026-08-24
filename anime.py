import requests
import json

# API documentation: https://docs.anilist.co/

class anilistAPI:
    def __init__(self):
        self.url = 'https://graphql.anilist.co'


    def cleanDescription(self, description:str) -> str:
        return description.split("<br>")[0]


    def cleanDate(self, startDate: dict) -> str:
        return f"{startDate["month"]}/{startDate["year"]}"
    

    def getAnimeByID(self, id: int) -> tuple[int, dict]: 
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
        if response.status_code == 200:
            jsonData = response.json()["data"]["Media"]
            jsonData["description"] = self.cleanDescription(jsonData["description"])
            jsonData["startDate"] = self.cleanDate(jsonData["startDate"])
        else:
            jsonData = response.json()["errors"]

        # with open("byId.json", "w") as file:
        #     json.dump(jsonData, file)

        return response.status_code, jsonData


    def browseAnimeByName(self, name: str) -> tuple[int, list[dict]]:
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
        
        # with open("browse.json", "w") as file:
        #     json.dump(response.json()["data"]["Page"]["media"], file)

        if response.status_code == 200:
            return response.status_code, response.json()["data"]["Page"]["media"]
        else: 
            return response.status_code, response.json()["errors"]

        # Retrieves all shows from user's show info in database
    def retrieveAllShowInfoFromUser(self, showIDs:list[dict]) -> tuple[int, list[dict]]:
        try:
            result = []
            for show in showIDs:
                showInfo = self.getAnimeByID(show["show_id"])
                result.append(showInfo[1])
            return 200, result
        except Exception as e:
            print("General error:", e)
            return 400, [{"error": e}]


if __name__ == "__main__":
    animeAPI = anilistAPI()
    # print(animeAPI.getAnimeByID(20920))
    animeAPI.browseAnimeByName("Call of the Night")
