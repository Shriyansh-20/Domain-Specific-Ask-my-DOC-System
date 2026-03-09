from django.shortcuts import render

# Create your views here.
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from .rag_pipeline import process_pdf, ask_question


@api_view(['POST'])
def upload_pdf(request):

    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES['file']

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)

    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    process_pdf(file_path)

    return Response({
        "message": "PDF uploaded and processed successfully"
    })


@api_view(['POST'])
def ask(request):

    question = request.data.get("question")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    result = ask_question(question)

    return Response(result)