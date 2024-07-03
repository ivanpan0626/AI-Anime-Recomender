# %%
import pandas as pd
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, 'animes.csv')
animes_df = pd.read_csv(csv_file_path)
animes_df = animes_df.drop_duplicates(subset=['uid','title'],keep='first')
animes_df

# %%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

vector = TfidfVectorizer(ngram_range=(1,2))
tfidf = vector.fit_transform(animes_df["title"])

def search(animeTitle):
    query_vec = vector.transform([animeTitle])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indexes = np.argpartition(similarity, -5)[-5:]
    results = animes_df.iloc[indexes][::-1]
    results_subset = results[["popularity", "title", "genre", "img_url", 'synopsis', 'score']]
    return results_subset.to_dict(orient='records')

def searchID(animeTitle):
    query_vec = vector.transform([animeTitle])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indexes = np.argpartition(similarity, -5)[-5:]
    results = animes_df.iloc[indexes][::-1]
    return results

import ipywidgets as widgets
from IPython.display import display

#animes_df_input = widgets.Text(
    #value="",
    #description="Title of Anime",
    #disabled=False
#)

#animes_list = widgets.Output()

#def input(data):
    #with animes_list:
        #animes_list.clear_output()
        #title = data["new"]
        #display(search(title))

#animes_df_input.observe(input, names='value')

#display(animes_df_input, animes_list)

# %%
animes_df.dtypes

# %%
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, 'reviews.csv')
ratings_df = pd.read_csv(csv_file_path)
ratings_df.dtypes

# %%
anime_id = 1575
#Code Geass

commonUsers = ratings_df[(ratings_df["anime_uid"]==anime_id) & (ratings_df["score"] >= 7)]["profile"].unique()

commonUsers_recs = ratings_df[(ratings_df["profile"].isin(commonUsers)) & (ratings_df["score"] >= 7)]["anime_uid"]
commonUsers_recs = commonUsers_recs.value_counts()/len(commonUsers)
commonUsers_recs = commonUsers_recs[(commonUsers_recs > .07) & (commonUsers_recs < 1)]

commonUsers_recs

# %%
allUsers = ratings_df[(ratings_df["anime_uid"].isin(commonUsers_recs.index)) & (ratings_df["score"] >= 7)]
allUsers_recs = allUsers["anime_uid"].value_counts()/len(allUsers["profile"].unique())
allUsers_recs

# %%
recPercent = pd.concat([commonUsers_recs, allUsers_recs], axis=1)
recPercent.columns = ["commonUsers_recs%", "allUsers_recs%"]
recPercent["differential"] = recPercent["commonUsers_recs%"] / recPercent["allUsers_recs%"]
recPercent = recPercent.sort_values("differential", ascending=False)

recPercent

# %%
def similar_animes(animeid):
    commonUsers = ratings_df[(ratings_df["anime_uid"]==animeid) & (ratings_df["score"] >= 7)]["profile"].unique()

    commonUsers_recs = ratings_df[(ratings_df["profile"].isin(commonUsers)) & (ratings_df["score"] >= 7)]["anime_uid"]
    commonUsers_recs = commonUsers_recs.value_counts()/len(commonUsers)
    commonUsers_recs = commonUsers_recs[(commonUsers_recs > .07) & (commonUsers_recs < 1)]

    allUsers = ratings_df[(ratings_df["anime_uid"].isin(commonUsers_recs.index)) & (ratings_df["score"] >= 7)]
    
    allUsers_recs = allUsers["anime_uid"].value_counts()/len(allUsers["profile"].unique())

    recPercent = pd.concat([commonUsers_recs, allUsers_recs], axis=1)
    recPercent.columns = ["commonUsers_recs%", "allUsers_recs%"]
    recPercent["differential"] = recPercent["commonUsers_recs%"] / recPercent["allUsers_recs%"]
    recPercent = recPercent.sort_values("differential", ascending=False)

    top_recs = recPercent.head(10).merge(animes_df, left_index=True, right_on="uid")[["popularity", "title", "genre", "img_url", 'synopsis', 'score']]
    return top_recs.to_dict(orient='records')

# %%
import ipywidgets as widgets
from IPython.display import display

#anime_name = widgets.Text(
    #value='',
    #description='Anime Title:',
    #disabled=False
#)
#animeRec_list = widgets.Output()

#def input(data):
    #with animeRec_list:
        #animeRec_list.clear_output()
        #title = data["new"]
        #if len(title) > 2:
            #results = search(title)
            #animeid = results.iloc[0]["uid"]
            #display(similar_animes(animeid))

#anime_name.observe(input, names='value')

#display(anime_name, animeRec_list)


