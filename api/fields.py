from rest_framework import serializers


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        ret = {
            'name': value.name,
            'slug': value.slug
        }
        return ret


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        ret = {
            'name': value.name,
            'slug': value.slug
        }
        return ret
