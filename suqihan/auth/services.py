from django.contrib.admin.options import get_content_type_for_model
from django.utils.encoding import force_text
from django.contrib.auth import authenticate

def log_addition(request, instance, message):
    """
    Log that an instance has been successfully added.

    The default implementation creates an admin LogEntry object.
    """
    from django.contrib.admin.models import LogEntry, ADDITION
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(instance).pk,
        object_id=instance.pk,
        object_repr=force_text(instance),
        action_flag=ADDITION,
        change_message=message,
    )

def resetPassword(request):
    user = request.user;
    old_password = request.data['old_password']
    password = request.data['password']
    password2 = request.data['password2']
    result = 1;#password not same
    if (password == password2):
        user = authenticate(username=user.username, password=old_password)
        if user is not None:
            result = 0#ok
            user.set_password(password)
            user.save()
        else:
            result = 2#old_password is in correct
    return result;
    
    
    
    