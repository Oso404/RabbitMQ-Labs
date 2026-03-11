"""
create a basic  producer that sends "hello world" message to a queue named "hello" 


this would be the producer code 

"""


import pika 

#url to our rabbitmq server 
url = "amqps://lhjnrpbb:7C2zXomPcuy_wy9p8KOCXmIgMt3C8yeT@leopard.lmq.cloudamqp.com/lhjnrpbb"
#extract required parameters from url
params = pika.URLParameters(url) 
#establishing a tcp connection based on params 
connection = pika.BlockingConnection(params) 
#basic channel connection to send and receive msgs
channel  = connection.channel() 
#declare a queue to want to connect to (if the queue doesn't exist, it will be created)
channel.queue_declare(queue='hello') #this queue should exist
#golang has taught me to handle errors so here we go 
try:
    channel.basic_publish(exchange='', routing_key='hello', body='Hello world!') 
except Exception as e:
    print("Error sending message: ", e)
print("Sent 'Hello world!' to the queue.")

connection.close()






