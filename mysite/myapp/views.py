from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer
from google.cloud import storage
from django.conf import settings

@api_view(['GET', 'POST'])
def image_list(request):
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def image_detail(request, pk):
    try:
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ImageSerializer(image)
        return Response(serializer.data)

@api_view(['GET'])
def get_file_by_name(request, filename):
    try:
        storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(f'images/{filename}')
        
        if not blob.exists():
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        file_url = blob.public_url
        return Response({'url': file_url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def list_bucket_files(request):
    try:
        storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
        bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
        blobs = bucket.list_blobs()
        
        file_urls = [blob.public_url for blob in blobs]
        
        return Response(file_urls, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)