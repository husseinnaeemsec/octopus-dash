from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()

def login_view(request):
    username_field = User.USERNAME_FIELD or 'username' 
    
    context = {
        'username':username_field
    }
    
    if request.method == "POST":
        # in case the user has not set or remove this field 
        # Getting the username value&argument from the USERNAME_FIELD attribute on the User Model class 
        username = request.POST.get(username_field,None)
        username_kwarg = {username_field:username}
        # Password
        password = request.POST.get("password")

        user = authenticate(request,**username_kwarg, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect("od-dashboard")  # update route as needed
            else:
                messages.error(request, "You are not authorized to access the admin dashboard.")
                # optional: logout just in case
                logout(request)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "od/auth/login.html",context)
