from rest_framework import viewsets, status
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    @action(detail=True,methods=['POST'])
    def rate_movie(self, request, pk=None):
    
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            # print('This is the ID',pk)
            # print('Movie title is', movie.title)
            #creating a static user
            # user = User.objects.get(id=1)
            user = request.user
            print('user: ', user)
            stars = request.data['stars']
            print('user:',user.username)
            try:
                rating = Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars = stars 
                rating.save()
                serializer = RatingSerializer(rating, many = False)
                response =  {'message': 'rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user,movie=movie,stars=stars)
                serializer = RatingSerializer(rating, many = False)
                response =  {'message': 'rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response =  {'message': 'you need to give stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response =  {'message': 'you cannot create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        response =  {'message': 'you cannot update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    