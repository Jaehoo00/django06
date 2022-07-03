from multiprocessing import context
from re import A
from django.shortcuts import render
from gtts import gTTS

# Create your views here.

def index(request):
    context = {}
    if request.method == "POST":
        c = request.POST.get("con")
        t = request.POST.get("tit")
        l = request.POST.get("lag")
 
        tts = gTTS(text=c, lang=l)
        tts.save(f"media/tts/{t}.mp3")

        context ={
            "con" : c,
            "tit" : t,
            "lag" : l
        }

    return render(request, "tts/index.html", context)