""" classes and functions file """
from extensions import cursor
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re


# fetch all the movies
class Movie:
    def __init__(self):
        self.db = cursor.get_collection('movies')
        
    def fetch_movies(self):
        try:
            movies = self.db.find().limit(2000)
            
            if not movies:
                return None
            
            output = []

            for movie in movies:
                output.append({**movie, "_id": str(movie["_id"])})
            
            return output
            
        except Exception as e:
            print(e)
            return
        
    def fetch_recommendations(self, title):
        try:
            recommender = Recommender()
            movies = self.fetch_movies()
            
            print(type(movies))
                        
            if not movies:
                return None
            
            recommended=recommender.get_recommendations(movies, 'score', 'synopsis', title)
            
            print(recommended)
            return recommended
        except Exception as e:
            print(e)
            return None
        
        # recommended movies
        
# recommender class
class Recommender:
    def __init__(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
        
    def remove_tags(sent):
        data = re.compile(r"<.*?>")
        return data.sub("", sent)

    def create_dataframe(self, array):
        """
        <method> To create a pandas dataframe from the array argument

        Args:
            array (list): list of items to be converted to a DataFrame

        Returns:
            <pandas object>: pandas dataframe 
        """ 
            
        df = pd.DataFrame(array)
        df = df.fillna('')
        
        return df
    
    def get_cosine_and_indices(self, df):
        
        tfidf_matrix = self.tfidf.fit_transform(df.synopsis)

        # get the cosine similarity matrix
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # get the indices
        indices = pd.Series(df.index, index=df.title).drop_duplicates()
        

        return {'cosine': cosine_sim, 'indices': indices}
        
    def format_title(self, title):
        """
            Capitalize the entire title
        """
        split = title.split()
        empty = ''
        length = len(split)
        unknown = length - 1
        names = split[:unknown]

        for name in names:
            capital = name.capitalize()
            empty+= capital + ' '
        empty+=split[-1].capitalize()
        return empty
    
    def get_recommendations(self, array, index, label, title):
        """
        <method> Get recommendations for a particle item given the arguments

        Args:
            array (list): list of the items you want to recommend
            index (string): field chosen to be used for indexing e.g title / date / rating
            label (string): field to be used for comparison e.g Description / body /summary
            title (string): title of the movie or item to be recommended

        Returns:
            list: list of recommendations
        """ 

        try:
            df = self.create_dataframe(array)
            item = self.get_cosine_and_indices(df)
            
            idx = item['indices'][title]
            
            print(idx)

            sim_scores = list(enumerate(item['cosine'][idx]))
            sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)

            sim_scores = sim_scores[1:21]
            
            print({'sim':sim_scores})
            
            recommended_indices = [i[0] for i in sim_scores]
            recommended = df.iloc[recommended_indices].to_dict('records')
            
            print({'recommended':recommended})

            return recommended
        except Exception as error: 
            print(error)
            return []
