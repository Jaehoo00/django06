from csv import writer
from django.shortcuts import render, redirect
from .models import Board, Reply
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    pg = request.GET.get("page", 1)
    kw = request.GET.get("kw", "")
    cate = request.GET.get("cate", "")

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            b = Board.objects.none()
    else:
        b = Board.objects.all()

    pag = Paginator(b, 3)
    obj = pag.get_page(pg)

    context = {
        "bset" : obj,
        "kw" : kw,
        "cate" : cate
    }
    return render(request, "board/index.html", context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rset" : r
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else:
        pass # 8일차
    return redirect("board:index")

def create(request):
    if request.method == "POST": 
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, content=c).save()
        return redirect("board:index")
    return render(request, "board/create.html")


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    
    if request.user != b.writer:
        pass # 8
        return redirect("board:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject, b.content = s, c
        b.save()
        return redirect("board:detail", bpk)
        
    context = {
        "b" : b
    }
    return render(request, "board/update.html", context)

def creply(request, bpk):
    r = request.POST.get("rep")
    b = Board.objects.get(id=bpk)
    Reply(b=b, replyer=request.user, comment=r).save()
    return redirect("board:detail", bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.reply == request.user:
        r.delete()
    else:
        pass # 8일차
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)