from .models import NavigationItem
from django.http import HttpResponsePermanentRedirect


class NavigationItemRedirectMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to be mindful about how many requests we're processing,
        # pass through if possible, given enough information

        # Begin 500 error funnel:
        # attempt to filter out any incoming request that is not a 500,
        # or that doesn't produce a 500 when I attempt to get the response
        # Any valid request should get caught in the funnel and returned

        try:
            # If I can get context, check the potential response to see if it's an error
            response = self.get_response(request)
            # If we haven't thrown an exception, and it's not a 500 error,
            # return this response, this case doesn't apply to this middleware
            if response.status_code != 500:
                return response
        except Exception as ex:
            # Trap this exception and ignore it, I probably don't have context and
            # this path needs to fail gracefully
            err = ex

        # End 500 error funnel:
        # only 500 errors should pass this far, any valid request should've
        # been returned already

        # Attempt to match the URL to a Navigation Item
        try:
            # Get compound path, for NavItem look up
            url_path = request.site.root_page.url_path[:-1] + request.path
            # Get the NavItem
            nav_item = NavigationItem.objects.get(url_path=url_path)
            # If we haven't thrown a DoesNotExist exception yet then
            # this is the case we are looking for: a NavItem that needs to redirect.
            # generate a response object and return it
            response = HttpResponsePermanentRedirect(nav_item.destination)
            return response
        except Exception as ex:
            # Again, fail gracefully, so we don't break on a NavigationItem.DoesNotExist
            # or any other error, since these need to pass through the other middleware as normal
            pass

        # Somehow a request might get this far. Not sure what it is or how
        # it wasn't caught in the funnel above, but here we are.
        # Pass the request along to the other middleware as normal.
        return response if response else request
