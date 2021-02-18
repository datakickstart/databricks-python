#!/usr/bin/env python
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Copyright 2016 Confluent Inc.
# Licensed under the MIT License.
# Licensed under the Apache License, Version 2.0
#s
# Original Confluent sample modified for use with Azure Event Hubs for Apache Kafka Ecosystems

from confluent_kafka import Producer
import sys
import time
import random

from config import producer_conf, producer_conf_local, sasl_passwords

source_filepath = "/opt/data/nyc_taxi/yellow_trips/2019/yellow_tripdata_json_2019-12.json"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s <topic>\n' % sys.argv[0])
        sys.exit(1)
    topic = sys.argv[1]
    try:
        local = sys.argv[2]
    except:
        local = False

    producer_conf['sasl.password'] = sasl_passwords[topic]

    if local:
        producer_conf = producer_conf_local

    # Create Producer instance
    p = Producer(**producer_conf)


    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' % (msg.topic(), msg.partition(), msg.offset()))


    # Write 1-100 to topic
    with open(source_filepath, 'r') as f:
        for row in f:
            try:
                print(row)
                # print(json.dumps(row))
                p.produce(topic, row, callback=delivery_callback)
            except BufferError as e:
                sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(p))
            p.poll(0)
            sleep_sec = random.randrange(7) # random number of seconds between 0 and 1
            time.sleep(sleep_sec)
            

    # Wait until all messages have been delivered
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()

