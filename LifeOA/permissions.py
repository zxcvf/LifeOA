def perm_login(request):
    return bool(request.user and request.user.is_authenticated)