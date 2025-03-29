from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
import pandas as pd
import os

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def basic_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def basic_delete(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_only_view(request):
    return Response({"message": "Welcome, Admin!"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import os


@api_view(['GET'])
def basic_load_task1(request):
    try:
        # Define the file path
        file_path = "D:\\PythonProject\\basic_loan\\basic_home_loan\\task\\loan_csv_missing_check.csv"

        # Check if the file exists
        if not os.path.exists(file_path):
            return Response({"error": "File not found at the specified path."}, status=404)

        # Load the dataset
        data = pd.read_csv(file_path)

        # Check if the dataset is empty
        if data.empty:
            return Response({"error": "The file is empty. Please check the dataset."}, status=400)

        # **Step 1: Identify Missing Values**
        missing_values = data.isnull().sum()  # Count missing values in each column
        total_missing = missing_values.sum()  # Total number of missing values

        if total_missing > 0:
            # Include details about columns with missing values
            missing_info = missing_values[missing_values > 0].to_dict()
            return Response({
                "message": "Dataset loaded successfully, but missing values were found.",
                "missing_values": missing_info,
                "total_missing": total_missing
            }, status=200)

        # **Step 2: Return the dataset preview (if no missing values)**
        preview = data.head(10).to_dict()  # Convert to dictionary for API response
        return Response({
            "message": "Dataset loaded successfully! No missing values detected.",
            "data_preview": preview,
            "total_rows": len(data),
            "columns": list(data.columns)
        }, status=200)

    except pd.errors.ParserError:
        return Response({"error": "The file could not be parsed as a CSV. Please verify the dataset format."},
                        status=400)
    except FileNotFoundError:
        return Response({"error": "File not found at the specified path."}, status=404)
    except pd.errors.EmptyDataError:
        return Response({"error": "The file is empty. Please check the dataset."}, status=400)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)




