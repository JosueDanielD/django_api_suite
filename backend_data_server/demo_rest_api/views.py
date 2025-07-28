from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        """
        Método GET para obtener todos los datos.
        """
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    

class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def _find_item_by_id(self, item_id):
        """
        Método auxiliar para encontrar un item por su ID.
        """
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None

    def put(self, request, item_id):
        """
        PUT: Reemplaza completamente los datos de un elemento.
        """
        item = self._find_item_by_id(item_id)
        
        if not item:
            return Response(
                {'error': f'Item con ID {item_id} no encontrado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Validación de campos requeridos
        if 'name' not in request.data or 'email' not in request.data:
            return Response(
                {'error': 'Los campos name y email son obligatorios.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reemplazar todos los datos excepto el ID
        item['name'] = request.data['name']
        item['email'] = request.data['email']
        item['is_active'] = request.data.get('is_active', True)

        return Response(
            {'message': 'Item actualizado completamente.', 'data': item}, 
            status=status.HTTP_200_OK
        )

    def patch(self, request, item_id):
        """
        PATCH: Actualiza parcialmente los campos del elemento.
        """
        item = self._find_item_by_id(item_id)
        
        if not item:
            return Response(
                {'error': f'Item con ID {item_id} no encontrado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar solo los campos proporcionados
        if 'name' in request.data:
            item['name'] = request.data['name']
        if 'email' in request.data:
            item['email'] = request.data['email']
        if 'is_active' in request.data:
            item['is_active'] = request.data['is_active']

        return Response(
            {'message': 'Item actualizado parcialmente.', 'data': item}, 
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        """
        DELETE: Elimina lógicamente un elemento (marcándolo como inactivo).
        """
        item = self._find_item_by_id(item_id)
        
        if not item:
            return Response(
                {'error': f'Item con ID {item_id} no encontrado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Eliminación lógica: marcar como inactivo
        item['is_active'] = False

        return Response(
            {'message': f'Item con ID {item_id} eliminado lógicamente.'}, 
            status=status.HTTP_200_OK
        )