from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import *
from faker import Faker
import random
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import  cache


# Create your views here.


# 首页
def index(request):
    parallel_results = userinfo.objects.filter(roles='普通用户').values('username', 'password', 'name',
                                                                                     'phone', 'address', 'roles')
    parallelrs = []
    for i in parallel_results:
        parallelrs.append(i)
    parallel_users =  random.choices(parallelrs,k=2)
    parallel_attack_user = parallel_users[0]['username']
    parallel_victim_user = parallel_users[1]['username']

    vertical_victim_user = userinfo.objects.filter(roles='管理员')[0].username

    return render(request,"index.html",locals())

def unauthorized_access(request):
    if request.method =='GET':
        username = request.GET.get("username")
        role = request.GET.get("role")
        operation = request.GET.get("operation")
        password = request.GET.get("password")
        phone = request.GET.get("phone")
        address = request.GET.get("address")
        #未授权访问
        if username ==None:
            results = userinfo.objects.all().values('username','password','name','phone','address','roles')
            rs = []
            for i in results:
                rs.append(i)
            return  JsonResponse(rs,safe=False)
        #平行越权
        elif len(username)>0 and role==None:
            #水平越权-查看用户信息
            if operation==None:
                results = userinfo.objects.filter(roles='普通用户').filter(username=username).values('username', 'password', 'name', 'phone', 'address', 'roles')
                rs = []
                for i in results:
                    rs.append(i)
                return  JsonResponse(rs,safe=False)
            #水平越权-修改用户信息
            elif operation =='edit':
                try:
                    rs = userinfo.objects.get(username=username)
                    if password!=None:
                        rs.password=password
                    if phone!=None:
                        rs.phone=phone
                    if address!=None:
                        rs.address=address
                    rs.save()
                    return JsonResponse({"msg": "成功更新用户信息：" + username})
                except:
                    return JsonResponse({"msg": "没有这条记录"})
            elif operation=='del':
                try:
                    userinfo.objects.get(username=username).delete()
                    return JsonResponse({"msg": "成功删除用户："+username})
                except:
                    return JsonResponse({"msg":"没有这条记录"})
            else:
                return JsonResponse({})
            #水平越权-删除用户信息


        #垂直越权
        elif len(username)>0 and role!=None:
            # 垂直越权-查看用户信息
            if operation == None:
                results = userinfo.objects.filter(roles=role).filter(username=username).values('username', 'password', 'name', 'phone', 'address', 'roles')
                rs = []
                for i in results:
                    rs.append(i)
                return JsonResponse(rs, safe=False)

            #垂直越权-修改用户信息
            elif operation =='edit':
                try:
                    rs = userinfo.objects.get(username=username)
                    if password!=None:
                        rs.password=password
                    if phone!=None:
                        rs.phone=phone
                    if address!=None:
                        rs.address=address
                    rs.roles=role
                    rs.save()
                    return JsonResponse({"msg": "成功更新用户信息：" + username})
                except:
                    return JsonResponse({"msg": "没有这条记录"})
            # 垂直越权-删除用户
            elif operation=='del':
                try:
                    userinfo.objects.get(username=username).delete()
                    return JsonResponse({"msg": "成功删除用户："+username})
                except:
                    return JsonResponse({"msg":"没有这条记录"})
            elif operation =='promotion':
                try:
                    users = userinfo.objects.get(username=username)
                    users.roles = role
                    users.save()
                    return JsonResponse({"msg": "更新成功："+username})
                except:
                    return JsonResponse({"msg":"没有这条记录"})
            else:
                return JsonResponse({})
@csrf_exempt
def shopping(request):
    if request.method =='GET':
        name = request.GET.get("name")
        username = request.GET.get("username")
        try:
            money = userinfo.objects.get(username=username).money
        except:
            return JsonResponse({"msg":"用户名不存在"})
        if name==None and username!=None:
            results = commodityinfo.objects.all().values('name', 'price', 'limit')
            rs = []
            for i in results:
                rs.append(i)
            return render(request,'shop.html',locals())

    elif request.method=='POST':
        username = request.GET.get("username")
        name = request.POST.get("name")
        price = request.POST.get("price")
        num = request.POST.get("num")
        userrs = userinfo.objects.get(username=username)
        money = userrs.money
        cmrs = commodityinfo.objects.get(name=name)
        limit = cmrs.limit
        if int(num)>limit:
            return JsonResponse({"msg":"超过商品限制"})

        total = int(num)*float(price)
        if total> money:
            return JsonResponse({"msg":"你的金额不够"})

        userrs.money = money-total
        userrs.save()
        cmrs.limit = limit-int(num)
        cmrs.save()
        return JsonResponse({"msg":"购买成功！！！"})


#初始化数据
def init_data(request):
    if request.method == 'GET':
        faker1 = Faker()
        faker2 = Faker("zh_CN")
        #用户数据初始化
        userinfo.objects.all().delete()
        roles = ['管理员','普通用户','客服人员']
        for i in range(0,1000):
            userinfo.objects.create(
                username=faker1.name(),
                password=faker2.password(),
                name=faker2.name(),
                phone=faker2.phone_number(),
                address=faker2.address(),
                roles=random.choice(roles)
            )


        #商品数据初始化
        commodityinfo.objects.all().delete()
        for i in range(0,10):
            commodityinfo.objects.create(
                name=faker1.city(),
                price = random.randint(1,100),
                limit = random.randint(1,100)
            )

        return HttpResponse("初始化成功")

def msg_code(request):

    phone = request.GET.get("phone")
    attack_type = request.GET.get("attack_type")
    rcode = request.GET.get("code")
    code = random.randint(100000,999999)
    if attack_type == 'horizontal':
        cache.set(f'phone_{phone}', code,None)
        return JsonResponse({"msg":"手机号："+phone+" 短信发送成功"})

    elif attack_type =='vertical':
        code_status = cache.get(f'phone_{phone}')
        if code_status==None:
            cache.set(f'phone_{phone}', code,60)
            return JsonResponse({"msg": "手机号："+phone+" 短信发送成功"})
        else:
            return JsonResponse({"msg": "手机号："+phone+" 需要等待一分钟才可以再次发送"})

    elif attack_type=='leak':
        return JsonResponse({"msg":"手机号："+phone+" 短信发送成功","code":f"{code}"})

    elif attack_type=='nofail':
        code = cache.get(f'phone_{phone}')
        print()
        try:
            if int(rcode)==int(code):
                return JsonResponse({"msg":"短信验证码校验成功","code":200})
            else:
                return JsonResponse({"msg":"校验错误","code":0,"real_code":code})
        except:
            return JsonResponse({"msg":"请去获取短信验证码","code":200})
    elif attack_type=='noauth':
        code = cache.get(f'phone_{phone}')

        try:
            if rcode==None:
                return JsonResponse({"msg": "短信验证码校验成功", "code": 200})

            if rcode==code:

                return JsonResponse({"msg":"短信验证码校验成功","code":200})
            else:
                return JsonResponse({"msg":"校验错误","code":0,"real_code":code})
        except:
            return JsonResponse({"msg": "请去获取短信验证码", "code": 200})

    elif attack_type == 'constant':

        if rcode == '888888':
            return JsonResponse({"msg": "短信验证码校验成功", "code": 200})

        if rcode == code:

            return JsonResponse({"msg": "短信验证码校验成功", "code": 200})
        else:
            return JsonResponse({"msg": "校验错误", "code": 0, "real_code": code})


    return HttpResponse("")
    #cache.set('my_key', 'hello, world!', 30)

def register(request):
    if request.method=='GET':
        attack_type = request.GET.get("attack_type")
        phone = request.GET.get("phone")
        username = request.GET.get("username")
        password = request.GET.get("password")

        if attack_type=='arbitrarily':

            try:
                ct = userinfo.objects.filter(phone=phone).count()
                if ct >0:
                    return JsonResponse({"code":0,"msg":"该用户已经注册"})
                else:
                    userinfo.objects.create(
                        username=username,
                        phone=phone,
                        password=password,
                    )
                    return JsonResponse({"code": 200, "msg": "用户成功注册！！"})
            except Exception as e :
                userinfo.objects.create(
                    username=username,
                    phone=phone,
                    password=password,
                )



        elif attack_type=='cover':
            userinfo.objects.create(
                username=username,
                phone=phone,
                password=password,
            )
            return JsonResponse({"code": 200, "msg": "用户成功注册！！"})

        elif attack_type=='cover_check':
            rs = userinfo.objects.filter(username=username).order_by("-id").values("id","username","phone","password")[0]
            return JsonResponse({"code": 200, "msg": rs})


def order(request):
    if request.method=='GET':
        operation = request.GET.get("operation")
        username = request.GET.get("username")
        cname = request.GET.get("cname")
        userrs= userinfo.objects.get(username=username)
        money = userrs.money
        crs = commodityinfo.objects.get(name=cname)
        price = crs.price
        userrs.money = money-price
        userrs.save()


        if operation=='buy':
            pass
        elif operation == 'revoke':
            pass