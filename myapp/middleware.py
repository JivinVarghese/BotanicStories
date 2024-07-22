from datetime import datetime


# Middleware to track recent activities (cookies)
class RecentActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            recent_activities = request.COOKIES.get('recent_activities', '').split(',')
            current_activity = f"[PATH::{request.path}]:[METHOD::{request.method}]\n"
            if current_activity not in recent_activities:
                recent_activities.append(current_activity)
            if len(recent_activities) > 5:  # Limit to 5 recent activities
                recent_activities.pop(0)
            response.set_cookie('recent_activities', ','.join(recent_activities), max_age=3600*24*30)
        return response


class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_date = datetime.now().strftime('%Y-%m-%d')
            if 'page_visits' not in request.session:
                request.session['page_visits'] = {}

            if current_date not in request.session['page_visits']:
                request.session['page_visits'][current_date] = 0

            request.session['page_visits'][current_date] += 1
            request.session.modified = True

        return response

