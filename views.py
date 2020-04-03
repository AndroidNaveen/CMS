from django.http import HttpResponse
from django.views.generic import View
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app3.serializers import ProductSerializer
from app3.models import ProductModel
import io

class ProductOperations(View):
    def get(self,request):
        qs = ProductModel.objects.all()
        ps = ProductSerializer(qs,many=True)
        json_data = JSONRenderer().render(ps.data)
        return HttpResponse(json_data,content_type="application/json")
    
    def post(self,request):
        byte_data = request.body # Will get data in bytes
        stm = io.BytesIO(byte_data) # converting bytes into streamed data
        dict_data = JSONParser().parse(stm) # Converting streamed data into dictionary
        ps = ProductSerializer(data=dict_data)
        if ps.is_valid():
            ps.save()
            message = {"message":"Product is Saved"}
        else:
            message = {"errors":ps.errors}

        json_data = JSONRenderer().render(message)
        return HttpResponse(json_data,content_type="application/json")

    
    class ReadOneProduct(View):
    def get(self,request):
        b_data = request.body
        strm = io.BytesIO(b_data)
        d1 = JSONParser().parse(strm)
        product_no = d1.get("product_no",None)
        if product_no:
            try:
                res = ProductModel.objects.get(no=product_no)
                ps = ProductSerializer(res)
                json_data = JSONRenderer().render(ps.data)
            except ProductModel.DoesNotExist:
                message = {"error": "Invalid Product No"}
                json_data = JSONRenderer().render(message)
            return HttpResponse(json_data,content_type="application/json")
        else:
            message = {"error": "Please Provide Product No"}
            json_data = JSONRenderer().render(message)
            return HttpResponse(json_data, content_type="application/json")
