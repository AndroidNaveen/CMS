from django.http import HttpResponse
from django.views.generic import View
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app3.serializers import ProductSerializer
from app3.models import ProductModel
import io
