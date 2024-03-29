from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = dict(categories=category_list,
                        pages=page_list)

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['last_visit'] = request.session['last_visit']
    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        # 检索关联的所有网页
        # 注意，filter() 返回一个网页对象列表或空列表

        pages = Page.objects.filter(category=category).order_by('-views')

        # 把得到的列表赋值给模板上下文中名为pages 的键

        context_dict['pages'] = pages

        # 也把从数据库中获取的category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在

        context_dict['category'] = category

    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在

        context_dict['category'] = None
        context_dict['pages'] = None
        # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    # 是HTTP POST 请求吗？
    if request.method == 'POST':
        form = CategoryForm(request.POST)  # Django 2.0 change

        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return index(request)
        else:
            print(form.errors)

    # 渲染表单，并显示可能出现的错误消息
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.view = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


# # user register
# def register(request):
#     # register flag
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             # calculate password
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             registered = True
#
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'rango/register.html',
#                   dict(user_form=user_form,
#                        profile_form=profile_form,
#                        registered=registered))


# def user_login(request):
#     if request.method == 'POST':
#         # Get username and password
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse('还没有成为好闺蜜呢')
#         else:
#             print("无法进入：{0},{1}".format(username, password))
#             return HttpResponse("用户名或者密码不存在")
#     else:
#         return render(request, 'rango/login.html', {})

@login_required
def like_category(request):
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
        if cat_id:
            cat = Category.objects.get(id= int(cat_id))
            if cat:
                likes= cat.likes+1
                cat.likes= likes
                cat.save()
        return HttpResponse(likes)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def track_url(request):
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)
