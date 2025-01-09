from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView,TemplateView
from django.utils.decorators import method_decorator
from .models import PhotoPost
from .forms import PhotoPostForm 
from accounts.forms import  CustomUser
from accounts.forms import CustomUserEditForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# 投稿関連のビュー
class IndexView(ListView):
    template_name = 'index.html'
    model = PhotoPost
    context_object_name = 'posts'
    paginate_by = 5
    queryset = PhotoPost.objects.order_by('-posted_at')

    def post(self, request, *args, **kwargs):
        form = PhotoPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # ログイン中のユーザーを設定

            # アイコンと自己紹介をユーザーの情報から設定
            post.icon = request.user.icon  # ユーザーのアイコンを設定
            post.introduction = request.user.introduction  # ユーザーの自己紹介を設定

            post.save()  # 投稿を保存
            return redirect('index')
        return render(request, self.template_name, {'form': form})



# hi_light/views.py
class ProfileView(ListView):
    template_name = 'profile.html'
    context_object_name = 'profiles'
    model = PhotoPost

    def get_queryset(self):
        return PhotoPost.objects.filter(user=self.request.user).order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # ユーザー情報を取得
        latest_photos = PhotoPost.objects.filter(user=self.request.user).order_by('-posted_at')
        
        context['profile'] = user  # ユーザー情報をテンプレートに渡す
        context['photos'] = latest_photos  # ユーザーの最新投稿を渡す
        return context



@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    form_class = PhotoPostForm
    template_name = "post_photo.html"
    success_url = reverse_lazy('hi_light:post_done')

    def form_valid(self, form):
        post_data = form.save(commit=False)
        post_data.user = self.request.user  # 現在のユーザーを設定

        # ユーザーのアイコンと自己紹介を表示用に設定
        post_data.icon = self.request.user.icon  # 投稿にユーザーのアイコンを設定（表示用）
        post_data.introduction = self.request.user.introduction  # 投稿にユーザーの自己紹介を設定（表示用）

        post_data.save()  # 投稿を保存
        return super().form_valid(form)


# hi_light/views.py
@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = CustomUser
    fields = ['icon', 'introduction']
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('hi_light:edit_done')

    def get_object(self, queryset=None):
        return self.request.user  # 現在のユーザー情報を取得

    def form_valid(self, form):
        user = form.save(commit=False)  # ユーザー情報を保存
        user.save()  # ユーザー情報を保存

        # ユーザー情報が変更された場合、関連するすべての投稿にアイコンと自己紹介を反映させる
        PhotoPost.objects.filter(user=user).update(icon=user.icon, introduction=user.introduction)

        return super().form_valid(form)


    
    
class PostSuccessView(TemplateView):
    template_name='post_success.html'
    
class EditSuccessView(TemplateView):
    template_name='edit_success.html'
    
class DiscoverView(ListView):
    template_name='discover.html'
    context_object_name = 'posts'
    model = PhotoPost
    queryset = PhotoPost.objects.order_by('-posted_at')

    def post(self, request, *args, **kwargs):
        form = PhotoPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # ログイン中のユーザーを設定

            # アイコンと自己紹介をユーザーの情報から設定
            post.icon = request.user.icon  # ユーザーのアイコンを設定
            post.introduction = request.user.introduction  # ユーザーの自己紹介を設定

            post.save()  # 投稿を保存
            return redirect('index')
        return render(request, self.template_name, {'form': form})


    
    
class DetailView(DetailView):
    template_name='detail.html'
    model = PhotoPost  # ProductPostモデルを使用
    context_object_name = 'record'
    
# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import PhotoPost

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PhotoPost, Like


@login_required
def like_post(request, post_id):
    post = get_object_or_404(PhotoPost, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        post.like_count -= 1
        liked = False
    else:
        post.likes.add(user)
        post.like_count += 1
        liked = True

    post.save()
    print(f"Post {post_id} updated: like_count={post.like_count}, liked={liked}")  # デバッグ用

    return JsonResponse({
        'success': True,
        'like_count': post.like_count,
        'liked': liked,
    })


from django.shortcuts import render
from .models import PhotoPost

from django.db.models import Prefetch

def liked_posts(request):
    if request.user.is_authenticated:
        liked_posts = PhotoPost.objects.filter(likes=request.user).distinct()  # 「いいね」した投稿を取得
    else:
        liked_posts = []
    return render(request, 'liked_posts.html', {'liked_posts': liked_posts})

class notifyView(TemplateView):
    template_name='notifications.html'