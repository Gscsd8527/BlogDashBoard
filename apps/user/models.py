from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class BaseModel(models.Model):
    """
    模型抽象基类
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 指定说明他是一个抽象模型类
        abstract = True



class User(AbstractUser, BaseModel):
    """
    用户模型类
    """
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name



class ArticlePost(models.Model):
    """
    发布的博客
    """
    title = models.CharField(max_length=60, verbose_name="博客名")
    content = models.TextField(verbose_name="文章内容")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True)
    # 文章作者。参数on_delete用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class CommentModel(models.Model):
    content = models.TextField(verbose_name="评论", null=False, blank=False)
    likes = models.IntegerField(u'顶', default=0)
    # user_likes = models.ManyToManyField(User,verbose_name='点赞的人', related_name='comments_liked')
    # comments = GenericRelation('Comment') # 自己对自己的评论, 也就是评论的回复
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    question_id = models.ForeignKey(ArticlePost, verbose_name="文章的id", on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, verbose_name="谁评论的", on_delete=False)

