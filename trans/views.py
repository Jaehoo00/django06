from django.shortcuts import render
from googletrans import Translator
import googletrans

# Create your views here.

def index(request):
    context = {
        "ndict" : googletrans.LANGUAGES
    }
    if request.method == "POST":
        b = request.POST.get("bf")
        f = request.POST.get("fr")
        t = request.POST.get("to")

        trans = Translator()
        after = trans.translate(b, src=f, dest=t)

        context.update({
            "af" : after.text,
            "bf" : b,
            "fr" : f,
            "to" : t
        })

    return render(request, "trans/index.html", context)