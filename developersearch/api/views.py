from time import process_time_ns
from unicodedata import name
from urllib import response
from pkg_resources import require
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProjectSerializer
from project.models import Project, Review, Tag


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'POST': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'DELETE': '/api/projects/id'},
        {'GET': '/api/projects/id/vote'},

        {'POST': '/api/users/token/'},
        {'POST': '/api/users/token/refresh/'},
    ]

    return Response(routes)


# ============================ Project api ================================= #

@api_view(['GET', 'POST'])
def getProjects(request):
    # View projects
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    # Create a project
    elif request.method == 'POST':
        if IsAuthenticated:
            user = request.user.profile
            data = request.data               
            
            try:
                if data['project']['title'] != None:
                    project = Project(owner=user, title=data['project']['title'], desciption=data['project']['desciption'], featured_image=data['project']['featured_image'], 
                    demo_link=data['project']['demo_link'], source_link=data['project']['source_link'])

                    project.save()
                    for tag in data.get('tags'):
                        
                        tag, created = Tag.objects.get_or_create(name=tag)
                        project.tags.add(tag)


                    return Response(status=status.HTTP_201_CREATED)
            except KeyError:
                return Response({"error":"Missing requirement"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error":"Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'DELETE'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    # check existing get to update or create no exits
    review, created = Review.objects.get_or_create(
        owner = user,
        project=project,
    )
    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')