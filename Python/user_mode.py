from tkinter import *

import xml.etree.ElementTree as ET
import inspect
import json
from xmlparser import xmlparser


class Description:
    def __init__(self, desc):
        self.description = desc

    def UpdateDescription(self, desc):
        self.description = desc

class Rule:
    def __init__(self, id):
        self.id = id
        self.quantifier = ""
        self.evaluate = ""
        self.description = ""
    def setFields(self, quant, eval, desc):
        self.quantifier = quant
        self.evaluate = eval
        self.description = desc.description
        print(inspect.getmembers(self))

    @staticmethod
    def AddItem(ruleList, rules):
        ruleList.insert(END, "Policy Rule " + str(ruleList.size() + 1))
        rules.append(Rule(ruleList.size()))
        print(rules)

    @staticmethod
    def OpenView(event,rules):
        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)
        print(data)
        top = Toplevel()
        top.title(data)
        frame = Frame(top)
        frame.pack()
        policy_id_frame = Label(frame, text="Policy " + str(rules[index].id))
        policy_id_frame.grid(row=0,column=0)

        policy_quantifier_frame = LabelFrame(frame, text="Quantifier")
        policy_quantifier_frame.grid(row=0,column=1)

        quantifier_options = {1:'for_all', 2: 'not_forall', 3:'exists', 4:'not_exists'}
        quantifier_to_options = { value:str(key) for key, value in quantifier_options.items()}

        v = IntVar(value= quantifier_to_options[rules[index].quantifier] if rules[index].quantifier != "" else 0)
    
        

        for_all = Radiobutton(policy_quantifier_frame, variable=v, value=1,text='for_all').pack(anchor=W)
        not_forall = Radiobutton(policy_quantifier_frame, variable=v, value=2,text='not_forall').pack(anchor=W)
        exists = Radiobutton(policy_quantifier_frame, variable=v, value=3,text='exists').pack(anchor=W)
        not_exists = Radiobutton(policy_quantifier_frame, variable=v, value=4,text='not_exists').pack(anchor=W)
        


        policy_evaluate_frame = LabelFrame(frame, text="Evaluate")
        policy_evaluate_frame.grid(row=0,column=2)

        evaluate = Entry(policy_evaluate_frame)
        evaluate.pack()
        evaluate.insert(INSERT, rules[index].evaluate)


        policy_description_frame = LabelFrame(frame, text="Description")
        policy_description_frame.grid(row=1,column=2)

        description = Entry(policy_description_frame)
        description.pack()
        description.insert(INSERT, rules[index].description)

        Button(frame, text= "Build rule", command= lambda: rules[index].setFields(quantifier_options[v.get()], evaluate.get(), Description(description.get()))).place(relx= 0.15, rely= .9, anchor= CENTER)


        top.mainloop()

class ObjectList:
    def __init__(self, name):
        self.name = name
        self.imported = True
        self.compute = ""

    def setFields(self, imported, compute):
        self.imported = imported
        self.compute = compute
        print(inspect.getmembers(self))

    @staticmethod
    def AddItem(objectListListbox, objectLists, entry):
        name = entry.get()
        if entry.get() == "":
            return
        objectListListbox.insert(END, "Object List: " + name)
        
        objectLists.append(ObjectList(name))
        entry.delete(0,END)
        print(objectLists)

    @staticmethod
    def OpenView(event,objectLists):
        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)
        print(data)


        top = Toplevel()
        top.title(data)
        frame = Frame(top)
        frame.pack()
        objList_name_frame = Label(frame, text="Object List: " + str(objectLists[index].name))
        objList_name_frame.grid(row=0,column=0)

        objList_imported_frame = LabelFrame(frame, text="Imported")
        objList_imported_frame.grid(row=0,column=1)

        v = BooleanVar(value=objectLists[index].imported)

        imported = Checkbutton(objList_imported_frame, variable=v, text='Imported')
        imported.pack(anchor=W)

        objList_compute_frame = LabelFrame(frame, text="Compute")
        objList_compute_frame.grid(row=0,column=2)

        compute = Entry(objList_compute_frame)
        compute.pack()
        compute.insert(INSERT, objectLists[index].compute)


        Button(frame, text= "Build Object List", command= lambda: objectLists[index].setFields(v.get(), compute.get())).place(relx= 0.15, rely= .9, anchor= CENTER)


        top.mainloop()

class Dictionary:

    def __init__(self, name):
        self.name = name
        self.imported = True
        self.compute = ""

    def setFields(self, imported, compute):
        self.imported = imported
        self.compute = compute
        print(inspect.getmembers(self))

    @staticmethod
    def AddItem(dictionaryListbox, dictionaries, entry):
        name = entry.get()
        if entry.get() == "":
            return
        dictionaryListbox.insert(END, "Dictionary: " + name)
        
        dictionaries.append(Dictionary(name))
        entry.delete(0,END)
        print(dictionaries)

    @staticmethod
    def OpenView(event,dictionaries):
        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)
        print(data)


        top = Toplevel()
        top.title(data)
        frame = Frame(top)
        frame.pack()
        dictionary_name_frame = Label(frame, text="Dictionary: " + str(dictionaries[index].name))
        dictionary_name_frame.grid(row=0,column=0)

        dictionary_imported_frame = LabelFrame(frame, text="Imported")
        dictionary_imported_frame.grid(row=0,column=1)

        v = BooleanVar(value=dictionaries[index].imported)

        imported = Checkbutton(dictionary_imported_frame, variable=v, text='Imported')
        imported.pack(anchor=W)
      


        dictionary_compute_frame = LabelFrame(frame, text="Compute")
        dictionary_compute_frame.grid(row=0,column=2)

        compute = Entry(dictionary_compute_frame)
        compute.pack()
        compute.insert(INSERT, dictionaries[index].compute)


        Button(frame, text= "Build Dictionary", command= lambda: dictionaries[index].setFields(v.get(), compute.get())).place(relx= 0.15, rely= .9, anchor= CENTER)


        top.mainloop()

def PolicyCreator(my_policies):
    root = Tk()
    root.title("Policy Creator")

    rules = []
    objectLists = []
    dictionaries = []
    description = Description("")

    frame = Frame(root)
    frame.pack()
    
    policy_rules_frame = LabelFrame(frame, text="Policy Rules")
    policy_rules_frame.grid(row=0,column=0)

    policy_objectLists_frame = LabelFrame(frame, text="Policy Object Lists")
    policy_objectLists_frame.grid(row=1,column=0)

    policy_dictionaries_frame = LabelFrame(frame, text="Policy Dictionaries")
    policy_dictionaries_frame.grid(row=2,column=0)

    policy_description_frame = LabelFrame(frame, text="Policy Description")
    policy_description_frame.grid(row=4,column=0)


    
    ruleListbox = Listbox(policy_rules_frame,selectmode=SINGLE)
    ruleListbox.grid(row=0, column=2)
    another_frame = Frame(policy_rules_frame)
    another_frame.grid(row=0, column=0, padx=30)
    add_rule_button = Button(another_frame, text="Add rule...",command=lambda: Rule.AddItem(ruleListbox, rules))
    add_rule_button.grid(row=0, column=0)
    ruleListbox.bind("<<ListboxSelect>>", lambda event, arg=rules: Rule.OpenView(event, arg))

    
    
    objectListListbox = Listbox(policy_objectLists_frame,selectmode=SINGLE)
    objectListListbox.grid(row=0, column=2)
    add_objectList_button = Button(policy_objectLists_frame, text="Add object list...",command=lambda: ObjectList.AddItem(objectListListbox, objectLists, objList_entry))
    add_objectList_button.grid(row=0, column=0)
    objectListListbox.bind("<<ListboxSelect>>", lambda event, arg=objectLists: ObjectList.OpenView(event, arg))
    objList_entry = Entry(policy_objectLists_frame)
    objList_entry.grid(row=1,column=0)


    dictionaryListbox = Listbox(policy_dictionaries_frame,selectmode=SINGLE)
    dictionaryListbox.grid(row=0, column=2)
    add_dictionary_button = Button(policy_dictionaries_frame, text="Add dictionary...",command=lambda: Dictionary.AddItem(dictionaryListbox, dictionaries, dictionary_entry))
    add_dictionary_button.grid(row=0, column=0)
    dictionaryListbox.bind("<<ListboxSelect>>", lambda event, arg=dictionaries: Dictionary.OpenView(event, arg))
    dictionary_entry = Entry(policy_dictionaries_frame)
    dictionary_entry.grid(row=1,column=0)


    description_entry = Text(policy_description_frame, width=50, height=5)
    description_entry.grid(row=1,column=0)
    add_description_button = Button(policy_description_frame, text="Add description...",command=lambda: description.UpdateDescription(description_entry.get("1.0",'end-1c')))
    add_description_button.grid(row=0, column=0)

    
    my_policy = Policy()
    my_policy.Populate(rules, objectLists, dictionaries, description)
    my_policies.append(my_policy)
    mainloop()
    


class Policy:
    def __init__(self):
        self.name = ""
        self.rules = []
        self.objectLists = []
        self.dictionaries = []
        self.description = Description("")
    def Populate(self, rules, objectLists, dictionaries, description):
        self.rules = rules
        self.objectLists = objectLists
        self.dictionaries = dictionaries
        self.description = description
    def PopulateFromJson(self,policy):
        self.name = policy["Name"]
        policyJson = policy["PolicyRuleSet"]
        for each in policyJson:
            if each == "PolicyRule":
                print(policyJson[each])
                if type(policyJson[each]) is dict:
                    rule = Rule(policyJson[each]['@name'])
                    rule.setFields(policyJson[each]['@quantifier'], policyJson[each]['@evaluate'], Description(policyJson[each]['Description']) if "Description" in policyJson[each] else Description(""))
                    self.rules.append(rule)
                else:
                    for i in range(len(policyJson[each])):
                        rule = Rule(policyJson[each][i]['@name'])
                        rule.setFields(policyJson[each][i]['@quantifier'], policyJson[each][i]['@evaluate'], Description(policyJson[each][i]['Description']) if "Description" in policyJson[each][i] else Description(""))
                        self.rules.append(rule)

            elif each == "ObjectList":
                print(type(policyJson[each]))
                if type(policyJson[each]) is dict:
                    objectList = ObjectList(policyJson[each]['@name'])
                    objectList.setFields(policyJson[each]['@imported'], policyJson[each]['@compute'])
                    self.objectLists.append(objectList)
                else:
                    for i in range(len(policyJson[each])):
                        objectList = ObjectList(policyJson[each][i]['@name'])
                        objectList.setFields(policyJson[each][i]['@imported'], policyJson[each][i]['@compute'])
                        self.objectLists.append(objectList)
                
            elif each == "Dictionary":
                if type(policyJson[each]) is dict:
                    dictionary = Dictionary(policyJson[each]['@name'])
                    dictionary.setFields(policyJson[each]['@imported'], policyJson[each]['@compute'])
                    self.dictionaries.append(dictionary)
                else:
                    for i in range(len(policyJson[each])):
                        dictionary = Dictionary(policyJson[each][i]['@name'])
                        dictionary.setFields(policyJson[each][i]['@imported'], policyJson[each][i]['@compute'])
                        self.dictionaries.append(dictionary)
                
            elif each == "Description":
                self.description.UpdateDescription(policyJson[each])


def ActivePolicyFrame(event, message):
    event.widget.configure(background='#A1CEE5')
    event.widget.bind("<Leave>", lambda  event :event.widget.configure(background='#FAFAFA'))


def FillRuleListbox(listbox, rules):
    for i in range(len(rules)):
        listbox.insert(END, "Policy Rule: " + rules[i].id)


def FillObjectListListbox(listbox, objectLists):
    for i in range(len(objectLists)):
        listbox.insert(END, objectLists[i].name)

def FillDictionariesListbox(listbox, dictionaries):
    for i in range(len(dictionaries)):
        listbox.insert(END, dictionaries[i].name)



def OpenPolicyView(event, policies, index, my_policies):
    policyJson = policies[index]
    print(policyJson)

    top = Toplevel()
    top.title(policies[index]['Name'])
    frame = Frame(top)
    frame.pack()

    policy = Policy()
    policy.PopulateFromJson(policyJson)
    policy_rules_frame = LabelFrame(frame, text= "Rules")
    policy_rules_frame.grid(row=0,column=0)

    policy_objectLists_frame = LabelFrame(frame, text= "Object Lists")
    policy_objectLists_frame.grid(row=0,column=1)

    policy_dictionaries_frame = LabelFrame(frame, text= "Dictionaries")
    policy_dictionaries_frame.grid(row=1,column=0)

    policy_description_frame = LabelFrame(frame, text= "Description")
    policy_description_frame.grid(row=1,column=1)

    rulesListbox = Listbox(policy_rules_frame,selectmode=SINGLE)
    FillRuleListbox(rulesListbox, policy.rules)
    rulesListbox.grid(row=0, column=0)
    rulesListbox.bind("<<ListboxSelect>>", lambda event, arg=policy.rules: Rule.OpenView(event, arg))

    objectListsListbox = Listbox(policy_objectLists_frame,selectmode=SINGLE)
    FillObjectListListbox(objectListsListbox, policy.objectLists)
    objectListsListbox.grid(row=0, column=0)
    objectListsListbox.bind("<<ListboxSelect>>", lambda event, arg=policy.objectLists: ObjectList.OpenView(event, arg))

    dictionariesListbox= Listbox(policy_dictionaries_frame,selectmode=SINGLE)
    FillDictionariesListbox(dictionariesListbox, policy.dictionaries)
    dictionariesListbox.grid(row=0, column=0)
    dictionariesListbox.bind("<<ListboxSelect>>", lambda event, arg=policy.dictionaries: Dictionary.OpenView(event, arg))


    description_view = Text(policy_description_frame)
    description_view.insert(END, policy.description.description)
    description_view.grid(row=0, column=0)
    

    Button(frame, text= "Add Policy", command= lambda: my_policies.append(policy)).grid(row=2, columnspan=2)

    top.mainloop()


def RenderLibrary(my_policies):
    library = json.load(open('library.json'))
    policies = library["Policies"]

    root = Tk()
    root.title("Policy Creator Library")
    frame = Frame(root)
    
    policies_frame = LabelFrame(frame, text="Policies",padx=40)
    policies_frame.pack()
    
    # policies.pop(0)       test whether this works
    if (not policies):
        no_policy_msg = Message(policies_frame,text="No policies available.")
        no_policy_msg.pack()

    for i in range(len(policies)):


        policy_frame = Frame(policies_frame,width=2)
        print(policies[i]["Name"])
        policy_name = Message(policy_frame,text=policies[i]["Name"])
        policy_name.configure(background='#FAFAFA',width=40)
        policy_name.bind("<Button-1>", lambda event, arg1=policies, arg2=i, arg3=my_policies: OpenPolicyView(event, arg1, arg2, arg3))
        policy_name.bind("<Enter>", lambda  event, arg=policy_name : ActivePolicyFrame(event, arg))

        policy_name.pack()
        policy_frame.grid(row=i,column=0)
        
    frame.pack()

    mainloop()

def PolicyAdderView():
    root = Tk()
    root.title("Publish Policy")
    frame = Frame(root)
    # frame.grid(row=0,column=0,padx=40)
    frame.place(in_=root, anchor="c", relx=.5, rely=.5)

    root.geometry("650x300")
    policy_message_frame = Message(frame,text="Do you want to publish your policy to the library?", width=400)
    policy_message_frame.grid(row=0,columnspan=2)

    my_policy_name = Entry(frame)
    my_policy_name.grid(row=1,columnspan=2,pady=10)
    button_no = Button(frame, text= "No", command= lambda: quit(),background='#FA6B84').grid(row=2, column=0,ipadx=40, padx=40)
    button_yes = Button(frame, text= "Yes", command= lambda: AddPolicyIfValid(my_policy_name.get()),background='#90EF90').grid(row=2, column=1,ipadx=40)

    # AddPolicyToLibrary('output.xml', En)
    mainloop()

def AddPolicyIfValid(name):
    top = Toplevel()
    frame = Frame(top)
    frame.place(in_=top, anchor="c", relx=.5, rely=.5)
    top.geometry("650x300")
    if name == "":
        top.title("Name Not Valid")
        policy_message_frame = Message(frame,text="Name cannot be blank. Please enter a name in the field provided.", width=400)
        button_ok = Button(frame, text= "Ok", command= lambda: top.destroy(),background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)

    else:
        AddPolicyToLibrary('output.xml', name)
        top.title("Succesfully Published " + name)
        policy_message_frame = Message(frame,text="Your policy \"" + name + "\" has been successfully added to the library!", width=400)
        button_ok = Button(frame, text= "Ok", command= lambda: quit(), background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)

    policy_message_frame.grid(row=0,columnspan=2)

    top.mainloop()

def UserMode():
    
    my_policies = [] 
    RenderLibrary(my_policies)
    print(my_policies)
    PolicyCreator(my_policies)
    
    my_rules = []
    my_objectLists = []
    my_dictionaries = []
    print(len(my_policies))
    for i in range(len(my_policies)):
        
        my_rules.extend(my_policies[i].rules)
        my_objectLists.extend(my_policies[i].objectLists)
        my_dictionaries.extend(my_policies[i].dictionaries)
        print(len(my_policies))
    for each in my_policies:
        print(type(each))
    my_description = my_policies[len(my_policies) - 1].description


    CreateXMLFile(my_rules, my_objectLists, my_dictionaries, my_description)
    PolicyAdderView()
    

def AddPolicyToLibrary(policy_xml, name):
    json_str = xmlparser(policy_xml, 'output.json')
    library = json.load(open('library.json','r'))

    policy_to_add = {"Name" : name}
    policy_to_add.update({"PolicyRuleSet": json.loads(json_str)["PolicyRuleSet"]})

    library["Policies"].append(policy_to_add)
    json_string = json.dumps(library, indent=4)
    
    out = open('library.json', "w", encoding='utf-8')
    out.write(json_string)
    out.close()
    return 


def CreateXMLFile(rules, objectLists, dictionaries, description):

    policyRuleSet = ET.Element("PolicyRuleSet")
    policyRuleSet.set("dtdVersion","0.1")

       #get Standards to follow 

    #get Rules for policy
    for i in range(len(rules)):
        policyRule = ET.SubElement(policyRuleSet, "PolicyRule")
        policyRule.set("name", str(rules[i].id))
        policyRule.set("quantifier", str(rules[i].quantifier))
        policyRule.set("evaluate", str(rules[i].evaluate))
        if (rules[i].description != ""):
            rule_description = ET.SubElement(policyRule, "Description")
            rule_description.text = rules[i].description

        print(policyRuleSet.attrib)

    for i in range(len(objectLists)):
        objectList = ET.SubElement(policyRuleSet, "ObjectList")
        objectList.set("name", str(objectLists[i].name))
        objectList.set("imported", str(objectLists[i].imported))
        objectList.set("compute", str(objectLists[i].compute))

    for i in range(len(dictionaries)):
        dictionary = ET.SubElement(policyRuleSet, "Dictionary")
        dictionary.set("name", str(dictionaries[i].name))
        dictionary.set("imported", str(dictionaries[i].imported))
        dictionary.set("compute", str(dictionaries[i].compute))

    if (description.description != ""):
        desc = ET.SubElement(policyRuleSet, "Description")
        desc.text = description.description

    tree = ET.ElementTree(policyRuleSet)

    with open("output.xml", 'wb') as file: 
        ET.indent(tree) 
        tree.write(file,xml_declaration=True,encoding='utf-8')
   