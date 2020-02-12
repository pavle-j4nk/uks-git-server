from django.views.decorators.csrf import csrf_exempt

from gitServer.git_server import handle_git_request


@csrf_exempt
def git(request, username, repository, path=''):
    return handle_git_request(request, username, repository, path)
