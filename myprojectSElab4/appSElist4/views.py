import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product


@csrf_exempt
def product_list(request):
    """
    Handle GET and POST requests for the products endpoint.
    - GET: List all products.
    - POST: Create a new product.
    """
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            price = data.get('price')
            available = data.get('available')

            if name is None or price is None or available is None:
                return HttpResponseBadRequest(
                    "Missing required fields: 'name', 'price', and 'available' are mandatory."
                )

            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()

            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            }, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    else:
        return HttpResponseBadRequest("Unsupported HTTP method. Use GET or POST.")


@csrf_exempt
def product_detail(request, product_id):
    """
    Handle GET requests for a specific product by ID.
    """
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            })

        except Product.DoesNotExist:
            return HttpResponseNotFound("Product not found.")

    else:
        return HttpResponseBadRequest("Unsupported HTTP method. Use GET.")
