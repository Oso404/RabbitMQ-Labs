"""
this would be the consumer code 
"""

#!/usr/bin/env python
import pika, sys, os, time, random

def main():
    #url to our rabbitmq server 
    url = "amqps://lhjnrpbb:7C2zXomPcuy_wy9p8KOCXmIgMt3C8yeT@leopard.lmq.cloudamqp.com/lhjnrpbb"
    #extract required parameters from url
    params = pika.URLParameters(url) 
    #establishing a tcp connection based on params 
    connection = pika.BlockingConnection(params) 
    channel = connection.channel()
    #this is the queue the consumer wants to consume from 
    channel.queue_declare(queue='task_queue', durable=True) #this queue should exist
    #simple callback function 
    def callback(ch, method, properties, body):
        print(f"Received {body}")
        time.sleep(random.randint(1, 4)) #simulate work
        method.delivery_tag
        ch.basic_ack(delivery_tag=method.delivery_tag) #best practice to manually send ack 
        print("Done processing")
    #establishing a connection between the consumer and the queue...should run callback() when a message is received 
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)

    print('Waiting for messages. To exit press CTRL+C')
    #start consuming messages from the queue (this will block the main thread)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)