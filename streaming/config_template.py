
sasl_passwords = {
    "demo-message-1": "Endpoint=sb://<your-eventhubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=ReadWriteTmp;SharedAccessKey=<YourSharedAccessKey>;EntityPath=<event-hub-name>",

}

kafka_conf = {
    'bootstrap.servers': '<your-eventhubs-namespace>.servicebus.windows.net:9093', #replace
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '$ConnectionString',
    #'sasl.password': #Populate in code by looking up in sasl_passwords or using secrets
}

producer_conf = kafka_conf
producer_conf['client.id'] = 'python-example-producer'

consumer_conf = {
    'request.timeout.ms': 60000,
    'session.timeout.ms': 60000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}
consumer_conf.update(kafka_conf)
consumer_conf['client.id'] = 'python-example-consumer'
