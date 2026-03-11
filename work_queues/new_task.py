import pika, sys 



message = ' '.join(sys.argv[1:]) or "Hello World!"

#url to our rabbitmq server 
url = "amqps://lhjnrpbb:7C2zXomPcuy_wy9p8KOCXmIgMt3C8yeT@leopard.lmq.cloudamqp.com/lhjnrpbb"
#extract required parameters from url
params = pika.URLParameters(url) 
#establishing a tcp connection based on params 
connection = pika.BlockingConnection(params) 
#basic channel connection to send and receive msgs
channel  = connection.channel() 
#declare a queue to want to connect to (if the queue doesn't exist, it will be created)
channel.queue_declare(queue='task_queue', durable=True) #this queue should exist
channel.basic_qos(prefetch_count=1) #this tells rabbitmq not to give more than 1 message to a worker at time (if worker busy dispatch to next worker in line (without this the job will wait in buffer))
#golang has taught me to handle errors so here we go 
try:
    # for i in range(5):
    #     message = f"{message} {i}"
    #     channel.basic_publish(exchange='', routing_key='hello', body=message)
    #     print(f"Sent '{message}' to the queue.")
        channel.basic_publish(exchange='', routing_key='task_queue', body=message, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)) #make message persistent (if rabbitmq crashes the message will still be there when it comes back up)
 
except Exception as e:
    print("Error sending message: ", e)
print(f"Sent '{message}' to the queue.")


connection.close()

