import datetime

import speedtest
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
import sys, time, io, requests
from .forms import SizeForm,ServerChoise,WorkMode,UserRegistrationForm
from .models import Measurement, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count,Q,Avg
from django.utils import timezone
size =0

def homepage(request):

    t= Measurement.objects.all().count()
    cutoffd = datetime.datetime.now()-datetime.timedelta(days=1)
    cutoffh = datetime.datetime.now()-datetime.timedelta(hours=12)
    d= Measurement.objects.filter(testdata__gt=cutoffd).count()
    h= Measurement.objects.filter(testdata__gt=cutoffh).count()
    context ={
        'statsall':t,
        'statsperday':d,
        'statsper12h':h
    }


    return render(request, 'base.html',context)

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
    idd=0

    if request.user.is_authenticated==True:
            user = request.user
            a=user.measurement_set.create(dsp=dsp1,usp=usp1,ping=ping1,servid=servid)
            idd=a.id
    else:
            a=Measurement(dsp=dsp1,usp=usp1,ping=ping1,servid=servid)
            a.save()
            idd=a.id

    resoutput =str("Download speed: "+f'{dsp1:.2f}'+"Mbps\nUpload speed: "+f'{usp1:.2f}'+'Mbps\nPing: '+f'{ping1}'+'ms\nServer ID '+f'{servid}')
    idd

    return render(request,'speed/result.html',{'resoutput':resoutput,'link':idd})

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
        idd=0

        if request.user.is_authenticated==True:
            user = request.user
            print('1')
            a=user.measurement_set.create(dsp=speed,size=size,time=restime)
            idd=a.id
        else:
             a=Measurement(dsp=speed,size=size,time=restime)
             a.save()
             idd=a.id

        resoutput =str(size) + "MB \t"+str(f'{restime:.2f}')+" seconds\t"+str("Speed"+f'{speed:.2f}'+"Mbps \n \n"+"Your re"
                "sult is available for link 127.0.0.1:8000/result/"+f'{idd}')




    return render( request , 'speed/result.html', {'resoutput': resoutput,'link':idd})
def resulturl(request,result_id):
    try:
        m=Measurement.objects.get(id=result_id)
    except:
        raise Http404("result not found or ttl=0")
    return render(request,"speed/resulturl.html",{"m":m})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

# Create your views here.

from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

@login_required()
def statistics(request):
    m =  Measurement.objects.filter(tester=request.user).count()
    cutoffd = datetime.datetime.now()-datetime.timedelta(days=1)
    cutoffh = datetime.datetime.now()-datetime.timedelta(hours=12)
    d= Measurement.objects.filter(tester=request.user,testdata__gt=cutoffd).count()
    h= Measurement.objects.filter(tester=request.user,testdata__gt=cutoffh).count()
    ddmaxsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffd).aggregate(Max('dsp'))
    ddavgsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffd).aggregate(Avg('dsp'))
    dumaxsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffd).aggregate(Max('usp'))
    duavgsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffd).aggregate(Avg('usp'))
    hdmaxsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffh).aggregate(Max('dsp'))
    hdavgsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffh).aggregate(Avg('dsp'))
    humaxsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffh).aggregate(Max('usp'))
    huavgsp = Measurement.objects.filter(tester=request.user,testdata__gt=cutoffh).aggregate(Avg('usp'))
    dmaxsp = Measurement.objects.filter(tester=request.user).aggregate(Max('dsp'))
    davgsp = Measurement.objects.filter(tester=request.user).aggregate(Avg('dsp'))
    umaxsp = Measurement.objects.filter(tester=request.user).aggregate(Max('usp'))
    uavgsp = Measurement.objects.filter(tester=request.user).aggregate(Avg('usp'))
    print(ddmaxsp.get('dsp__max'))

    context ={
        'm':m,
        'statsperday':d,
        'statsper12h':h,
        'ddm':ddmaxsp.get('dsp__max'),'dum':dumaxsp.get('usp__max'),'dda':ddavgsp.get('dsp__avg'), 'dua':duavgsp.get('usp__avg'),
        'hdm':hdmaxsp.get('dsp__max'),'hum':humaxsp.get('usp__max'),'hda':hdavgsp.get('dsp__avg'), 'hua':huavgsp.get('usp__avg'),
        'dm':dmaxsp.get('dsp__max'),'um':umaxsp.get('usp__max'),'da':davgsp.get('dsp__avg'),'ua':uavgsp.get('usp__avg')
    }
    return render(request,"profile/profile.html",context)

from django.shortcuts import get_object_or_404
def records(request):
    latest_records_list= Measurement.objects.filter(tester=request.user).order_by('-testdata')

    context = {"records_list":latest_records_list}
    return render(request, 'profile/records.html',context)
