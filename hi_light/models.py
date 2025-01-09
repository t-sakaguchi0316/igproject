from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    title = models.CharField(verbose_name='カテゴリー', max_length=100)

    def __str__(self):
        return self.title

class PhotoPost(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=200)
    comment = models.TextField(verbose_name='コメント')
    image1 = models.ImageField(verbose_name='イメージ1', upload_to='photos')
    posted_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PhotoPost, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # ユーザーと投稿の組み合わせがユニークであることを保証
