from distutils.spawn import find_executable
from email.parser import BytesParser
from subprocess import Popen, PIPE

from django.conf import settings
from django.http import HttpResponse


def handle_git_request(request, username, repository, path):
    env = create_env(request, username, repository, path)
    response = run_cgi(request.body, env)

    return convert_response(response)


def create_env(request, repository, username, path):
    path_info = get_path_info(repository, username, path)
    path_translated = settings.GIT_REPOSITORIES_DIR + path_info
    service = "service=" + request.GET["service"] if request.GET else ""
    remote_addr = get_client_ip(request)

    env = {
        "SCRIPT_NAME": "git-http-backend",
        "GATEWAY_INTERFACE": "CGI/1.1",
        "REQUEST_METHOD": request.method,
        "REMOTE_ADDR": remote_addr,
        "GIT_PROJECT_ROOT": settings.GIT_REPOSITORIES_DIR,
        "GIT_HTTP_EXPORT_ALL": "1",
        "CONTENT_TYPE": request.content_type,
        "PATH_INFO": path_info,
        "QUERY_STRING": service,
        "PATH_TRANSLATED": path_translated,
        "REMOTE_USER": "Foo"  # TODO: authorize
    }

    return env


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_path_info(repository, username, path):
    paths = [repository, username, path]
    paths = [string for string in paths if string != ""]
    path_info = "/" + "/".join(paths)

    return path_info


def convert_response(response):
    headers, body = parse_backend_response(response)
    http_response = HttpResponse(content=body, status=get_backend_status(headers, 200))

    for k in headers.keys():
        http_response[k] = headers.get(k)

    return http_response


def parse_backend_response(response):
    headers, body = response.split(b'\r\n\r\n')
    headers = BytesParser().parsebytes(headers)

    return headers, body


def get_backend_status(headers, default):
    status = default

    if headers["Status"]:
        status = headers["Status"].split(" ")[0]

    return status


def run_cgi(request, env):
    git_path = find_executable("git")
    proc = Popen([git_path, "http-backend"], stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
    stdout, stderr = proc.communicate(input=request)
    proc.stderr.close()
    proc.stdout.close()
    return stdout
