from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from departments.models import department


def ListDepartment(request):
    return render(request, 'dictionaries/dictionary_list.html')


def ListDepartmentJson(request):
    list_objects = department.objects.all().order_by('name')
    json_res = []
    for obj in list_objects:
        json_res.append(obj.to_dict)
    return JsonResponse({'success': True, 'objects': json_res})
