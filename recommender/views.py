from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from scipy.sparse import issparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'recommender_data')
TFIDF = joblib.load(os.path.join(DATA_DIR, 'tfidf_vectorizer.pkl'))
ENCODER = joblib.load(os.path.join(DATA_DIR, 'onehot_encoder.pkl'))
FEATURES = joblib.load(os.path.join(DATA_DIR, 'book_features_matrix.pkl'))
METADATA = joblib.load(os.path.join(DATA_DIR, 'books_metadata.pkl'))

class RecommendBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        book_ids = data.get('book_ids')
        top_n = int(data.get('top_n', 10))

        if not book_ids or not isinstance(book_ids, list) or not all(isinstance(b, int) for b in book_ids):
            return Response({'error': 'Передайте book_ids: список id книг'}, status=400)

        indices = METADATA.index[METADATA['book_id'].isin(book_ids)].tolist()
        if not indices:
            return Response({'error': 'Не найдено ни одной книги из списка'}, status=404)

        mean_vector = FEATURES[indices].mean(axis=0)

        if issparse(mean_vector):
            mean_vector = mean_vector
        else:
            mean_vector = np.array(mean_vector).reshape(1, -1)

        similarities = cosine_similarity(FEATURES, mean_vector).flatten()

        results = METADATA.copy()
        results['similarity'] = similarities

        recommended = results[~results['book_id'].isin(book_ids)] \
            .sort_values(by='similarity', ascending=False) \
            .head(top_n)

        return Response(recommended[['book_id', 'title', 'similarity']].to_dict(orient='records'))
