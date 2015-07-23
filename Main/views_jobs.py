from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from Main.views import ren2res
from Main.models import *
from Main.views import paginate
from Main import client

# Create your views here.
# 接受用户请求，读取数据库app表中的应用，将应用作为响应返回给浏览器；如果app表为空，则返回提示信息
@login_required
def choose(req):
    if req.method=='GET':
        if App.objects.exists():
            return ren2res("jobs/choose.html",req,{'apps':App.objects.all()})
        else:
            return ren2res("jobs/choose.html",req,{'info':"抱歉，还没有可用的应用！"})

@login_required
def submit(req,aid):
    # 处理以GET方式发送的请求，请求包含的参数aid代表选择的应用id
    if req.method == 'GET':
        try:
            app = App.objects.get(id=aid)
        except:
            raise Http404
        # 检索数据库，将param表中关联到app表的外键等于aid的项作为响应的参数返回
        params = Param.objects.filter(app=app)
        dict={'app':app,'params':params,'length':params.count()}
        # 在submit.html页面的表单经验证存在为空时又重定向到该方法，因此添加提示信息作为响应的参数
        if req.GET.get("msg"):
            dict.update({'err':"带*的参数不能为空！"})
        return ren2res("jobs/submit.html",req,dict)
    # 处理submit.html页面提交的表单
    elif req.method == 'POST':
        id = req.POST['id']
        params = Param.objects.filter(app=App.objects.get(id=id)).order_by("order")
        # 验证表单提交的数据中不能为空的参数是否为空
        for param in params:
           value=req.POST.get(str(param.order))
           if value.strip()=="" and param.blank==False:
               return HttpResponseRedirect("?msg=err")
        # 将作业信息及有关参数值存入数据库的job表中
        cmd=""
        for param in params:
            cmd += req.POST[str(param.order)]
            cmd += " "
        job=Job(uid=req.user,app=App.objects.get(id=id),cmd=cmd.strip())
        job.save()
        # 调用client的start方法执行这次作业
        client.start(job.id)
        return HttpResponseRedirect("/jobs?page=1&msg=info")

@login_required
def list(req):
    if req.method=='GET':
        # 对于超级用户，返回所有用户提交过的作业信息
        if req.user.is_superuser and Job.objects.all().exists():
            job=Job.objects.all().order_by("-add_time")
        # 对于普通用户，返回该用户自己提交过的作业
        elif Job.objects.filter(uid=req.user).exists():
            job=Job.objects.filter(uid=req.user).order_by("-add_time")
        # 当数据库中不存在历史作业提交记录时返回提示信息
        else:
            return ren2res("jobs/list.html", req, {'info':"没有提交的作业！"})
        # 返回的作业列表经过分页处理，按照请求中的页数返回某一页作业记录
        dict=paginate(req,job)
        if req.GET.get("msg"):
            dict.update({'info':"作业提交成功!"})
        return ren2res("jobs/list.html",req,dict)

@login_required
def detail(req,jid):
    # 返回请求的作业详细信息，请求的参数jid表示作业id
    if req.method=='GET':
        try:
            job=Job.objects.get(id=jid)
        except:
            raise Http404
        dict={'job':job}
        if job.ret is None:
            res="作业还未执行完成！"
            dict.update({'result':res})
        else:
            # 对于已经执行完成的作业，读取结果文件中的执行结果，作为响应的参数返回
            try:
                with open("/result/out_"+jid,"r") as result:
                    res=result.read()
                with open("/result/err_"+jid,"r") as error:
                    err=error.read()
                dict.update({'result':res,'error':err})
            except:
                pass
        return ren2res("jobs/detail.html",req,dict)

# 用于停止某一作业的执行，作业由请求的参数jid指定
def stop(req,jid):
    if req.method=='GET':
        client.stop(jid)



