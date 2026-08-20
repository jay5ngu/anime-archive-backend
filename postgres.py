import os
from dotenv import load_dotenv
from supabase import create_client, Client
import bcrypt
from postgrest.exceptions import APIError
from anime import anilistAPI

# Load variables from the .env file into the system environment
load_dotenv()

class Postgres:
    def __init__(self, url, key):
        self.supabase: Client = create_client(url, key)
        self.animeAPI = anilistAPI()

    def _encryptPassword(self, password: str) -> str:
        # Convert string to bytes (bcrypt requires byte inputs)
        passwordBytes = password.encode('utf-8')

        # Generate salt
        salt = bcrypt.gensalt(rounds=12)
        
        # Hash the password
        hashedPassword = bcrypt.hashpw(passwordBytes, salt)

        # Convert bytes to string (database cannot store type bytes)
        return hashedPassword.decode("utf-8")

    def _decryptPassword(self, hashedPassword:str, userInput:str) -> str:
        userInputBytes = userInput.encode('utf-8')
        hashedPasswordBytes = hashedPassword.encode("utf-8")

        # checkpw reads the salt directly out of the hashed_password string
        return bcrypt.checkpw(userInputBytes, hashedPasswordBytes)


    def createUser(self, firstName:str, lastName:str, email:str, password:str) -> bool:
        try:
            encryptedPassword = self._encryptPassword(password)
            response = self.supabase.table("users").insert({"first_name": firstName, "last_name": lastName, "password": encryptedPassword, "email": email}).execute()
            return len(response.data) != 0
        except APIError as e:
            print("Error when creating new user:", e)
            return False
        except Exception as e:
            print("General error:", e)
            return False


    def retrieveUser(self, email: str, password:str) -> bool:
        try:
            response = self.supabase.table("users").select("password").eq("email", email).execute()
            if len(response.data) == 0:
                print("Error when retrieving user: Email does not exist")
                return False
            else: 
                dbPassword = response.data[0]["password"]
                return self._decryptPassword(hashedPassword=dbPassword, userInput=password)
        except APIError as e:
            print("Error when retrieving user:", e)
            return False


    def updateUser(self, userID:int, firstName:str=None, lastName:str=None, email:str=None, password:str=None):
        pass


    def deleteUser(self, userID:int):
        pass

    """
    ### Create this database if I want to store the info from the anime api into my own database for better retrieval
    
    def createShow(self, showID:int, title:str, description:str, image:str):
        pass

    def updateShow(self, showID:int, title:str, description:str, image:str):
        pass

    def deleteShow(self, user_id:int, show_id:int):
        pass
    
    """

    def addShowToUser(self, showID:int, userID:int) -> bool:
        try:
            response = self.supabase.table("user_shows").insert({"show_id": showID, "user_id": userID}).execute()
            return (len(response.data)) != 0
        except Exception as e:
            print(e)
            return False

    def removeShowFromUser(self, showID:int, userID:int) -> bool:
        pass

    def retrieveAllShowIDsFromUser(self, userID:int) -> list[dict]:
        response = self.supabase.table("user_shows").select("show_id").eq("user_id", userID).execute()
        return response.data

    def retrieveAllShowInfoFromUser(self, userID:int) -> list[dict]:
        showIDs = self.retrieveAllShowIDsFromUser(userID)
        result = []
        for show in showIDs:
            result.append(self.animeAPI.getAnimeByID(show["show_id"]))
        return result


if __name__ == "__main__":
    # Retrieve the values using os.getenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SECRET_KEY")

    pg = Postgres(url, key)

    # Test creating new user
    # userCreated = pg.createUser(firstName="Test", lastName="User", email="test@gmail.com", password="test1234")
    # print(userCreated)

    # Test retrieving user (for sign in)
    # print(pg.retrieveUser("test@gmail.com", "test1234"))

    # Test assigning show to user
    # pg.addShowToUser(151807, 9)

    # Test retrieving all user show ids
    # print(pg.retrieveAllShowIDsFromUser(9))

    # Test retrieving all user show info
    print(pg.retrieveAllShowInfoFromUser(9))
