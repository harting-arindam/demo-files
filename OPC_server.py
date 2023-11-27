from opcua import Server
import xml.etree.ElementTree as ET
import zipfile

# Function to extract AAS information from an AASX file
def extract_aas_information(aasx_file):
    aas_info = {}

    # with zipfile.ZipFile(aasx_file, 'r') as zip_ref:
    #     # Extract the AAS XML file from the AASX archive
    #     aas_xml_file = zip_ref.extract('aas/aas.xml', './temp')

        # Parse the AAS XML file
    tree = ET.parse('aas_xml.xml')
    root = tree.getroot()

        # Extract relevant information (customize based on your AAS structure)
    aas_info['name'] = root.find('.//aas:AssetAdministrationShell/aas:identification/aas:Identifier',
                                    namespaces={'aas': 'http://www.admin-shell.io/core/aas'})
    # Add more extraction logic for other AAS information

    return aas_info

# OPC UA Server setup
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

uri = "http://example.org"
idx = server.register_namespace(uri)

obj = server.nodes.objects.add_object(idx, "AASObject")

# Expose AAS information as variables
aas_info = extract_aas_information('Arindammid1.aasx')
for key, value in aas_info.items():
    var = obj.add_variable(idx, key, value)

# Start the server
server.start()

try:
    while True:
        pass  # Your server logic here

finally:
    server.stop()
    print("Server stopped")
