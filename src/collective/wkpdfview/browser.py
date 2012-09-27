from subprocess import check_call, PIPE
from tempfile import mktemp
import os

class WKPdfView(object):
    def __init__(self, context, request):
        self.context, self.request = context, request
    def __call__(self):
        "Invoke wkhtmltopdf on the url without the final @@wkpdf"
        command = "wkhtmltopdf"
        if 'WKHTMLTOPDF_PATH' in os.environ:
            command = os.environ['WKHTMLTOPDF_PATH']
        url = self.request.URL
        if '/@@wkpdf' not in url:
            raise RuntimeError("This use case is not implemented yet")
        url = url.replace('/@@wkpdf', '')
        filepath = mktemp()
        result = check_call((command, url, filepath),
                            stdout=PIPE, stderr=PIPE)
        if result == 0:
            self.request.response.setHeader("Content-type", "application/pdf")
            with open(filepath) as fh:
                filecontents = fh.read()
            return filecontents
        else:
            raise RuntimeError("Error running wkhtmltopdf")
