from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from fresh_shop.settings import GOODS_NUMBER
from goods.models import GoodsCategory, Goods


def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染的首页index.html页面
        # 方法二性能更好
        # 方法一
        # 获取商品分类的元组
        # gcts = GoodsCategory.CATEGORY_TYPE
        # # 获取商品分类的所有对象
        # gcs = GoodsCategory.objects.all()
        # # 获取商品的所有对象
        # gs = Goods.objects.all()
        # return render(request, 'index.html', {'gcs': gcs, 'gs': gs, 'gcts': gcts})
        # 方法二 现在后端对数据进行组装
        gcs = GoodsCategory.objects.all()
        result = []
        for gc in gcs:
            goods = gc.goods_set.all()[:4]
            data = [gc, goods]
            result.append(data)
        gcts = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result, 'gcts': gcts})


def detail(request, id):
    if request.method == 'GET':
        # 返回详情页面解析的商品信息
        g = Goods.objects.get(pk=id)
        return render(request, 'detail.html', {'g': g})
    if request.method == 'POST':
        pass


def recent_browse(request):
    if request.method == 'POST':
        gid = request.POST.get('id')
        good_id = request.session.get('nums')
        if not good_id:
            request.session['nums'] = []
        if gid not in request.session['nums']:
            request.session['nums'].append(gid)
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def goods_list(request, id):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        gc = GoodsCategory.objects.get(pk=id)
        goods = gc.goods_set.all()
        pg = Paginator(goods, GOODS_NUMBER)
        goods = pg.page(page)
        gcs = GoodsCategory.objects.all()
        gcts = GoodsCategory.CATEGORY_TYPE
        return render(request, 'list.html', {'goods': goods, 'gcs': gcs, 'gcts': gcts, 'gc': gc})
