from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, GenreViewSet, BookViewSet,
    ReviewViewSet, OrderViewSet,
)

router = DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("genres", GenreViewSet)
router.register("books", BookViewSet)
router.register("reviews", ReviewViewSet)
router.register("orders", OrderViewSet)

urlpatterns = router.urls
