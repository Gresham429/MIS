from django.shortcuts import render


def devices_index(request):
    return render(request, 'devices/devices.html')