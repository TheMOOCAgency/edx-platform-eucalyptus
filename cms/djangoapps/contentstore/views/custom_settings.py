"""
Views related to custom settings
"""
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import django.utils
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from opaque_keys.edx.keys import CourseKey

from edxmako.shortcuts import render_to_response
from models.settings.course_metadata import CourseMetadata
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json

from xmodule.modulestore.django import modulestore
from xmodule.tabs import InvalidTabsException

from contentstore.views.course import get_course_and_check_access

log = logging.getLogger(__name__)

__all__ = ['custom_settings_handler',]


@login_required
@ensure_csrf_cookie
@require_http_methods(("GET", "POST", "PUT"))
@expect_json
def custom_settings_handler(request, course_key_string):
    """
    Course settings configuration
    GET
        html: get the page
        json: get the model
    PUT, POST
        json: update the Course's settings. The payload is a json rep of the
            metadata dicts.
    """
    course_key = CourseKey.from_string(course_key_string)
    with modulestore().bulk_operations(course_key):
        course_module = get_course_and_check_access(course_key, request.user)
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') and request.method == 'GET':

            return render_to_response('custom_settings.html', {
                'context_course': course_module,
                'is_new':course_module.is_new,
                'invitation_only': course_module.invitation_only,
                'visible_to_manager_only': course_module.visible_to_manager_only,
            })
        elif 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            if request.method == 'GET':
                return JsonResponse(CourseMetadata.fetch(course_module))
            else:
                try:
                    # validate data formats and update the course module.
                    # Note: don't update mongo yet, but wait until after any tabs are changed
                    is_valid, errors, updated_data = CourseMetadata.validate_and_update_from_json(
                        course_module,
                        request.json,
                        user=request.user,
                    )

                    if is_valid:
                        try:
                            additional_info = {
                                'is_new': request.POST.get('is_new', False),
                                'invitation_only': request.POST.get('invitation_only', False),
                                'visible_to_manager_only': request.POST.get('visible_to_manager_only', False)
                            }
                            CourseMetadata.update_from_dict(additional_info, course_module, request.user)
                        except InvalidTabsException as err:
                            log.exception(err.message)
                            response_message = [
                                {
                                    'message': _('An error occurred while trying to save your tabs'),
                                    'model': {'display_name': _('Tabs Exception')}
                                }
                            ]
                            return JsonResponseBadRequest(response_message)

                        return JsonResponse(updated_data)
                    else:
                        return JsonResponseBadRequest(errors)

                # Handle all errors that validation doesn't catch
                except (TypeError, ValueError, InvalidTabsException) as err:
                    return HttpResponseBadRequest(
                        django.utils.html.escape(err.message),
                        content_type="text/plain"
                    )
