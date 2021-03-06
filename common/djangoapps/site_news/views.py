"""
Views related to news pages
"""
from util.json_request import expect_json, JsonResponse

from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from edxmako.shortcuts import render_to_response

from site_news.models import NewsPage
from site_news.pages import create_page, save_page, delete_page
from site_news.utils import (
    get_lms_link_for_news,
    get_media_link_for_jacket,
    get_default_jacket_url
)


@login_required
@ensure_csrf_cookie
@require_http_methods(("GET"))
def news_outline(request):
    """
    The restful handler for news outline.
    Called to list at CMS.

    Author: Naresh Makwana
    """
    if not request.user.is_staff:
        raise PermissionDenied()

    # assume html
    # get all pages from the news pages list
    # present in the LIFO order
    pages_to_render = NewsPage.objects.filter(
        author=request.user
    )

    # order the pages
    pages_to_render = sorted(pages_to_render, key=lambda x: x.order_num)

    return render_to_response('edit-news.html', {
        'pages_to_render': pages_to_render,
        'lms_link': get_lms_link_for_news(),
    })

@login_required
@ensure_csrf_cookie
@require_http_methods(("DELETE", "POST"))
def news_handler(request, page_id=None):
    """
    The restful handler news.

    DELETE
        To delete any news page
    PUT or POST
        save the pages
    """
    # Must have staff access
    if not request.user.is_staff:
        raise PermissionDenied()

    # For updating any page, page ID is must
    if page_id:
        try:
            page = NewsPage.objects.get(pk=page_id)
        except NewsPage.DoesNotExist:
            return JsonResponse({
                'error': 'No such page exists.'
            })

        # Staff can access own pages
        if not page.access_check(request.user):
            raise PermissionDenied()

        if request.method == 'DELETE':
            delete_page(page)
        elif request.method == 'POST':
            metadata = request.POST.dict()
            if 'jacket' in request.FILES:
                metadata.update({'jacket': request.FILES['jacket']})
            save_page(page, metadata)

        return JsonResponse()
    else:  # no page ID
        if request.method == 'POST':
            page = create_page(request.user)
            return JsonResponse({
                'page_id': page.id
            })
        else:
            return JsonResponse({
                'error': 'Only page create allowed without page ID.'
            })

@expect_json
@login_required
@ensure_csrf_cookie
@require_http_methods(("POST"))
def news_visibility_handler(request, page_id=None):
    """
    The restful handler news visibility.

    DELETE
        To delete any news page
    PUT or POST
        save the pages
    """
    # Must have staff access
    if not request.user.is_staff:
        raise PermissionDenied()

    # For updating any page, page ID is must
    if page_id:
        try:
            page = NewsPage.objects.get(pk=page_id)
        except NewsPage.DoesNotExist:
            return JsonResponse({
                'error': 'No such page exists.'
            })

        # Staff can access own pages
        if not page.access_check(request.user):
            raise PermissionDenied()

        visible = request.json.get('visible', False)
        page.visible = visible
        page.save()

        return JsonResponse()
    else:  # no page ID
        return JsonResponse({
            'error': 'Page ID required.'
        })

@expect_json
@login_required
@ensure_csrf_cookie
@require_http_methods(("GET"))
def get_news_content(request, page_id=None):
    """
    To get the content for the specified
    page.

    Returns content and other studio specific details, if page exists and no
    errors. Else return ''
    """
    # Initialize the response dictionary
    content = ''

    # Must have staff access
    if not request.user.is_staff:
        raise PermissionDenied()

    # For updating any page, page ID is must
    if page_id:
        try:
            page = NewsPage.objects.get(pk=page_id)
        except NewsPage.DoesNotExist:
            return JsonResponse({
                'error': 'No such page exists.'
            })

    # Return JSON response
    return JsonResponse({
        'title': page.title,
        'summary': page.summary,
        'content': page.content,
        'jacket': get_media_link_for_jacket(page),
        'default_jacket': get_default_jacket_url()
    })

@login_required
@ensure_csrf_cookie
@require_http_methods(("GET"))
def news_detail(request, news_id=None):
    """
    To make the content of the page visible
    To the student.
    """
    try:
        page = NewsPage.objects.get(pk=news_id)
        if not (page.visible or request.user.is_staff):
            page = None
    except NewsPage.DoesNotExist:
        page = None

    return render_to_response('site_news/detail.html', {
        'news': page
    })

@login_required
@ensure_csrf_cookie
@require_http_methods(("GET"))
def news(request):
    """
    List the news on LMS with pagination.
    """
    # Get all news
    news_list = NewsPage.objects.all()

    # Filter if its needs to be accessed by student
    if not request.user.is_staff:
        news_list = news_list.filter(visible=True)

    # order the pages
    news_list = sorted(news_list, key=lambda x: x.order_num)

    # Show 5 news per page
    paginator = Paginator(news_list, 5)

    # Get page number from request
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    # Render news list
    return render_to_response('site_news/list.html', {
        'news_list': news
    })

@expect_json
@login_required
@ensure_csrf_cookie
@require_http_methods(("POST"))
def reorder_news_handler(request):
    """
    To arrange the news.
    Author: Naresh Makwana
    """
    # Get the pages in requested order
    requested_page_id_locators = request.json['pages']

    for order_num, page_id_locator in enumerate(requested_page_id_locators):
        try:
            page = NewsPage.objects.get(pk=page_id_locator.get('page_id', -1))
        except NewsPage.DoesNotExist:
            return JsonResponse(
                {"error": "News Page with id_locator '{0}' does not exist.".format(page_id_locator)}, status=400
            )
        # Change the order of the page
        page.order_num = order_num
        page.save()

    # Return empty response
    return JsonResponse()
