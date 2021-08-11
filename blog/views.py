from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.models import Post


# 一覧表示
class Index(ListView):
    model = Post


# 詳細表示
class Detail(DetailView):
    model = Post


# 新規作成
class Create(CreateView):
    model = Post
    fields = ["title", "body", "category", "tags"]


# 編集画面
class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]


# 削除
class Delete(DeleteView):
    model = Post
    success_url = "/"
