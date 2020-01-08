#!/usr/bin/env python
# coding: utf-8

from mqttclient import Client

c = Client()
c.publish(period=50)