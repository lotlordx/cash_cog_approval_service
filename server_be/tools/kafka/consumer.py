import json
from kafka import KafkaConsumer


class KafkaConsumerBase:
    """
    Kafka Consumer base Class
    """

    def __init__(self, kafka_brokers, topic):
        """
        :param kafka_brokers [list]: represents the broker url's
        :param topic: represents the topic name eg (approval topic)
        """
        self.consumer = KafkaConsumer(topic, auto_offset_reset='earliest',
                                      auto_commit_interval_ms=1000, group_id='lotlord',
                                      bootstrap_servers=kafka_brokers, api_version=(0, 10), consumer_timeout_ms=1000)

        self.topic = topic

    def subscribe(self):
        """
        This function , subcribes to notifications from a
        given topic, sets an offset by means of a group_id
         to prevent re-retrival of already subscribed messages.
        :return:
        """
        results = []
        for data in self.consumer:
            try:
                msg = json.loads(data.value.decode())
                results.append(msg)
            except:
                continue
        self.consumer.close()

        return results
