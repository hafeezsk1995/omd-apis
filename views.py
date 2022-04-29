
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Movie
import requests

omdb_key = "f70d32bf"

# Create your views here.



class GetMovieByTitle(APIView):
    def get(self,request):
        try:
            title = self.request.GET.get('t')
            movie_obj = Movie.objects.filter(title=title).values('title').first()
            if not movie_obj:
                omdb_data = requests.get(f'http://www.omdbapi.com/?apikey={omdb_key}&t={title}')
                omdb_data = omdb_data.json()
                # print("got json data")
                if omdb_data and 'Title' in omdb_data:
                    genres = list(omdb_data['Genre'].split(','))
                    print("genres",genres)
                    Movie.objects.create(title=omdb_data['Title'],released_year=omdb_data['Year'],rating=omdb_data['imdbRating'],generes=genres)
                    movie_obj = Movie.objects.filter(title=title).values('title').first()
            return Response({"Title":movie_obj['title']},status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=status.HTTP_400_BAD_REQUEST)  



class GetMovieById(APIView):
    def get(self,request,pk):
        try:
            movie_obj = Movie.objects.filter(pk=pk).values().first()
            if not movie_obj:
                return Response({"Error":f"Movie object is not found with given id {pk}"},status=status.HTTP_404_NOT_FOUND)
            return Response(movie_obj,status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=status.HTTP_400_BAD_REQUEST) 


class GetMovieByYear(APIView):
    def get(self,request):
        try:
            year = self.request.GET.get('year')
            movie_obj = Movie.objects.filter(released_year=year).values().first()
            if not movie_obj:
                return Response({"Error":f"Movie object is not found with given year {year}"},status=status.HTTP_404_NOT_FOUND)
            return Response(movie_obj,status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class GetMoviesByGivenHigherRating(APIView):
    def get(self,request):
        try:
            rating = self.request.GET.get('rating')
            movie_obj = Movie.objects.filter(rating__gt=rating).values()
            if not movie_obj:
                return Response({"Error":f"Movie objects is not found with higher than given ratings {rating}"},status=status.HTTP_404_NOT_FOUND)
            return Response(movie_obj,status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=status.HTTP_400_BAD_REQUEST)



class GetMoviesByGenres(APIView):
    def get(self,request):
        try:
            genres = self.request.GET.get('genres')
            #movie_obj = Movie.objects.filter(generes__in=genres).values()
            movie_data = Movie.objects.all()
            movies_lst = []
            for obj in movie_data:
                for gen in obj.generes:
                    if gen.lower() == genres.lower():
                        res = Movie.objects.get(pk=obj.id)
                        movies_lst.append({
                            "id":res.id,
                            "title":res.title,
                            "released_year":res.released_year,
                            "rating":res.rating,
                            "generes":res.generes
                        })
            return Response(movies_lst,status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"Error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
