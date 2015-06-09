
import json
from datetime import date, datetime
from django.shortcuts import redirect,render, render_to_response, RequestContext, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    errors = []
    if request.method == "POST":
        post = json.loads(request.body.decode('utf-8'))
        username = post['username']
        password = post['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(status=200, content_type='application/json', content='{"login":true, "errors":[]}')
            else:
                errors.append({'message': "Your account has been disabled"})
                resp = {"login":False, "errors":errors}
                return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
        else:
            errors.append({'message': "The username and password you have entered do not match our records"})
            resp = {"login":False, "errors":errors}
            return HttpResponse(status=200, content_type='application/json', content=json.dumps(resp))
    return render_to_response("index.html", {'errors': errors}, RequestContext(request))


@login_required(login_url='/login/')
def home(request):
    return render_to_response('index.html', {}, RequestContext(request))

