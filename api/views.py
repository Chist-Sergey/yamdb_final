from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilterBackend
from .models import Category, Genre, Review, Title
from .permissions import IsAdminOrReadOnlyPermission, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerWithRating)


class CustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all().order_by('id')
    permission_classes = (IsAdminOrReadOnlyPermission,)
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all().order_by('id')
    permission_classes = (IsAdminOrReadOnlyPermission,)
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    permission_classes = (IsAdminOrReadOnlyPermission,)
    serializer_class = TitleSerializer
    filterset_class = TitleFilterBackend

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerWithRating
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review,
                                   title=title,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review,
                                   title=title,
                                   id=self.kwargs.get('review_id'))
        serializer.save(review=review)
