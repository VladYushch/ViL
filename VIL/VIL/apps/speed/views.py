import datetime

import speedtest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import sys, time, io, requests
from .forms import SizeForm,ServerChoise,WorkMode
from .models import Measurement
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count,Q
from django.utils import timezone
size =0

def homepage(request):
    return render(request, 'base.html')

def workmode(request):
    return render(request,"speed/genspeed.html")
def manualtest(request):
    ser = ServerChoise(request.POST or None)
    if request.method == "POST":
        if ser.is_valid():
            a=ser.cleaned_data
            if a=={'serverchoise':'1'}:
                servers=[8633]
                return sptest(request,servers)
            elif a=={'serverchoise':'2'}:
                servers = [38783]
                return sptest(request,servers)
    return render(request,'speed/testdown.html',{'form':ser})

def autotest(request):
    servers = []
    return sptest(request,servers)
def sptest(request,servers):
    threads=None
    s = speedtest.Speedtest()
    s.get_servers(servers)
    #s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    results_dict = s.results.dict()
    dsp1= float(results_dict.get('download'))/(1024*1024)
    usp1= float(results_dict.get('upload'))/(1024*1024)
    ping1=float(results_dict.get('ping'))
    servid = results_dict.get('server').get('id')
    print(str(servid))
    link=(results_dict.get('share'))
    resoutput =str("Download speed: "+f'{dsp1:.2f}'+"Mbps\nUpload speed: "+f'{usp1:.2f}'+'Mbps\nPing: '+f'{ping1}'+'ms\nServer ID '+f'{servid}')
    if request.user.is_authenticated==True:
            user = request.user
            user.measurement_set.create(dsp=dsp1,usp=usp1,ping=ping1,servid=servid)
    else:
            a=Measurement(dsp=dsp1,usp=usp1,ping=ping1,servid=servid)
            a.save()

    return render(request,'speed/result.html',{'resoutput':resoutput})

def dtest(request):
    form = SizeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            a=form.cleaned_data
            print(a)
            if a =={'sizechoise': '1'}:
                size = 5
                return down5(request, size)
            else:
                size = 10
                return down5(request,size)


    return render(request, 'speed/testdown.html',{'form': form})


def down5(request,size):
    print('1')
    if size ==5:
        url = f"https://github.com/yourkin/fileupload-fastapi/raw/a85a697cab2f887780b3278059a0dd52847d80f3/tests/data/test-5mb.bin"
    elif size ==10:
        url = f"https://github.com/yourkin/fileupload-fastapi/raw/main/tests/data/test-10mb.bin"
    with io.BytesIO() as f:
        start = time.perf_counter()
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None: # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(30 * dl / int(total_length))
                sys.stdout.write("\r[%s%s] %s Mbps" % ('=' * done, ' ' * (30-done), dl//(time.perf_counter() - start) / 100000))
        speed = dl/(time.perf_counter()-start)/100000
        restime = (time.perf_counter() - start)
        resoutput =str(size) + "MB \t"+str(f'{restime:.2f}')+" seconds\t"+str("Speed"+f'{speed:.2f}'+"Mbps")
        if request.user.is_authenticated==True:
            user = request.user
            print('1')
            user.measurement_set.create(dsp=speed)
        else:
             a=Measurement(dsp=speed)
            #a.save()




    return render( request , 'speed/result.html', {'resoutput': resoutput})
def historyprint(request):
    context = {
        'historyprint': Measurement.objects.filter(tester=request.user)
    }
    return render(request,"profile/profile.html",context)



# Create your views here.
