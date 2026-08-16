import os
from flask import Flask
from dotenv import load_dotenv
from postgres import Postgres
from anime import anilistAPI

load_dotenv()

app = Flask(__name__)

supabase = Postgres(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

anime = anilistAPI()

@app.route('/')
def index():
    response = supabase.table('instruments').select("*").execute()
    instruments = response.data

    html = '<h1>Instruments</h1><ul>'
    for instrument in instruments:
        html += f'<li>{instrument["name"]}</li>'
    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run(debug=True)