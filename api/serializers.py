from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User

from .fields import CategoryField, GenreField
from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerWithRating(serializers.ModelSerializer):
    genre = GenreField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )

    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id'))
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на один объект.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
