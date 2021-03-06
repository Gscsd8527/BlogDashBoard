from django.shortcuts import render, redirect, reverse
from .models import User, ArticlePost, CommentModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login

def Index(request):
    """
    主页
    :param request:
    :return:
    """
    questions =  ArticlePost.objects.all().order_by('-create_time')
    user = request.user
    # print(user, type(user))
    # print(user.username, type(user.username), len(user.username))
    if not len(user.username):
        user = None
    return render(request, 'index.html', context={'user': user, 'questions': questions})

def Login(request):
    """
    登录界面
    :param request:
    :return:
    """

    # print('path= ', request.path)
    next_url = request.GET.get('next')
    # print('next_url= ', next_url)


    if request.method == 'GET':
        return render(request, 'user/login.html', context={'user': None, 'next_url': next_url})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        if not all([id, username, password]):
            context = {
                'error_msg': '参数不全'
            }
            return render(request, 'user/login.html', context=context)
        else:
            user = User.objects.filter(username=username, password=password).first()
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url, context={'user': user})
                questions = ArticlePost.objects.all().order_by('-create_time')
                return render(request, 'index.html', context={'user': user, 'questions': questions})
            else:
                return render(request, 'user/login.html', context={'error_msg': '用户名密码不存在，请先注册'})

def Register(request):
    """
    注册界面
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/register.html', context={'user': None})
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'user/register.html', context={
                'error_msg': '两次密码不相等，请核对后再填写！'
            })
        else:
            user = User()
            user.username = username
            user.password = password1
            user.save()
            return render(request, 'index.html', context={'user': user})


def Logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    # request.session.pop('user_id')
    # del request.session['user_id']
    # request.session.clear()
    logout(request)
    return redirect(reverse('user:index'))

# from util.decorator import login_required

@login_required
def MyBlog(request):
    """
    展示我的博客
    :param request:
    :return:
    """
    # user_id = request.session.get('user_id', False)
    user = request.user
    user_id = user.id
    # print('user_id= ', user_id)
    if user_id:
        username = User.objects.filter(pk=user_id).first()
        # print('username= ', username)
        questions = ArticlePost.objects.filter(author_id=user_id).order_by('-create_time')
        return render(request, 'user/myblog.html', context={'user': username, 'questions': questions})
    else:
        return render(request, 'user/login.html')
    # else:
    #     # response = redirect('/login/')
    #     return render(request, 'user/login.html')


def WriteBlog(request):
    """
    写博客
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/writeblog.html')
    else:
        user = request.user
        user_id = user.id
        title = request.POST.get('title')
        content = request.POST.get('content')
        ArticlePost.objects.create(title=title, content=content, author_id=user_id)
        questions = ArticlePost.objects.all()
        return render(request, 'user/myblog.html', {'questions': questions})


def Detail(request):
    """
    显示文章详情
    :param request:
    :return:
    """
    user = request.user
    if not len(user.username):
        user = None
    question_id = request.GET.get('question_id', 1)
    request.session['question_id'] = question_id
    question = ArticlePost.objects.filter(id=question_id).first()
    Comment = CommentModel.objects.filter(question_id=question).order_by('-create_time')
    return render(request, 'user/detail.html', context={'user': user, 'question': question, 'Comment': Comment})

@login_required
def AddComment(request):
    """
    添加评论
    :param request:
    :return:
    """
    if request.method == 'POST':
        content = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        # print('content = ', content)
        # print('post_id = ', post_id)
        user = request.user
        Comment = CommentModel()
        Comment.content = content
        Comment.question_id = ArticlePost.objects.filter(pk=post_id)[0]
        Comment.author_id = User.objects.filter(username=user)[0]
        Comment.save()
        # 评论完成还是当前页面
        question = ArticlePost.objects.filter(id=post_id).first()

        Comment = CommentModel.objects.filter(question_id=question).order_by('-create_time')
        return render(request, 'user/detail.html', context={'question': question, 'user': user, 'Comment': Comment})
    else:
        user = request.user
        question_id = request.session['question_id']
        question = ArticlePost.objects.filter(pk=question_id).first()
        return render(request, 'user/detail.html', context={'question': question, 'user': user})


