from django.views.decorators.cache import never_cache
from .decoradores import login_requerido
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Practica, Post
from .forms import EditPerfilForm


def nosotros(request):
    return render(request, "miapp/nosotros.html")


def home(request):
    response = render(request, "miapp/home.html")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def generos(request):
    return render(request, "miapp/generos.html")


@login_requerido
def post(request):
    todos_posts = Post.objects.select_related('author').all().order_by('-created_at')

    context = {
        'posts': todos_posts,
        'total_posts': todos_posts.count(),
        'es_mi_perfil': False,
    }

    return render(request, "miapp/post.html", context)


@login_requerido
def newPost(request):
    if request.method == 'POST':
        usuario_id = request.session.get('user_id')

        if not usuario_id:
            return HttpResponse("No hay usuario logueado", status=401)

        usuario = Practica.objects.get(id=usuario_id)

        Post.objects.create(
            post_type=request.POST.get('postType'),
            title=request.POST.get('title'),
            genre=request.POST.get('genre'),
            tags=request.POST.get('tags'),
            content=request.POST.get('content'),
            image_url=request.POST.get('image'),
            author=usuario
        )

        return redirect('post')

    return render(request, "miapp/newPost.html")


@never_cache
@login_requerido
def perfil(request):
    usuario = Practica.objects.get(id=request.session.get("user_id"))
    mis_posts = Post.objects.filter(author=usuario).order_by('-created_at')

    context = {
        "usuario": usuario,
        "mis_posts": mis_posts,
        "es_mi_perfil": True,
    }

    return render(request, "miapp/perfil.html", context)


@never_cache
@login_requerido
def editPerfil(request):
    usuario = Practica.objects.get(id=request.session.get("user_id"))

    if request.method == "POST":
        form = EditPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = EditPerfilForm(instance=usuario)

    return render(request, "miapp/editPerfil.html", {
        "form": form,
        "usuario": usuario
    })


def header(request):
    return render(request, "miapp/header.html")


def sidebar(request):
    return render(request, "miapp/sidebar.html")


def SegunVist(request):
    return render(request, "miapp/moreinfo.html")


def TercerVist(request):
    return render(request, "miapp/pag-3.html")


@never_cache
def registro(request):
    if request.method == "GET":
        return render(request, "miapp/registro.html")

    usern = request.POST.get("username")
    passw1 = request.POST.get("password1")
    passw2 = request.POST.get("password2")
    email = request.POST.get("email", "")

    if Practica.objects.filter(username=usern).exists():
        return render(request, "miapp/registro.html", {
            "infosms": "El nombre de usuario ya existe"
        })

    if passw1 == passw2:
        Practica.objects.create(username=usern, password=passw2, email=email)
        return redirect("login")

    return render(request, "miapp/registro.html", {
        "infosms": "Las contraseñas no coinciden"
    })


@never_cache
def login(request):
    if request.method == "GET":
        return render(request, "miapp/login.html")

    user = request.POST.get("txtusuario")
    password = request.POST.get("txtpassword")

    try:
        usuario = Practica.objects.get(username=user)

        if usuario.password == password:
            request.session['user_id'] = usuario.id
            request.session['username'] = usuario.username
            return redirect("home")

        return render(request, "miapp/login.html", {
            "error": "Contraseña incorrecta"
        })

    except Practica.DoesNotExist:
        return render(request, "miapp/login.html", {
            "error": "El usuario no existe"
        })


@never_cache
def cerrarSesion(request):
    request.session.flush()
    return redirect("login")


def check_session(request):
    return JsonResponse({
        'authenticated': 'user_id' in request.session,
        'username': request.session.get('username', '')
    })


@login_requerido
def editPost(request, post_id):
    post = Post.objects.get(id=post_id)
    usuario = Practica.objects.get(id=request.session.get('user_id'))

    if post.author != usuario:
        return HttpResponse("Acceso denegado", status=403)

    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.genre = request.POST.get('genre', post.genre)
        post.tags = request.POST.get('tags', post.tags)
        post.content = request.POST.get('content', post.content)
        post.image_url = request.POST.get('image', post.image_url)
        post.save()
        return redirect('perfil')

    return render(request, "miapp/editPost.html", {"post": post})


@login_requerido
def elimPost(request, post_id):
    post = Post.objects.get(id=post_id)
    usuario = Practica.objects.get(id=request.session.get('user_id'))

    if post.author != usuario:
        return HttpResponse("Acceso denegado", status=403)

    if request.method == 'POST':
        post.delete()
        return redirect('perfil')

    return render(request, "miapp/elimPost.html", {"post": post})
