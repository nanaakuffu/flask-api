import sys
from pika import BlockingConnection, ConnectionParameters, BasicProperties, channel
from flask import current_app
from typing import Callable


class Queues():
    """
    This is a queueing class that sends to and listen from a rabbitmq server to process background requests.

    At instantiation, it takes the name of the rabbitmq server, function to execute and the name of the queue
    to listen for.
    """

    def __init__(
        self,
        server: str = 'localhost',
        target: Callable = None,
        queue: str = 'email_queue'
    ) -> None:
        self._app = current_app._get_current_object()
        self._parameters = ConnectionParameters(server)
        self._queue = queue
        self._target_method = target
        self._connection = None
        self.channel = None

    def sendDispatch(self, email: str):
        self._connection = BlockingConnection(self._parameters)
        self.channel = self._connection.channel()
        self.channel.queue_declare(queue=self._queue,
                                   durable=True)

        self.channel.basic_publish(exchange='',
                                   routing_key=self._queue,
                                   body=email,
                                   properties=BasicProperties(
                                       delivery_mode=2)
                                   )

        print(f" [+] Email dispatched to {email}.")

        self._connection.close()

    def _onMessageCallBack(self, ch, method, properties, body):
        with self._app.app_context():
            print(f"[-] Received job: {body.decode()}")
            if callable(self._target_method):
                self._target_method(body.decode())
            else:
                raise Exception(
                    f"{self._target_method} is not callable.")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def receiveDispatch(self):
        self._connection = BlockingConnection(self._parameters)
        self.channel = self._connection.channel()

        self.channel.basic_qos(prefetch_count=1)

        with self._app.app_context():
            self.channel.basic_consume(queue=self._queue,
                                       on_message_callback=self._onMessageCallBack)

        print(' [+] Waiting for messages. To exit press CTRL+C')
        return self.channel
