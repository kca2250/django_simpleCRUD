from django.contrib import admin
from django import forms
from django.contrib.admin.forms import AuthenticationForm
from django.contrib.admin import AdminSite
from . import models


class PostTitleFilter(admin.SimpleListFilter):
    title = '本文'
    parameter_name = "body_contains"

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(body__icontains=self.value())
        return queryset

    def lookups(self, request, model_admin):
        return [
            ("本文", "「本文」を含む"),
            ("開発", "「開発」を含む"),
            ("日記", "「日記」を含む"),
        ]


class PostAdminForm(forms.ModelForm):
    class Meta:
        labels = {
            'title': 'ブログタイトル',
        }

    def clean(self):
        body = self.changed_data.get('body')
        if '<' in body:
            raise forms.ValidationError('HTMLタグは使えません')


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    # フォームに関するもの
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = [
        (None, {'fields': ('title',)}),
        ('コンテンツ', {'fields': ('body',)}),
        ('分類', {'fields': ('category', 'tags')}),
        ('メタ', {'fields': ('created_at', 'updated_at')})
    ]
    form = PostAdminForm

    # リスト（一覧）に関するもの
    list_display = ('id', 'title', 'category', 'published', 'tags_summary', 'created_at', 'updated_at')
    list_select_related = ('category',)
    list_editable = ('title', 'category')
    search_fields = ('title', 'category__category', 'tags__tags', "created_at", "updated_at")
    ordering = ('-created_at', "-updated_at")
    list_filter = (PostTitleFilter, 'category', 'tags', 'created_at', 'updated_at')
    actions = ("publish", "unpublish")
    filter_horizontal = ('tags',)

    @staticmethod
    def tags_summary(obj):
        qs = obj.tags.all()
        label = ', '.join(map(str, qs))
        return label

    tags_summary.short_description = "tags"

    # ManyToManyのデータベースの場合この処理をしていると負荷が下がる
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tags')

    # 公開、非公開の状態
    def publish(self, request, queryset):
        queryset.update(published=True)

    publish.short_description = "公開する"

    def unpublish(self, request, queryset):
        queryset.update(published=False)

    unpublish.short_description = "非公開にする"


class PostInline(admin.TabularInline):
    model = models.Post
    fields = ('title', 'body')
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]


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
