from pandas import DataFrame
import pandas as pd
from typing import cast
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ServiceTFIDF:

    def __init__(self) -> None:
        self.docs_index = ['doc 1', 'doc_2', 'doc_3','doc_4','doc_5']
        self.corpus_df : DataFrame | None = None
        self.vectorize : TfidfVectorizer | None= None
        self.matrix_corpus = None
        # Get the corpus
        corpus_df = pd.read_csv(BASE_DIR / ".." / "assets" / "corpus.csv", delimiter="\r\n", names=['text'])
        corpus_df['document'] = self.docs_index
        corpus_df.set_index("document",drop=True)

        self.corpus_df = corpus_df
        self.vectorize = TfidfVectorizer(smooth_idf=False)
        self.matrix_corpus = self.vectorize.fit_transform(corpus_df.text)
        self.table_tf_idf = pd.DataFrame(self.matrix_corpus.toarray(),index=[self.docs_index],columns=self.vectorize.get_feature_names_out())

    
    def getScoreTFIDF(self, query:str):
        print("Calling tfidf")
        vectorize = cast(TfidfVectorizer,self.vectorize)
        rank_result = {}
        corpus = list(vectorize.get_feature_names_out())
        
        for doc in self.docs_index:
            rank_result[doc] = 0
            for term in query.split():
                # Check apakah query yg di cari ada di dalam 
                if term in corpus:
                    nTfIdf = self.table_tf_idf.loc[doc,term].item()
                    rank_result[doc] += nTfIdf

        # Create df Ranking
        result_rangking = pd.DataFrame({"doc":rank_result.keys(),"score":rank_result.values()})
        result_rangking.sort_values(by=['score'], ascending=False, inplace=True)
        result_merge = result_rangking.merge(self.corpus_df[['text','document']], left_on="doc", right_on="document",)
        result_merge.drop(columns=['document'], inplace=True)
        return result_merge.to_html()
    
    def getScoreCosineSimiliarity(self, query:str):
        print("Calling cosine")
        result_consine=[]
        vectorLocal = cast(TfidfVectorizer,self.vectorize)
        vector_query = vectorLocal.transform([query])

        localCorpusDf = cast(DataFrame,self.corpus_df)

        score = cosine_similarity(vector_query, self.matrix_corpus).flatten()
        rank_index_cosine = score.argsort()[::-1]

        for a in rank_index_cosine:
            result_consine.append({'doc':localCorpusDf.loc[a]['document'],'score':score[a],'text':localCorpusDf.loc[a]['text']})

        return pd.DataFrame(result_consine).to_html()