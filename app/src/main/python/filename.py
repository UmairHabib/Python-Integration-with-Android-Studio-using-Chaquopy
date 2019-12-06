import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def function(file1,file2):
    credits = pd.read_json(file1)
    movies_df = pd.read_json(file2)
    credits_column_renamed = credits.rename(index=str, columns={"movie_id": "id"})
    movies_df_merge = movies_df.merge(credits_column_renamed, on='id')
    movies_cleaned_df = movies_df_merge.drop(columns=['homepage', 'title_x', 'title_y', 'status','production_countries'])

    #W= (Rv + Cm)/(v + m)
    #W is weighted Rating
    #R average for movies as number from 0 to 10 (mean)= Rating
    # v= number of votes for the movies =votes
    #m = minimum votes required to be listed in top 250 out of 3k
    #C = the mean vote across the whole report (currently 6.9)

    v=movies_cleaned_df['vote_count']
    R=movies_cleaned_df['vote_average']
    C=movies_cleaned_df['vote_average'].mean()
    m=movies_cleaned_df['vote_count'].quantile(0.70)

    movies_cleaned_df['weighted_average']=((R*v)+ (C*m))/(v+m)

    #without popularity column
    movie_sorted_ranking=movies_cleaned_df.sort_values('weighted_average',ascending=False)

    #using popularity column too
    scaling=MinMaxScaler()
    movie_scaled_df=scaling.fit_transform(movies_cleaned_df[['weighted_average','popularity']])
    movie_normalized_df=pd.DataFrame(movie_scaled_df,columns=['weighted_average','popularity'])
    movies_cleaned_df[['normalized_weight_average','normalized_popularity']]= movie_normalized_df
    movies_cleaned_df['score'] = movies_cleaned_df['normalized_weight_average'] * 0.5 + movies_cleaned_df['normalized_popularity'] * 0.5
    movies_scored_df = movies_cleaned_df.sort_values(['score'], ascending=False)
    return movies_scored_df[['id','original_title', 'normalized_weight_average', 'normalized_popularity', 'score']].head(20)
