import logging
from sqlite3 import IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Car, Favorite
from .serializers import CarSerializer
from rest_framework import generics, status
from django.db.models import Q


class CarListView(ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        queryset = Car.objects.all()
        search_query = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_mileage = self.request.query_params.get('min_mileage')
        max_mileage = self.request.query_params.get('max_mileage')
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        if search_query:
            queryset = queryset.filter(
                Q(marka__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(body_type__icontains=search_query) |
                Q(transmission__icontains=search_query)
            )

        # if marka:
        #     queryset = queryset.filter(marka__icontains=marka)
        # if model:
        #     queryset = queryset.filter(model__icontains=model)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_mileage:
            queryset = queryset.filter(mileage__gte=min_mileage)
        if max_mileage:
            queryset = queryset.filter(mileage__lte=max_mileage)
        if min_year:
            queryset = queryset.filter(year__gte=min_year)
        if max_year:
            queryset = queryset.filter(year__lte=max_year)

        return queryset


class CarDetailView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


logger = logging.getLogger(__name__)


class CreateCarView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут создавать посты

    def perform_create(self, serializer):
        # Логируем пользователя, который пытается создать пост
        logger.debug(f"Creating car for user: {self.request.user}")
        serializer.save(user=self.request.user)  # Сохраняем пользователя как автора поста

    def create(self, request, *args, **kwargs):
        # Логируем данные запроса для отладки
        logger.debug(f"Request data: {request.data}")
        return super().create(request, *args, **kwargs)


@api_view(['POST'])
def add_to_favorites(request):
    car_id = request.data.get('car_id')
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        car = Car.objects.get(id=car_id)
        # Проверяем, существует ли уже такая запись в избранных
        favorite_exists = Favorite.objects.filter(user=user, car=car).exists()
        if favorite_exists:
            return Response({'message': 'Car is already in favorites'}, status=status.HTTP_409_CONFLICT)

        Favorite.objects.create(user=user, car=car)
        return Response({'success': 'Car added to favorites'})
    except Car.DoesNotExist:
        return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Добавляем более общий обработчик исключений для отладки
        logger.error(f"Error in add_to_favorites: {e}")
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_favorites(request):
    car_id = request.data.get('car_id')
    car = Car.objects.get(id=car_id)
    Favorite.objects.filter(user=request.user, car=car).delete()
    return Response({'status': 'removed from favorites'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    cars = [favorite.car for favorite in favorites]
    serializer = CarSerializer(cars, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    posts = Car.objects.filter(user=request.user)
    serializer = CarSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    posts = Car.objects.filter(user=request.user)
    serializer = CarSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)