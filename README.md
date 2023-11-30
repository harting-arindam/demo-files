"# demo-files" 
https://chat.openai.com/share/a64cb213-2b7f-4890-b527-e6d195872510


from opcua import Server
import time
import random
import paho.mqtt.client as mqtt

# OPC UA Server setup
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
uri = "http://example.org"
idx = server.register_namespace(uri)
objects = server.get_objects_node()
obj = objects.add_object(idx, "SensorData")
# obj = server.nodes.objects.add_object(idx, "SensorData")
variables = {"temperature": obj.add_variable(idx, "Temperature", 0.0),
             "pressure": obj.add_variable(idx, "Pressure", 0.0),
             "humidity": obj.add_variable(idx, "Humidity", 0.0)}

variables['temperature'].set_writable()
variables['pressure'].set_writable()
variables['humidity'].set_writable()
server.start()

# MQTT Broker setup
mqtt_client = mqtt.Client()
mqtt_client.connect("192.168.0.100", 1883, 60)

try:
    while True:
        # Generating random data for each variable
        for var_name, variable in variables.items():
            data_value = random.uniform(20.0, 30.0)  # Replace with actual data source
            opc_payload = variable.set_value(data_value)
            # print('Opc payload',opc_payload)


            # Publish data to MQTT broker
            mqtt_payload = f"{var_name}: {data_value}"
            # print('mqtt payload',mqtt_payload)

            mqtt_client.publish(f"opcua/{var_name}", opc_payload)
            # mqtt_client.publish(f"opcua/{var_name}", mqtt_payload)

        time.sleep(5)

finally:
    server.stop()
    server.iserver.stop()
    mqtt_client.disconnect()

