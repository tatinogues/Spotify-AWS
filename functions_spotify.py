
import time 
import pandas as pd 
import spotipy 
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


def get_track_data(n_recs, CLIENT_ID, CLIENT_SECRET): 
    '''
    It fetch n_recs for the available genres and searches for tracks features in each genre:
    among them we can find: accousticness, energy, valence, astist_name, track_name, duration_ms, 
    and others
    
    '''
    auth_manager= SpotifyClientCredentials(client_id= CLIENT_ID, client_secret= CLIENT_SECRET)
    sp= spotipy.Spotify(auth_manager= auth_manager)
    
    genres = sp.recommendation_genre_seeds()
    
    # Set number of recommendations per genre
    n_recs = 100


    data_dict = {"id":[], "genre":[], "track_name":[], "artist_name":[],
             "valence":[], "energy":[], "danceability": [], "key": [], 'loudness': [], 
             'speechiness':[], 'acousticness': [], 'instrumentalness':[], 'liveness':[], 
             'tempo':[], "duration_ms": [], "popularity": [], 
             "audio": []}

    for g in genres['genres']:
    
        # Get n recommendations
        recs = sp.recommendations(seed_genres = [g], limit = n_recs)
        recs= recs['tracks']
    
        for track in recs: 
            data_dict["id"].append(track["id"])
            data_dict["genre"].append(g)
            data_dict["track_name"].append(track['name'])
            data_dict["duration_ms"].append(track['duration_ms'])
            data_dict["popularity"].append(track['popularity'])
            data_dict['audio'].append(track['preview_url'])
        
            #Nombre del artista
            track_meta = sp.track(track["id"])
            data_dict["artist_name"].append(track_meta['artists'][0]['name'])
        
            ##Track detalles de la cancion
            track_features = sp.audio_features(track['id'])
            data_dict["valence"].append(track_features[0]['valence'])
            data_dict["energy"].append(track_features[0]['energy'])
            data_dict["danceability"].append(track_features[0]['danceability'])
            data_dict["key"].append(track_features[0]['key'])
            data_dict["loudness"].append(track_features[0]['loudness'])
            data_dict['speechiness'].append(track_features[0]['speechiness'])
            data_dict['acousticness'].append(track_features[0]['acousticness'])
            data_dict['instrumentalness'].append(track_features[0]['instrumentalness'])
            data_dict['liveness'].append(track_features[0]['liveness'])
            data_dict['tempo'].append(track_features[0]['tempo'])
        

            # Wait 0.2 seconds per track so that the api doesnt overheat
            time.sleep(0.2)
 
    # Store data in dataframe
    df = pd.DataFrame(data_dict)

    print('df generado ok')

    # Drop duplicates
    df.drop_duplicates(subset = "id", keep = "first", inplace = True)
    return df 
    

    