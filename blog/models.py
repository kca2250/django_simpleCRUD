from django.db import models
from django.urls import reverse_lazy


class Tag(models.Model):
    tags = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.tags


class Category(models.Model):
    category = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.category


class Post(models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="タイトル"
    )

    body = models.CharField(
        max_length=99999,
        blank=False,
        null=False,
        verbose_name="内容",
        help_text="HTMLは使えません。"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="作成日"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="最終更新日"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="カテゴリー"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="タグ"
    )

    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])

    def __str__(self):
        return self.title
