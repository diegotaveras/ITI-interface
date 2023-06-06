import xmltodict
import json
xml_file=open("policy.xml","r")
xml_string=xml_file.read()
python_dict=xmltodict.parse(xml_string)
json_string=json.dumps(python_dict, indent=4)

out = open("output.json", "w")
out.write(json_string)
out.close()

print("The given .xml file given in .json format: output.json")


