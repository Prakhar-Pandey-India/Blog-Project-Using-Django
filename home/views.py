from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Blog
from django.db.models import Q

class PublicBlog(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.Get.get('search')
                blogs = blogs.filter(Q(title_icontains = search) | Q(blog_text_icontains = search))

            # serializer = BlogSerializer(blogs, many = True)

            page_number = request.GET.get('page',1)
            paginator = Paginator(blogs,1)

            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'data': {},
                'message':'something went wrong or invalid page'
            }, status= status.HTTP_400_BAD_REQUEST)





class BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    #to fetch all blog user has created
    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)
            print(blogs)
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            serializer = BlogSerializer(blogs, many = True)

            return Response({
                'data': serializer.data,
                'message': 'blogs fetched successfully'
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message':'something went wrong or invalid page'
            }, status= status.HTTP_400_BAD_REQUEST)




    def post(self, request):
        try:
            data = request.data
            # print('#####')
            # print(request.user)
            # print('######')
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'blog created successfully'
            }, status = status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)
        
    #
    def patch(self, request):
        try:
            data = request.data
            # print("Data:-->",data)
            # print(data.get('uid'))
            blog = Blog.objects.filter(uid = data.get('uid'))
            
            # print("blog:-->",blog)

            if not blog.exists():
                return Response({
                    'data':{},
                    'message': 'invalis blog uid'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            # print("blog[0]:-->",blog[0])
            # print("blog[0].user:-->",blog[0].user)
            # print("request.user",request.user)
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message': 'You are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer = BlogSerializer(blog[0], data = data, partial = True)
            print("serializer",serializer)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'blog updated successfully'
            }, status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            data = request.data

            blog = Blog.objects.filter(uid = data.get('uid'))

            #checking blog exist or not
            if not blog.exists():
                return Response({
                    'data':{},
                    'message': 'invalis blog uid'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            #checking that the person who wants to delete the blog and the person who has created the blog is same or different. If then only it will delete. 
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message': 'You are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()
            return Response({
                'data': {},
                'message': 'blog deleted successfully'
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)