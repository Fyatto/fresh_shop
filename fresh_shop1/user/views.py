from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from fresh_shop.settings import ORDER_NUMBER
from goods.models import Goods
from order.models import OrderInfo
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 使用表单form做校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 账号不存在于数据库，密码和确认密码一直，邮箱格式正确
            username = form.cleaned_data['user_name']
            pwd = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username, password=pwd, email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 获取表单验证不通过的错误信息
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 用户名存在，密码正确
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        # 删除session中的键值对,user_id
        del request.session['user_id']
        # 删除商品的信息
        if request.session.get('goods'):
            del request.session['goods']
        if request.session.get('nums'):
            del request.session['nums']
        return HttpResponseRedirect(reverse('goods:index'))


def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        activate = 'site'
        return render(request, 'user_center_site.html', {'user_address': user_address, 'activate': activate})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id, address=address,
                                       signer_name=username, signer_mobile=mobile,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors': errors})


def user_info(request):
    if request.method == 'GET':
        goods_list = []
        good_id = request.session.get('nums')
        if good_id:
            for goods_id in good_id:
                goods_list.append(Goods.objects.filter(pk=goods_id).first())
        activate = 'info'
        return render(request, 'user_center_info.html', {'goods_list': goods_list, 'activate': activate})


def user_order(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        # 获取登陆系统用户的id值
        user_id = request.session.get('user_id')
        # 查询当前用户产生的订单信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        # 分页
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        activate = 'order'
        return render(request, 'user_center_order.html', {'orders': orders, 'status': status, 'activate': activate})
