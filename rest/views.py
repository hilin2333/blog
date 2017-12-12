# -*- coding: utf-8 -*-
import os
import datetime

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class UploadList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser,)
    MAX_SIZE = 1024 * 1024 * 8
    def post(self, request, format=None):
        if request.FILES.get('files').size > self.MAX_SIZE:
            return Response(self.getResult() , status=200)
        baseDir = os.path.dirname(os.path.abspath(__name__))
        uploaddir = os.path.join(baseDir, 'static', 'upload')
        upload = request.FILES.get('files')
        newDir = datetime.datetime.now().strftime('%Y/%m/%d/');
        path = os.path.join(uploaddir,newDir)
        if not os.path.exists(path):
            os.makedirs(path)
        filename = os.path.join(path, upload.name.replace(' ',''))
        url = None
        fobj = None
        try:
            fobj = open(filename, 'wb')
            for chrunk in upload.chunks():
                fobj.write(chrunk)
            msg = '上传成功'
            url = 'http://'+ request.get_host() + (filename.replace(baseDir ,'').replace("\\",'/'))
        except IOError as err:
            msg = '上传失败'
        finally:
            fobj.close()
        return Response(self.getResult(msg,url) , status=200)


    def getResult(self, msg='上传图片过大，请文字描述', url=None):
        return {
            'msg':msg,
            'files':[{'url': url}]
        }

