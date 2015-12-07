import os
from subprocess import check_call, PIPE
from subprocess import CalledProcessError
from tempfile import mktemp
from urlparse import urlparse
import json


class WKPdfView(object):
    def __init__(self, context, request):
        self.context, self.request = context, request

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/pdf")
        return self.get_pdf_file()

    def get_pdf_file(self):
        "Invoke phantomjs on the url without the final @@wkpdf"
        command = "phantomjs"
        if 'PHANTOMJS_PATH' in os.environ:
            command = os.environ['PHANTOMJS_PATH']
        host, port = self.request.HTTP_HOST.split(':')
        if 'PHANTOMJS_BASE' in os.environ:
            host, port = os.environ['PHANTOMJS_BASE'].split(':')
        path = '/'.join(self.context.getPhysicalPath())
        url = 'http://%s:%s%s' % (host, port, path)
        filepath = mktemp('.pdf')
        scriptpath = make_scriptfile(self.request, host)
        try:
            try:
                cmd_tuple = (command, scriptpath, url, filepath)
                check_call(cmd_tuple, stdout=PIPE, stderr=PIPE)
            except CalledProcessError:
                # An error occurred
                if not os.path.isfile(filepath):
                    raise
            with open(filepath) as fh:
                filecontents = fh.read()
            return filecontents
        finally:  # clean up
            for path in (filepath, scriptpath):
                if os.path.isfile(path):
                    os.unlink(path)


def make_scriptfile(request, hostname=None):
    if not hostname:
        u = urlparse(request.URL)
        hostname = u.hostname
    path = mktemp('.js')
    addcookie_scripts = []
    cookie = dict(domain=hostname)
    for k, v in request.cookies.items():
        cookiestr = json.dumps(dict(cookie, name=k, value=v))
        addcookie_scripts.append("phantom.addCookie(%s);" % cookiestr)
    with open(path, 'w') as fh:
        fh.write(RASTERIZE_SCRIPT % '\n'.join(addcookie_scripts))
    return path


RASTERIZE_SCRIPT = """
var page = require('webpage').create(),
    address, output, size;

if (phantom.args.length < 2 || phantom.args.length > 3) {
    console.log('Usage: rasterize.js URL filename');
    phantom.exit();
} else {
    address = phantom.args[0];
    output = phantom.args[1];
    %s
    //page.paperSize = {format: "A4"};
    page.viewportSize = { width: 1500, height: 1160 };
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
                page.render(output);
                phantom.exit();
            }, 200);
        }
    });
}
"""
