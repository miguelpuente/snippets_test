from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments import highlight
from .models import Snippet, Language
from .forms import SnippetForm
from .tasks import sendEmailInSnippetCreation

class SnippetAdd(LoginRequiredMixin, View):
    template_name = "snippets/snippet_add.html"
    login_url = '/login/'

    def get(self, request):
        form = SnippetForm()
        return render(request, self.template_name, {"form": form, "action": "Add"})

    def post(self, request):
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            sendEmailInSnippetCreation.delay(snippet.name, snippet.description, request.user.email)
            return redirect("snippet", id=snippet.id)
        return render(request, self.template_name, {"form": form, "action": "Add"})

class SnippetEdit(LoginRequiredMixin, View):
    login_url = "login"  # Redirección si no está autenticado

    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs['id'])
        if snippet.user != request.user:
            return HttpResponseForbidden("No tienes permiso para editar este snippet.")
        form = SnippetForm(instance=snippet)
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit"})

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs['id'])
        if snippet.user != request.user:
            return HttpResponseForbidden("No tienes permiso para editar este snippet.")
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect("snippet", id=snippet.id)
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit"})

class SnippetDelete(LoginRequiredMixin,View):
    login_url = "login"  # Redirección si no está autenticado

    def get(self, request, *args, **kwargs):
        return redirect("index")  # Evita el error 405 redirigiendo a la página principal

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs["id"])
        if snippet.user != request.user:
            return HttpResponseForbidden("No tienes permiso para eliminar este snippet.")
        snippet.delete()
        return redirect("index")


class SnippetDetails(View):
    template_name = "snippets/snippet.html"

    def get(self, request, id, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=id)

        # Verificar acceso si el snippet es privado
        if not snippet.public and snippet.user != request.user:
            return HttpResponseForbidden("No tienes permiso para ver este snippet.")

        # Formatear código con Pygments
        lexer = get_lexer_by_name(snippet.language.name, stripall=True)
        formatter = HtmlFormatter(full=True, linenos=True, cssclass="source")
        formatted_snippet = highlight(snippet.snippet, lexer, formatter)

        return render(
            request, self.template_name,
            {"snippet": snippet, "formatted_snippet": formatted_snippet}
        )


class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        user = get_object_or_404(User, username=username)

        if request.user == user:
            snippets = Snippet.objects.filter(user=user).defer('snippet', 'public').order_by("-created")
        else:
            snippets = Snippet.objects.filter(user=user, public=True).defer('snippet', 'public').order_by("-created")

        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        language = get_object_or_404(Language, slug=language)

        snippets = Snippet.objects.filter(language=language, public=True).defer('snippet', 'public')

        return render(request, "index.html", {"snippets": snippets})


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "login.html", {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        return render(request, "login.html", {'form': form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class Index(View):
    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(public=True).defer('snippet', 'public').order_by("-created")
        return render(request, "index.html", {"snippets": snippets})
