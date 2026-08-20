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
    response = anime.browseAnimeByName(name=title)
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
    response = supabase.retrieveAllShowInfoFromUser(userID=data["user_id"])
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)