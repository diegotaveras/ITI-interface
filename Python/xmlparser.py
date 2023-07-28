import xmltodict
import json

def xmlparser(in_xml, out_json):

    xml_file=open(in_xml,"r")
    xml_string=xml_file.read()
    python_dict=xmltodict.parse(xml_string, attr_prefix='')
    json_string=json.dumps(python_dict, indent=4)

    out = open(out_json, "w")
    out.write(json_string)
    out.close()
    print("The given .xml file given in .json format: " + out_json)
    print(json_string)
    return json_string
    
    


