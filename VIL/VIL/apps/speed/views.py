import speedtest
from django.http import HttpResponse


servers = [8633]# 38783]
def sptest(request):
    return HttpResponse("success")

def dtest(request):
    st = speedtest.Speedtest()
    st.get_servers(servers)
    down = st.download(threads=None)
    st.upload(threads=None)
    st.results.share()

    results_dict = st.results.dict()

    return HttpResponse(down)
#from django.shortcuts import render

# Create your views here.
