from django.shortcuts import render
from codex.baseview import APIView, BaseView
from Vis.service import  DrugFlow, SellPredictor, RiskDetector
import logging
import os
import Vis.settings as settings
from django.http import HttpResponse, Http404
from django.http import StreamingHttpResponse
import mimetypes
from django.shortcuts import render


def demo(request, demoid):
    return render(request, f'demo{demoid}.html', {})


class Flow(APIView):
    def get(self):
        self.check_input("batch_number", "starter")
        return DrugFlow.flow(self.input["batch_number"], self.input["starter"])

class ProductSale(APIView):
    def get(self):
        self.check_input("batch_number", "year", "month", "province")
        batch, year, month, province = self.input["batch_number"], self.input["year"], self.input["month"], self.input["province"]
        if province:
            return SellPredictor.sell_city(batch_number=batch, year=year, month=month, province=province)
        else:
            return SellPredictor.sell_province(batch_number=batch, year=year, month=month)

class Risk(APIView):
    def get(self):
        self.check_input("query_area")
        query_area = self.input["query_area"]
        res = RiskDetector.risk_area(query_area)
        return res

class CycleRisk(APIView):
    def get(self):
        self.check_input("batch_number")
        res = RiskDetector.risk_multi(self.input["batch_number"])
        return res


class StaticFileView(BaseView):

    logger = logging.getLogger('Static')

    def get_file(self, fpath):
        if os.path.isfile(fpath):
            return open(fpath, 'rb').read()
        else:
            return None

    def file_iterator(self, file_name, chunk_size=10000):
        with open(file_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    if file_name.endswith(".zip"):
                        os.remove(file_name)



    def do_dispatch(self, *args, **kwargs):
        if not settings.DEBUG:
            self.logger.warn('Please use nginx/apache to serve static files in production!')
            raise Http404()
        print(self.request)
        rpath = self.request.path.replace('..', '.').strip('/')
        if '__' in rpath:
            raise Http404('Could not access private static file: ' + self.request.path)

        # 100M以下，暴力传输
        # 100M以上，流式传输
        file_path = os.path.join(settings.STATIC_ROOT, rpath)
        if os.path.getsize(file_path) < 1024 * 1024 * 100:
            content = self.get_file(os.path.join(settings.STATIC_ROOT, rpath))
            if content:
                response = HttpResponse(content, content_type=mimetypes.guess_type(rpath)[0])
                # 消除下载后的pdf报告
                if "REPORTS" not in file_path and file_path.endswith("zip"):
                    os.remove(file_path)

                return response
        else:
            file_name = os.path.basename(file_path)
            # 文件改成流式下载
            if os.path.exists(file_path):
                content = self.file_iterator(file_path)
                response = StreamingHttpResponse(streaming_content=content)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
                return response

        raise Http404('Could not found static file: ' + self.request.path)
