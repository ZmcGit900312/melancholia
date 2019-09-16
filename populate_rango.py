import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'melancholia.settings')

import django

django.setup()
from rango.models import Category, Page

import random


def populate():
    # 首先创建一些字典，列出想添加到各分类的网页
    # 然后创建一个嵌套字典，设置各分类
    # 这么做看起来不易理解，但是便于迭代，方便为模型添加数据

    love_pages = [
        dict(title='小破站',
             url='https://www.bilibili.com/',
             views=random.randint(1, 1024)),
        dict(title='京东',
             url='https://www.jd.com/',
             views=random.randint(1, 1024)),
        dict(title='淘宝',
             url='https://www.taobao.com/',
             views=random.randint(1, 1024)),
        dict(title='北邮人',
             url='https://bt.byr.cn/torrents.php/',
             views=random.randint(1, 1024)),
        dict(title='抑郁症项目',
             url='https://github.com/ZmcGit900312/melancholia/',
             views=random.randint(1, 1024))
    ]

    django_pages = [
        dict(title='Django Introduction',
             url='https://docs.djangoproject.com/en/2.2/intro/',
             views=random.randint(1, 1024)),
        dict(title='Django Download',
             url='https://www.djangoproject.com/download/',
             views=random.randint(1, 1024)),
        dict(title='Django Project',
             url='https://www.djangoproject.com/',
             views=random.randint(1, 1024))
    ]

    other_pages = [
        dict(title='Pexel(一个自由的照片网站)',
             url='https://www.pexels.com/',
             views=random.randint(1, 1024)),
        dict(title='选老婆的网站',
             url='https://pixivic.com/',
             views=random.randint(1, 1024))
    ]

    cats = dict(
        love=dict(pages=love_pages,
                  likes=random.randint(1, 1024),
                  views=random.randint(1, 1024)),
        django=dict(pages=django_pages,
                    likes=random.randint(1, 1024),
                    views=random.randint(1, 1024)),
        others=dict(pages=other_pages,
                    likes=random.randint(1, 1024),
                    views=random.randint(1, 1024))
    )

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


if __name__ == '__main__':
    print('开始填充.......')
    populate()
    print('填充完毕了')
