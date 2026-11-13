from rest_framework import serializers
from .models import Author, Genre, Book, Review, Order


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "birth_year"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "book", "user", "rating", "text", "created_at"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source="genres",
        write_only=True, many=True, required=False
    )

    class Meta:
        model = Book
        fields = [
            "id", "title", "description", "year", "price", "stock",
            "author", "author_id", "genres", "genre_ids", "created_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Order
        fields = ["id", "user", "book", "quantity", "status", "created_at"]
