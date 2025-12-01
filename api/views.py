from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
import time


@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint.
    Returns basic status information.
    """
    return Response({
        'status': 'ok',
        'service': 'cerberus-ref',
        'timestamp': time.time()
    })


@api_view(['GET'])
def metrics_example(request):
    """
    Example endpoint demonstrating custom Cerberus metrics.

    This endpoint shows how to attach custom metrics to a response
    that will be captured by the Cerberus middleware.
    """
    # Simulate some processing
    start_time = time.time()

    result = {
        'message': 'This endpoint demonstrates custom metrics',
        'example_data': [1, 2, 3, 4, 5]
    }

    processing_time = (time.time() - start_time) * 1000

    # Create response
    response = Response(result)

    # Attach custom metrics for Cerberus
    # The middleware will extract this and include it in the metrics sent to backend
    response.data['_cerberus_metrics'] = {
        'processing_time_ms': round(processing_time, 2),
        'items_returned': len(result['example_data']),
        'cache_hit': False,
        'custom_flag': True
    }

    return response


@api_view(['GET', 'POST'])
def item_list(request):
    """
    List all items or create a new item.

    GET: Returns list of all items
    POST: Creates a new item
    """
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)

        # Add custom metrics
        response = Response(serializer.data)
        response.data = {
            'items': serializer.data,
            '_cerberus_metrics': {
                'items_count': len(serializer.data),
                'operation': 'list'
            }
        }
        return response

    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Add custom metrics for item creation
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.data = {
                **serializer.data,
                '_cerberus_metrics': {
                    'operation': 'create',
                    'item_id': serializer.data['id']
                }
            }
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    """
    Retrieve, update or delete an item.

    GET: Returns item details
    PUT: Updates an item
    DELETE: Deletes an item
    """
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(
            {'error': 'Item not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = ItemSerializer(item)

        response = Response(serializer.data)
        response.data = {
            **serializer.data,
            '_cerberus_metrics': {
                'operation': 'retrieve',
                'item_id': pk
            }
        }
        return response

    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = Response(serializer.data)
            response.data = {
                **serializer.data,
                '_cerberus_metrics': {
                    'operation': 'update',
                    'item_id': pk
                }
            }
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()

        response = Response(status=status.HTTP_204_NO_CONTENT)
        # For DELETE, we need to set the metrics differently since there's no response.data
        response._cerberus_metrics = {
            'operation': 'delete',
            'item_id': pk
        }
        return response


@api_view(['GET'])
def slow_endpoint(request):
    """
    Intentionally slow endpoint for testing performance metrics.
    """
    import random

    # Simulate slow processing
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)

    response = Response({
        'message': 'This was a slow operation',
        'delay_seconds': round(delay, 2)
    })

    response.data['_cerberus_metrics'] = {
        'processing_time_ms': round(delay * 1000, 2),
        'endpoint_type': 'slow',
        'simulated_delay': True
    }

    return response


@api_view(['GET'])
def error_example(request):
    """
    Example endpoint that returns an error for testing error tracking.
    """
    error_type = request.query_params.get('type', 'validation')

    if error_type == 'validation':
        return Response(
            {'error': 'Validation error example', 'field': 'name'},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif error_type == 'not_found':
        return Response(
            {'error': 'Resource not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    elif error_type == 'server':
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return Response(
            {'error': 'Unknown error type'},
            status=status.HTTP_400_BAD_REQUEST
        )
