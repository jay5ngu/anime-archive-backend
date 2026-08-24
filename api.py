import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from postgres import Postgres
from anime import anilistAPI

load_dotenv()

# Initialize Flask server
app = Flask(__name__)

# Initialize supabase database
supabase = Postgres(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SECRET_KEY")
)

# Initialize anime api
anime = anilistAPI()

@app.route('/search/<title>', methods=['GET'])
def search(title:str):
    data : tuple[int, list[dict]] = anime.browseAnimeByName(name=title)
    if data[0] == 200:
        response = {
            "success": True,
            "status": data[0],
            "message": "Search results retrieved successfully.",
            "data": data[1]
            # "timestamp": "2026-08-22T18:46:00Z"
        }
    else:
        response = {
            "success": False,
            "status": data[0],
            "message": "Search result unsuccessful.",
            "data": data[1]
        }
    return jsonify(response)

@app.route('/addShow', methods=['POST'])
def addShow():
    """
    Request Body:
    user_id: int
    show_id: int
    """
    data = request.get_json()
    response = supabase.addShowToUser(showID=data['show_id'], userID=data['user_id'])
    if response:
        return jsonify({'status' : 201})

    return jsonify({'status' : 400})

@app.route('/myShowsInfo', methods=['POST'])
def allUserShows():
    """
    Request Body:
    user_id: int
    """
    data = request.get_json()
    supaResult = supabase.retrieveAllShowIDsFromUser(userID=data["user_id"])
    animeResult = anime.retrieveAllShowInfoFromUser(supaResult)
    if animeResult[0] == 200:
        response = {
            "success": True,
            "status": animeResult[0],
            "message": "User's show info retrieved successfully.",
            "data": animeResult[1]
        }
    else:
        response = {
            "success": False,
            "status": animeResult[0],
            "message": "User's show info unsuccessful.",
            "data": animeResult[1]
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8000)