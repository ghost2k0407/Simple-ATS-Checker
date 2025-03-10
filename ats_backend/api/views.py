from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ResumeSerializer
import docx
from PyPDF2 import PdfReader

class ResumeUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Extract text from uploaded file
            file = request.FILES['file']
            text = self.extract_text(file)
            
            # Perform keyword matching
            keywords = ["Python", "Django", "React", "Data Science", "Machine Learning", "Gen AI", "SQL"]
            matched_keywords = [kw for kw in keywords if kw in text]

            return Response({
                "message": "Resume uploaded successfully!",
                "matched_keywords": matched_keywords
            }, status=201)
        return Response(serializer.errors, status=400)

    def extract_text(self, file):
        if file.name.endswith('.docx'):
            doc = docx.Document(file)
            return ' '.join([para.text for para in doc.paragraphs])
        elif file.name.endswith('.pdf'):
            reader = PdfReader(file)
            return ' '.join([page.extract_text() for page in reader.pages])
        return ""