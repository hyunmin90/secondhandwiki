from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from flask import Flask, render_template, request
from hashlib import sha1
import time, os, json, base64, hmac, urllib

app = Flask(__name__)



def landing(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main') 
    else:
        return HttpResponseRedirect('/login')

def test_page(request):
    return render(request, 'test_page.html', {})

@app.route("/account/")
def account():
    return render_template('account.html')

@app.route('/sign_s3/')
def sign_s3():
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    
    object_name = request.args.get('s3_object_name')
    mime_type = request.args.get('s3_object_type')
    
    expires = int(time.time()+10)
    amz_headers = "x-amz-acl:public-read"
    
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
    
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
    signature = urllib.quote_plus(signature.strip())
    
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    
    return json.dumps({
                      'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
                      'url': url
                      })


@app.route("/submit_form/", methods=["POST"])
def submit_form():
    username = request.form["username"]
    full_name = request.form["full_name"]
    avatar_url = request.form["avatar_url"]
    update_account(username, full_name, avatar_url)
    return redirect(url_for('profile'))