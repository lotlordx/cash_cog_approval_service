import json
import requests
from kafka import KafkaProducer


class KafkaProducerBase:
    """
    Kafka Producer Base Class
    """

    def __init__(self, kafka_brokers, stream_url, topic):
        self.broker = kafka_brokers
        self.url = stream_url
        self.topic = topic

    def connect_kafka_producer(self):
        """
        This function connects to the kafka broker
        :return:
        """

        _producer = None
        try:
            _producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                      bootstrap_servers=self.broker, api_version=(0, 10))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return _producer

    def stream_service(self):
        """
        This generator function streams requests from a
        streaming service
        :return: yields a json object
        """

        try:
            resp = requests.get(self.url, stream=True)
            for line in resp.iter_lines():
                if line:
                    yield json.loads(line.decode())
        except Exception as ex:
            print("Event Service is not available kindly confirm uri -- {}".format(self.url))
            print(ex)

    def publish(self):
        """
        This function publishes streamed feeds to the appropriate kafka topic
        :return:
        """

        _producer = self.connect_kafka_producer()
        resource = self.stream_service()

        for data in resource:
            print("pushing data {} to kafka topic --> {}".format(data, self.topic))
            _producer.send(self.topic, data)
            _producer.flush()
