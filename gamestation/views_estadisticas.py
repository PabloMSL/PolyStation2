from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .authentication import FirebaseAuthentication
from .permissions import IsVendedor, IsAdministrador
from principalstation.firebase_config import initialize_firebase

db = initialize_firebase()

# estadísticas para distribuidor
class EstadisticasDistribuidorAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsVendedor]

    def get(self, request):
        """
        es unresumen de la actividad del distribuidor:
        - total de juegos publicados
        - juegos gratis
        - juegos de pago
        - total de compras de sus juegos
        - total de ingresos generados
        """
        uid = request.user.uid

        try:
            # 1. Obtener juegos del distribuidor
            docs_juegos = db.collection('juegos').where('distribuidor_id', '==', uid).stream()

            total_juegos = 0
            juegos_gratis = 0
            juegos_pago = 0
            ids_juegos = []

            for doc in docs_juegos:
                total_juegos += 1
                data = doc.to_dict()
                ids_juegos.append(doc.id)

                precio = float(data.get('precio', 0))

                if precio <= 0:
                    juegos_gratis += 1
                else:
                    juegos_pago += 1

            # 2. Buscar compras relacionadas con esos juegos
            total_compras = 0
            ingresos_totales = 0

            if ids_juegos:
                docs_compras = db.collection('compras').stream()

                for compra_doc in docs_compras:
                    compra = compra_doc.to_dict()
                    juego_id = compra.get('juego_id')

                    if juego_id in ids_juegos:
                        total_compras += 1
                        ingresos_totales += float(compra.get('precio', 0))

            # 3. Calcular promedio de ventas por juego
            if total_juegos > 0:
                promedio_ventas = round(total_compras / total_juegos, 2)
            else:
                promedio_ventas = 0

            return Response({
                "total_juegos_publicados": total_juegos,
                "juegos_gratis": juegos_gratis,
                "juegos_de_pago": juegos_pago,
                "total_compras_recibidas": total_compras,
                "ingresos_totales": ingresos_totales,
                "promedio_ventas_por_juego": promedio_ventas
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Estadísticas para comprador
class EstadisticasCompradorAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = []

    def get(self, request):
        """
        Será un resumen del comprador:
        - total de compras
        - total gastado
        - cantidad de reseñas hechas
        - juegos únicos en biblioteca
        """
        uid = request.user.uid

        try:
            # 1. Obtener compras del usuario
            docs_compras = db.collection('compras').where('usuario_id', '==', uid).stream()

            total_compras = 0
            total_gastado = 0
            juegos_unicos = set()

            for doc in docs_compras:
                total_compras += 1
                compra = doc.to_dict()

                total_gastado += float(compra.get('precio', 0))
                juego_id = compra.get('juego_id')

                if juego_id:
                    juegos_unicos.add(juego_id)

            # 2. Obtener reseñas del usuario
            docs_resenas = db.collection('resenas').where('usuario_id', '==', uid).stream()

            total_resenas = 0
            for _ in docs_resenas:
                total_resenas += 1

            # 3. Calcular porcentaje de juegos reseñados
            if len(juegos_unicos) > 0:
                porcentaje_resenado = int((total_resenas / len(juegos_unicos)) * 100)
                if porcentaje_resenado > 100:
                    porcentaje_resenado = 100
            else:
                porcentaje_resenado = 0

            return Response({
                "total_compras": total_compras,
                "total_gastado": total_gastado,
                "juegos_en_biblioteca": len(juegos_unicos),
                "total_resenas": total_resenas,
                "porcentaje_juegos_resenados": f"{porcentaje_resenado}%"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

