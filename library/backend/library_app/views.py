from rest_framework import viewsets
from .models import Author, Genre, Book, Review, Order
from .serializers import (
    AuthorSerializer, GenreSerializer, BookSerializer,
    ReviewSerializer, OrderSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").prefetch_related("genres")
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "book")
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        book_id = self.request.query_params.get("book")
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self._get_user())

    def _get_user(self):
        from django.contrib.auth.models import User
        if self.request.user.is_authenticated:
            return self.request.user
        return User.objects.get_or_create(username="guest")[0]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user", "book")
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        from django.contrib.auth.models import User
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = User.objects.get_or_create(username="guest")[0]
        serializer.save(user=user)
