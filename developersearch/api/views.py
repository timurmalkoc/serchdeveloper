from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProjectSerializer, UserSerializer
from project.models import Project, Review, Tag
from django.contrib.auth.models import User

@api_view(['GET'])
def getRoutes(request):
    routes = [
        
        {'GET': '/api/projects'},
        {'POST': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'PUT': '/api/projects/id'},
        {'DELETE': '/api/projects/id'},
        {'GET': '/api/projects/id/vote'},

        {'POST': '/api/users/'},
        {'POST': '/api/users/token/'},
        {'POST': '/api/users/token/refresh/'},
    ]

    return Response(routes)

# ============================ User api ==================================== #
@api_view(['POST'])
def createUser(request):
    data = request.data
    if data.get('username') == None or data.get('password') == None:
        return Response({'error':'Missig field'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username = data['username'].lower()).first():
        return Response({'error':'User exist or taken'}, status=status.HTTP_400_BAD_REQUEST)
    user = UserSerializer.create({'email':data['email'], 'username':data['username'], 'password':data['password']})
    user.username = user.username.lower()
    user.save()
    return Response(status.HTTP_201_CREATED)



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
        else:
            return Response({"error":"You are not authoried"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error":"Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def getProject(request, pk):
    # View projects
    if request.method == 'GET':
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

    # Update a project
    elif request.method == 'PUT':
        if IsAuthenticated:
            user = request.user.profile
            data = request.data               
            project = user.project_set.filter(id=pk).first()
            if project == None:
                return Response({"error":"You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)    

            project.update(data.get('project'))

            project.save()
            for tag in data.get('tags'):
                
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)


    # Delete a project
    elif request.method == 'DELETE':
        if IsAuthenticated:
            user = request.user.profile
            project = user.project_set.filter(id=pk).first()
            if project == None:
                return Response({"error":"You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
            project.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"error":"Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

