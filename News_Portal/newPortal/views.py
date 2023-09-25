from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from .tasks import *
from django.core.cache import cache


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('post:post_list')


class PostList(ListView):
    paginate_by = 10
    model = Post
    template_name = 'postt.html'
    context_object_name = 'post'
    ordering = '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset().filter(post_type='news')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newPortal.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    raise_exception = True


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newPortal.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

