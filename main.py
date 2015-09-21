from datetime import date
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import os
from pdfrw import PdfReader, PdfWriter 
import base64

class PdfHandler(tornado.web.RequestHandler):
    def get(self,id):
        inpfn = 'teste.pdf'
        ranges = [id]
        #
        assert ranges, "Expected at least one range"
        #
        ranges = ([int(y) for y in x.split('-')] for x in ranges)
        outfn = '%sfrag' % os.path.basename(inpfn)
        pages = PdfReader(inpfn).pages
        outdata = PdfWriter()
        #
        for onerange in ranges:
            onerange = (onerange + onerange[-1:])[:2]
            for pagenum in range(onerange[0], onerange[1]+1):
                outdata.addpage(pages[pagenum-1])
        outdata.write(outfn)
        #
        pdfout = base64.encodestring(open(outfn,"rb").read())
        #
        self.write('<iframe src="data:application/pdf;base64,'+pdfout+'" style="position:fixed; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;"/>')
        # self.write(response)
 
 
def main():
    application = tornado.web.Application([
        (r"/pdf/([0-9]+)", PdfHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()