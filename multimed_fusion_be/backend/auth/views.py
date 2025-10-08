# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": f"Already logged in as {request.user.username}"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Not logged in"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # POST → Perform login
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class UpdateUserDetailsView(APIView):
    """
    API endpoint to update user details.
    Only authenticated users can update their own profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def put(self, request, *args, **kwargs):
        user = request.user  # current authenticated user

        data = request.data
        allowed_fields = ['first_name', 'last_name', 'email']

        # Update allowed fields only
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        user.save()

        return Response({
            "message": "User details updated successfully.",
            "user": {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        }, status=status.HTTP_200_OK)



class DeleteUserView(APIView):
    """
    API endpoint to delete a user by ID.
    Only accessible to authenticated users (you can modify as needed).
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # Optional: prevent user from deleting others
            if request.user != user and not request.user.is_staff:
                return Response(
                    {"error": "You are not authorized to delete this user."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.delete()
            return Response(
                {"message": f"User with ID {user_id} deleted successfully."},
                status=status.HTTP_200_OK
            )
        
        except User.DoesNotExist:
            return Response(
                {"error": f"User with ID {user_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
