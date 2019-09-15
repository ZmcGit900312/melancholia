from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = dict(categories=category_list,
                        pages=page_list)
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        # 检索关联的所有网页
        # 注意，filter() 返回一个网页对象列表或空列表

        pages = Page.objects.filter(category=category)

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
