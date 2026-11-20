from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .library_app.models import Author, Genre, Book, Review, Order


class AuthorAPITest(APITestCase):
    def test_create_author(self):
        url = reverse("author-list")  # имя роута от DefaultRouter
        payload = {"name": "Иван Иванов", "bio": "Писатель", "birth_year": 1980}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.first().name, "Иван Иванов")

    def test_create_author_without_birth_year(self):
        """birth_year опционален — null должен проходить."""
        url = reverse("author-list")
        payload = {"name": "Без года", "bio": "", "birth_year": None}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_list_authors(self):
        Author.objects.create(name="A1")
        Author.objects.create(name="A2")
        resp = self.client.get(reverse("author-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # если у вас пагинация — results, иначе просто список
        data = resp.data.get("results", resp.data) if isinstance(resp.data, dict) else resp.data
        self.assertEqual(len(data), 2)


class GenreAPITest(APITestCase):
    def test_create_genre(self):
        url = reverse("genre-list")
        resp = self.client.post(url, {"name": "Фантастика"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 1)

    def test_create_genre_empty_name_fails(self):
        url = reverse("genre-list")
        resp = self.client.post(url, {"name": ""}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_genres(self):
        Genre.objects.create(name="Детектив")
        resp = self.client.get(reverse("genre-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class BookAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Автор")
        self.genre = Genre.objects.create(name="Роман")

    def test_create_book_with_author_id_and_genre_ids(self):
        url = reverse("book-list")
        payload = {
            "title": "Книга",
            "description": "Описание",
            "year": 2020,
            "price": "199.99",
            "stock": 10,
            "author_id": self.author.id,
            "genre_ids": [self.genre.id],
        }
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        book = Book.objects.get()
        self.assertEqual(book.author_id, self.author.id)
        self.assertEqual(book.genres.count(), 1)

    def test_list_books_returns_nested_author(self):
        Book.objects.create(
            title="Книга", author=self.author,
            year=2020, price="100.00", stock=1,
        )
        resp = self.client.get(reverse("book-list"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data.get("results", resp.data) if isinstance(resp.data, dict) else resp.data
        self.assertEqual(data[0]["author"]["name"], "Автор")


class ReviewAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="x")
        self.author = Author.objects.create(name="Автор")
        self.book = Book.objects.create(
            title="Книга", author=self.author,
            year=2020, price="100.00", stock=1,
        )

    def test_create_review_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("review-list")
        payload = {"book": self.book.id, "rating": 5, "text": "Отлично"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        review = Review.objects.get()
        self.assertEqual(review.user, self.user)

    def test_filter_reviews_by_book(self):
        Review.objects.create(user=self.user, book=self.book, rating=4, text="ok")
        url = reverse("review-list") + f"?book={self.book.id}"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="x")
        self.author = Author.objects.create(name="Автор")
        self.book = Book.objects.create(
            title="Книга", author=self.author,
            year=2020, price="100.00", stock=5,
        )

    def test_create_order_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        payload = {"book": self.book.id, "quantity": 1, "status": "new"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().user, self.user)