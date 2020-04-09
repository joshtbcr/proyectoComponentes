from azure.storage.common import CloudStorageAccount
from azure.storage.queue import Queue, QueueService, QueueMessage
import config
import base64

class QueueWorker():

    def __init__(self):
        
        self.account_name = config.STORAGE_ACCOUNT_NAME
        self.account_key = config.STORAGE_ACCOUNT_KEY
        self.account = CloudStorageAccount(self.account_name, self.account_key)

    def queue_busqueda(self, mensaje):
        account = self.account
        queuename = "monjoshqueue"
        messagename = mensaje


        try:
            # Crear servicio de queue
            queue_service = account.create_queue_service()

            #Hay q pasarlo a base64, sino da error en leer el message en el Function App
            encodedBytes = base64.b64encode(messagename.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")

            queue_service.put_message(queuename, encodedStr)
            
            print ('Se agrego exitosamente el queue: Base64: ', encodedStr,', Cleartext: ', mensaje)
            
            return True
        except Exception as e:
            
            return str(e)

