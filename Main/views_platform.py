from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect
from Finance.settings import UPLOAD_DIR
from Main.models import File

from Main.views import ren2res
from Main.views import paginate
from Main.models import *

@login_required
def upload(req):
    if req.method == 'GET':
        return ren2res("platform/upload.html", req)
    elif req.method == 'POST':
        print("get")
        print(req.FILES)
        files = req.FILES.getlist('file')
        for f in files:
            print("ok")
            try:
                destination = open(UPLOAD_DIR + str(f.name), 'wb+')
                for chunk in f.chunks():
                    destination.write(chunk)
                    destination.close()
                submit = File(name=f, uid_id=req.user.id, path=UPLOAD_DIR)
                submit.save()
            except:
                return ren2res("platform/upload.html", req, {'err': "文件上传失败"})
        return ren2res("platform/upload.html", req, {'info': "上传成功"})

@login_required
def download(req):
    # 工作开始的地方
    return

@login_required
def list(req):
    if req.method == 'GET':
        f=File.objects.all()
        return ren2res("platform/files_list.html", req, paginate(req, f))




