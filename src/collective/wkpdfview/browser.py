import os
import re
from subprocess import check_call, PIPE
from tempfile import mktemp
from urlparse import urlparse


class WKPdfView(object):
    def __init__(self, context, request):
        self.context, self.request = context, request
    def __call__(self):
        "Invoke wkhtmltopdf on the url without the final @@wkpdf"
        command = "wkhtmltopdf"
        if 'WKHTMLTOPDF_PATH' in os.environ:
            command = os.environ['WKHTMLTOPDF_PATH']
        host, port = self.request.HTTP_HOST.split(':')
        if 'WKHTMLTOPDF_BASE' in os.environ:
            host, port = os.environ['WKHTMLTOPDF_BASE'].split(':')
        path = self.request.PATH_TRANSLATED.replace('/@@wkpdf', '')
        path = re.sub('/(@@)?wkpdf(\?|$)', r'\2', path)
        url = 'http://%s:%s%s' % (host, port, path)
        filepath = mktemp('.pdf')
        cookiepath = build_cookiejar(self.request)

        try:
            check_call((command, '--print-media-type',
                        '--cookie-jar', cookiepath,
                        url, filepath),
                        stdout=PIPE, stderr=PIPE)
            self.request.response.setHeader("Content-type", "application/pdf")
            with open(filepath) as fh:
                filecontents = fh.read()
            return filecontents
        finally:
            if os.path.isfile(filepath):
                os.unlink(filepath)
            if os.path.isfile(cookiepath):
                os.unlink(cookiepath)


def build_cookiejar(request):
    u = urlparse(request.URL)
    filename = mktemp('.jar')
    with open(filename, 'w') as fh:
        for k, v in request.cookies.items():
            fh.write("%s=%s; domain=%s; path=/;\n" % (k, v, u.hostname))
    return filename
