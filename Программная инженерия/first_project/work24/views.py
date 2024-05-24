from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .forms import PostSearchForm
from .models import Post
# Create your views here.

class HomeView(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return "work24/components/post-list-elements.html"
        return "work24/index.html"
    
def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status="published")
    related = Post.objects.filter(author=post.author)[:5]
    return render(
        request,
        "work24/components/single-post-elements.html",
        {"post": post, "related": related},
    )


class PostSearchView(HomeView):
    form_class = PostSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Post.objects.filter(title__icontains=form.cleaned_data["q"])

    def get_template_names(self):
        if self.request.htmx:
            return "work24/components/search-list-elements.html"
        return "work24/search.html"