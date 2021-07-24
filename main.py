from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.preprocessing import StandardScaler

from SpotifyAPI import SpotifyAPI

required_features = [
    'Danceability',
    'Energy',
    'Key',
    'Loudness',
    'Speechiness',
    'Acousticsness',
    'Instrumentalness',
    'Liveliness',
    'Valence',
    'Tempo',
    'Duration_ms'
]

loaded_model = joblib.load('knn_model.sav')
loaded_api = SpotifyAPI('831cc784a86e40f7a94913a7760911c1', '9ec69ad406ef4de69d0c52b0becf9eb8')


# Do escape(stuff) on any unsafe stuff to avoid SQL injection

def validate_input(song_features):
    # this should return ALL the missing/invalid features and not just return early.
    for feature in required_features:
        if feature not in song_features:
            return f'{feature} requires a value'

        # have to add validation to makes sure each value is correct.
        if 0 > song_features[feature] or song_features[feature] > 100:
            return f'{feature} value should be between 0 - 100'


def format_input(song_features):
    # create the age variable in days as an integer from release date.
    # can get this from spotify API

    # map it all to a dictionary .. if dict doesn't work then put it in a 1 liner DF

    # song = thedictionary

    # scaled_song = StandardScaler().fit_transform(song)

    # loaded_model.predict_proba(scaled_song)

    return None


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "<p>This is the backend endpoint. do a GET request to /predict with the song features </p>"


@app.route("/predict", methods=['GET'])
def predict():
    song_features = request.args.to_dict()
    error = validate_input(song_features)

    if error:
        return error

    result = loaded_model.predict_proba(format_input(song_features))

    return song_features


@app.route("/autocomplete/<id>", methods=['GET'])
def autocomplete(id):
    response = loaded_api.topFiveTracks(id)

    return response
