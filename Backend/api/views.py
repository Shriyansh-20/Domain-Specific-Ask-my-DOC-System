import os
import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .rag_pipeline import process_pdf, ask_question

session_id = str(uuid.uuid4())

@api_view(['POST'])
def upload_pdf(request):

    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    uploaded_file = request.FILES['file']

    session_dir = f"sessions/{session_id}"
    docs_dir = f"{session_dir}/docs"

    os.makedirs(docs_dir, exist_ok=True)

    file_path = os.path.join(docs_dir, uploaded_file.name)

    # save file
    with open(file_path, "wb+") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # process PDF for RAG
    process_pdf(file_path, session_id)

    return Response({
        "session_id": session_id,
        "message": "PDF uploaded and processed"
    })


@api_view(['POST'])
def ask(request):

    question = request.data.get("question")
    session_id = request.data.get("session_id")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    if not session_id:
        return Response({"error": "Session ID is required"}, status=400)

    result = ask_question(question, session_id)

    return Response(result)