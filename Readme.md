# This is a practice project of Django

May まえだ あつこ bless me

![](./media/niko.jpg)

[まえだ あつこ](<https://baike.baidu.com/item/%E5%89%8D%E7%94%B0%E6%95%A6%E5%AD%90/9928563?fr=aladdin>)

####1. FormTrap 
   ```python
   form = CategoryForm(request)
   
   #Djanao 2.0 以后
   form = CategoryForm(request.POST)
   ```

####2. _url_ to _path_ and _re_path_
   
   ```python
   url('^add_category/$',views.add_category,name= 'add_category')
   url('^category/(?P<category_name_slug>[\w\-]+)/$',
         views.show_category,name = 'show_category')
   
   #Djanao 2.0 以后
   path('add_category/',views.add_category,name= 'add_category')
   re_path('category/(?P<category_name_slug>[\w\-]+)/',
            views.show_category,name = 'show_category')
   ```
   
####3. **register** _tag_

   自定义模板标签，使用时报以下错误
   
   ```shell
   TemplateSyntaxError at /my_customer_tags/
   'admin_tags' is not a registered tag library. Must be one of:
   admin_list
   admin_modify
   admin_static
   admin_urls
   cache
   custom_tags
   i18n
   kingadmin_tags
   l10n
   log
   static
   staticfiles
   tz
   ```
   
   解决方法：在proj.settings中做如下设置
   
   ```python
   TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [TEMPLATE_DIR,],
       'APP_DIRS': True,
       'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
         
            #注意这里添加的libraries为注册的标签，然后重启服务器
            #manage.py runserver
            'libraries': {
                'rango_template_tags':'rango.templatetags.rango_template_tags',
               }
        },
   },
   ]
    
   ```
    
   添加标签后要重启服务器
    
   ```shell
   python manage.py runserver
   ```
    
   **使用help可以查看django的命令**
   
   ```shell
   python manage.py help
   ```