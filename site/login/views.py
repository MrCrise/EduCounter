from django.shortcuts import render, redirect


USERS = [
    {"username": "хозяин", "password": "123"},
    {"username": "новиков", "password": "123"},
]


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        for user in USERS:
            if user["username"] == username and user["password"] == password:
                request.session["username"] = username
                return redirect("auditoriums:auditoriums_list")

        error_message = "Неверный логин или пароль"
        return render(request,
                      "login/login.html",
                      {"error_message": error_message})

    return render(request, "login/login.html")


def logout(request):
    if "username" in request.session:
        del request.session["username"]
    return redirect("login:login")
