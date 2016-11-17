import json

from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.http import JsonResponse

from openedx.core.djangoapps.user_api.accounts.image_helpers import get_profile_image_urls_for_user


@ensure_csrf_cookie
@login_required
@require_http_methods(("GET"))
def get_forum_profile_pic(request):
    """
    Description: This view allows to get the profile images
    for the required users.

    Request Parameters:
        users: List of the username.

    Returns:
        json response with username as key and
        profile image url as value.

    Author: Naresh Makwana
    """
    # For default response
    username_profile_mapping = {}

    # Get the list of the username
    username_list = json.loads(
        request.GET.get("users", "[]")
    )

    # Iterate and get the profile pic URL for each users
    for username in username_list:
        student = User.objects.get(username=username)
        username_profile_mapping.update({
            username: get_profile_image_urls_for_user(student)['medium']
        })

    # return json response
    return JsonResponse(username_profile_mapping)
