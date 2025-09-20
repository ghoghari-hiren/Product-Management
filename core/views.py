from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .permissions import is_admin
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer
from .models import Product
from .pagination import ProductPagination
from .throttles import AdminUserRateThrottle, RegularUserRateThrottle, AnonymousRateThrottle

class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonymousRateThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "User registered successfully",
                "access": access_token,
                "refresh": str(refresh),
                "role": user.role
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonymousRateThrottle]


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "User Login successfully",
                "access": access_token,
                "refresh": str(refresh),
                "role": user.role
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateView(APIView):
    pagination_class = ProductPagination
    def post(self, request):
        if not is_admin(request.user):
            return Response({"error": "Only admin users can create products"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        products = Product.objects.filter(is_active=True)

        title = request.GET.get('title')
        description = request.GET.get('description')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')

        if title:
            products = products.filter(title__icontains=title)
        if description:
            products = products.filter(description__icontains=description)
        if price_min:
            products = products.filter(price__gte=price_min)
        if price_max:
            products = products.filter(price__lte=price_max)

        sort_by = request.GET.get('sort_by', 'created_on')
        order = request.GET.get('order', 'desc')

        if sort_by not in ['created_on', 'updated_on', 'price']:
            sort_by = 'created_on'
        if order == 'desc':
            sort_by = '-' + sort_by

        
        paginator = ProductPagination()
        paginated_queryset = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class ManageProductView(APIView):

    def put(self, request, pk):
        if not is_admin(request.user):
            return Response({"error": "Only admin users can update products"}, status=status.HTTP_403_FORBIDDEN)
    
        product = get_object_or_404(Product, pk=pk, is_active=True)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not is_admin(request.user):
            return Response({"error": "Only admin users can update products"}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(Product, pk=pk, is_active=True)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not is_admin(request.user):
            return Response({"error": "Only admin users can delete products"}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        if not is_admin(request.user):
            return Response({"error": "Only admin users can disable products"}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(Product, pk=pk, is_active=True)
        product.is_active = False
        product.save()
        return Response({"message": "Product disabled successfully"}, status=status.HTTP_200_OK)
