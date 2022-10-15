from django.shortcuts import render
from django.http import HttpResponse
from .models import Project

def projects(request):
    projects = Project.objects.all()
    return HttpResponse('Here are products')


def project(request, pk):
    project = Project.objects.get(id=pk)


def createProject(request):
    pass

def updateProject(request):
    pass


def deleteProject(request):
    pass
