import pika, time, random



#simulate a job that takes 5 seconds to process 
"""
ch is the channel object that the consumer is using 
method contains information about the message like delivery tag, exchange, routing key, etc
properties contains any additional properties that were sent with the message (like headers, content type, etc)
body is the actual message body that was sent by the producer (in this case, it will be 'User Information')
"""
def pdf_process_function(ch, method, properties, body):
    print("PDF processing")
    print("Received " + str(body))
    time.sleep(random.randint(1, 10))  # simulate a job 1 to 10 secs.
    print("PDF processing finished")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # manually acknowledge



url = "amqps://lhjnrpbb:7C2zXomPcuy_wy9p8KOCXmIgMt3C8yeT@leopard.lmq.cloudamqp.com/lhjnrpbb"
params = pika.URLParameters(url) # extracts parameters (host, port username, etc) from URL and returns an object that can be used to connect to RabbitMQ server
connection = pika.BlockingConnection(params) # creates a connnection to RabbitMQ server using the parameters from URL in params variable
# establishes a channel for us to send and receive messages 
channel = connection.channel() 
#declares a queue for consumer to consume from (if the queue doesn't exist, it will be created)
channel.queue_declare(queue='pdfprocess')
#sends a message to the exchange (default exchange in this case) along with routing key and message body 
channel.basic_publish(exchange='', routing_key='pdfprocess', body='User Information')
channel.basic_publish(exchange='', routing_key='pdfprocess', body='User Information 1')
channel.basic_publish(exchange='', routing_key='pdfprocess', body='User Information 2')
channel.basic_publish(exchange='', routing_key='pdfprocess', body='User Information 3')

print("Sent user information to the queue.")
# establishes a connection between the consumer and the queue 
channel.basic_consume(
    queue='pdfprocess',           # which queue to consume from
    on_message_callback=pdf_process_function, # function to run when a message arrives
    auto_ack=False                # whether RabbitMQ auto-acknowledges the message
)

try:
    channel.start_consuming()  # consumer starts consuming messages from the queue
except KeyboardInterrupt:
    print("\nStopping consumer...")
    channel.close() #close channel
    connection.close()  #close connection




