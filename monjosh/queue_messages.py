from azure.storage.common import CloudStorageAccount
from azure.storage.queue import Queue, QueueService, QueueMessage
import config
from random_data import RandomData

class QueueMessage():

      def __init__(self):
        self.random_data = RandomData()

       def run_all_samples(self, account):
        try:
            print('Azure Storage Basic Queue samples - Starting.')
            
            # declare variables
            queuename = "queuesample" + self.random_data.get_random_name(6)
            queuename2 = "queuesample" + self.random_data.get_random_name(6)
            
            # create a new queue service that can be passed to all methods
            queue_service = account.create_queue_service()

            # Basic queue operations such as creating a queue and listing all queues in your account
            print('\n\n* Basic queue operations *\n')
            self.basic_queue_operations(queue_service, queuename, queuename2)

            # Add a message to a queue in your account
            print('\n\n* Basic message operations *\n')
            self.basic_queue_message_operations(queue_service, queuename)

        except Exception as e:
            if (config.IS_EMULATED):
                print('Error occurred in the sample. Please make sure the Storage emulator is running.', e)
            else: 
                print('Error occurred in the sample. Please make sure the account name and key are correct.', e)
        finally:
            # Delete the queues from your account
            self.delete_queue(queue_service, queuename)
            self.delete_queue(queue_service, queuename2)
            print('\nAzure Storage Basic Queue samples - Completed.\n')

    # Basic queue operations including creating and listing
    def basic_queue_operations(self, queue_service, queuename, queuename2):
        # Create a queue or leverage one if already exists
        print('Attempting create of queue: ', queuename)
        queue_service.create_queue(queuename)
        print('Successfully created queue: ', queuename)

        # Create a second queue or leverage one if already exists
        print('Attempting create of queue: ', queuename2)
        queue_service.create_queue(queuename2)
        print('Successfully created queue: ', queuename2)

        #List all queues with prefix "queuesample"
        print('Listing all queues with prefix "queuesample"')
        queues = queue_service.list_queues("queuesample")
        for queue in queues:
            print('\t', queue.name)