from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Search, Post
from .serializers import SearchSerializer, PostSerializer
from scraper import scrape
from dateutil.parser import parse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import pdb


class SearchList(APIView):
    def get(self, request):
        pdb.set_trace()
        searches = Search.objects.all()
        serializer = SearchSerializer(searches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchDetail(APIView):
    def get_object(self, id):
        try:
            return Search.objects.get(id=id)
        except Search.DoesNotExist:
            return None

    def get(self, request, id):
        search = self.get_object(id)
        if search:
            serializer = SearchSerializer(search)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Search not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        search = self.get_object(id)
        if search:
            search.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Search not found'}, status=status.HTTP_404_NOT_FOUND)


class PostsBySearch(APIView):
    def get(self, request, id):
        search = Search.objects.filter(id=id).first()
        if search:
            posts = search.posts.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Search not found'}, status=status.HTTP_404_NOT_FOUND)


class ScrapeView(APIView):
    def post(self, request):
        search = Search.objects.filter(id=request.data['search_id']).first()

        if not search:
            return Response({'error': 'Search not found'}, status=status.HTTP_404_NOT_FOUND)

        raw_posts = scrape(
            search_terms=request.data['search_terms'],
            limit=request.data.get('limit', 100),
            subreddit=request.data.get('subreddit', None),
            include_over_18=request.data.get('include_over_18', False),
            sort=request.data.get('sort', 'new'),
            time_filter=request.data.get('time_filter', 'all'),
            restrict_to_subreddit=request.data.get('restrict_to_subreddit', False),
            pages=request.data.get('pages', 1)
        )

        new_posts = []

        if raw_posts:
            for post in raw_posts:
                if not Post.objects.filter(reddit_id=post['full_name']).first():
                    new_post = Post(
                        reddit_id=post['full_name'],
                        created=parse(post['date_time']),
                        title=post['post_title'],
                        url=post['post_link'],
                        img_url=post['post_img'],
                        body=post['post_body']
                    )
                    new_posts.append(new_post)

            Post.objects.bulk_create(new_posts)
            search.posts.add(*new_posts)

            serializer = PostSerializer(new_posts, many=True)

            if not new_posts:
                return Response({'message': 'No new posts'}, status=status.HTTP_204_NO_CONTENT)

            return Response({
                'posts': serializer.data,
                'search': SearchSerializer(search).data
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Scrape returned no results'}, status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    def get(self, request):
        searches = Search.objects.all()
        search_id = request.query_params.get('search_id')
        
        if search_id:
            posts = Post.objects.filter(searches__id=search_id).order_by('-created')
        else:
            posts = Post.objects.all().order_by('-created')
        
        paginator = Paginator(posts, 25)
        page_number = request.query_params.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'home.html', {
            'searches': searches,
            'page_obj': page_obj,
            'selected_search_id': int(search_id) if search_id else None
        })


class SearchesView(APIView):
    def get(self, request):
        searches = Search.objects.all()
        return render(request, 'searches.html', {'searches': searches})
    
    def post(self, request):
        title = request.data.get('title')
        search_terms = [term.strip() for term in request.data.get('search_terms').split(',')]
        
        if title and search_terms:
            Search.objects.create(
                title=title,
                search_terms=search_terms
            )
        return redirect('searches')
    
class SearchDeleteView(APIView):
    def post(self, request, id):
        search = Search.objects.filter(id=id).first()
        if search:
            search.delete()
        return redirect('searches')