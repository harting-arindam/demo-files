from opcua import Client

url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

client = Client(url)
client.connect()

print("Server Address Space:")
for node in client.get_objects_node().get_children():
    print(node)

try:
    # Assuming the AAS information is exposed under the "AASObject" object
    aas_object = client.get_node("ns=2;i=1")

    # Read AAS information variables
    aas_name_node = aas_object.get_child(["2:name"])
    
    # Check if the node exists before reading its value
    if aas_name_node is not None:
        aas_name = aas_name_node.get_value()
        print("AAS Name:", aas_name)
    else:
        print("AAS Name node not found.")

    # Add more variables as needed
    
    # Keep the client alive for a while
    input("Press Enter to exit...\n")

finally:
    client.disconnect()
    print("Client disconnected")
