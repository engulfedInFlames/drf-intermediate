from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    public = models.BooleanField(default=True)

    class Meta:
        verbose_name = "회원"
        verbose_name_plural = "회원 리스트"

    def __str__(self) -> str:
        return self.username
