import random


from django.db import models
from django.conf import settings

TAG_VALUES = [
    "electronics",
    "cars",
    "cameras",
    "kitchen",
    "stationary",
]


### Django Default Search Engine
# Search results only depends on the target model
# Actually a filtering feature
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = models.Q(title__icontains=query) | models.Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user:
            qs_ = self.filter(user=user).filter(lookup)
            qs = (qs | qs_).distinct()
        return qs


class ProductMangaer(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(
            query,
            user=user,
        )


###


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        null=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    title = models.CharField(max_length=255)
    content = models.TextField(
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=9.99,
    )
    public = models.BooleanField(default=True)

    # ProductManager가 Product 모델에 관한 어떤 퀘리셋에서도 실행 가능하며, public==True인지를 확인
    objects = ProductMangaer()

    class Meta:
        verbose_name = "상품"
        verbose_name_plural = "상품 리스트"

    def __str__(self) -> str:
        return self.title

    @property
    def discounted_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    @property
    def body(self):
        return self.content

    def is_public(self):
        return self.public

    def get_random_tag(self):
        return [random.choice(TAG_VALUES)]
