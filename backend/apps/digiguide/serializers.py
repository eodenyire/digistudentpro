from rest_framework import serializers
from .models import StudentProfile, AcademicRecord, Career, CareerPrediction

class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'

class CareerPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPrediction
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    academic_records = AcademicRecordSerializer(many=True, read_only=True)
    careers = CareerSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'

class DashboardDataSerializer(serializers.Serializer):
    student_profile = StudentProfileSerializer()
    predicted_career = CareerPredictionSerializer()

    class Meta:
        fields = ['student_profile', 'predicted_career']