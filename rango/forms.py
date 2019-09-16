from django import forms
from rango.models import Category, Page
from rango.models import UserProfile,User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="请输入分类名字")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # 把这个ModelForms和一个模型连起来
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='请输入网页名字')
    url = forms.URLField(max_length=200, help_text='请输入网址')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        '''想在表单中放哪些字段？
        有时不需要全部字段,有些字段接受空值，因此可能无需显示
        这里我们想隐藏外键字段,为此，可以排除 category 字段
        '''
        exclude = ('category',)
        # field= ('title','url','views')

    def clean(self):
        cleaned_data= self.cleaned_data
        url= cleaned_data.get('url')

        if url:
            cleaned_data['url']= url

        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')