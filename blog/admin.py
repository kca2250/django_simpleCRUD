from django.contrib import admin
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.admin import AdminSite
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class BlogAdminSite(AdminSite):
    site_header = "マイページ"
    site_title = "マイページ"
    index_title = "ホーム"
    site_url = None
    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active


myPage_site = BlogAdminSite(name="myPage")

myPage_site.register(models.Post)
myPage_site.register(models.Tag)
myPage_site.register(models.Category)
