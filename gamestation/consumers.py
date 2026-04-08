import json
from channels.generic.websocket import AsyncWebsocketConsumer
from principalstation.firebase_config import initialize_firebase
from firebase_admin import firestore
import asyncio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

db = initialize_firebase()

class PriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Definimos el grupo de precios (como tu chat_global)
        self.room_name = "precios_juegos"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Iniciamos el vigilante de Firestore en segundo plano
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.escuchar_cambios_firestore)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Este método envía el mensaje final al navegador (parecido a tu chat_message)
    async def precio_update_mensaje(self, event):
        await self.send(text_data=json.dumps({
            'juego_id': event['juego_id'],
            'titulo': event['titulo'],
            'precio': event['precio']
        }))

    def escuchar_cambios_firestore(self):
        """
        Función que detecta cuando un distribuidor cambia un precio en Firestore
        """
        def on_snapshot(col_snapshot, changes, read_time):
            for change in changes:
                # 'MODIFIED' detecta cuando editas el juego con tu PUT
                if change.type.name == 'MODIFIED':
                    datos = change.document.to_dict()
                    juego_id = change.document.id
                    
                    # Enviamos la notificación a todos los conectados al grupo
                    layer = get_channel_layer()
                    async_to_sync(layer.group_send)(
                        self.room_name,
                        {
                            'type': 'precio_update_mensaje',
                            'juego_id': juego_id,
                            'titulo': datos.get('titulo'),
                            'precio': datos.get('precio')
                        }
                    )

        # IMPORTANTE: Asegúrate de que 'juegos' sea el nombre de tu colección en Firestore
        db.collection('juegos').on_snapshot(on_snapshot)
