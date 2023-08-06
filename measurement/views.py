from django.core.serializers import json
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Measurement, Sensor
from .serializers import MeasurementSerializer


class SensorAPIView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = MeasurementSerializer

    def get(self, request):
        '''получение датчиков'''
        return Response({'Sensors': list(self.queryset.values())})

    def post(self, request):
        '''создание датчика'''
        post_new = Sensor.objects.create(
            name=request.data['name'],
            description=request.data['description'],
        )
        return Response({'post': model_to_dict(post_new)})

    def patch(self, request, pk):
        '''обновление датчика'''
        patch_update = Sensor.objects.get(id__exact=pk)
        print(model_to_dict(patch_update))
        if 'name' in request.data: patch_update.name = request.data['name']
        if 'description' in request.data: patch_update.description = request.data['description']
        patch_update.save()
        return Response({'patch': model_to_dict(patch_update)})

class MeasurementAPIView(RetrieveAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):
        '''добавление измерения'''
        post_new = Measurement.objects.create(
            sensor=Sensor.objects.get(id__exact=request.data['sensor']),
            temperature=request.data['temperature'],
        )
        return Response({'Measurement': model_to_dict(post_new)})

    def get(self, request, pk):
        '''получение информации по датчику'''
        sensor_found = Sensor.objects.get(id__exact=pk)
        measures = Measurement.objects.filter(sensor=sensor_found)
        response = model_to_dict(sensor_found)
        response['measurements'] = [model_to_dict(measure) for measure in measures]
        print(response)
        return Response(response)
