from tkinter import *
import xml.etree.ElementTree as ET
import inspect

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

        v = IntVar(value= quantifier_to_options[rules[index].quantifier] if rules[index].quantifier != None else 0)
    
        

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


def UserMode():
    root = Tk()
    root.title("Policy Creator")

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


    rules = []
    ruleListbox = Listbox(policy_rules_frame,selectmode=SINGLE)
    ruleListbox.grid(row=0, column=2)
    another_frame = Frame(policy_rules_frame)
    another_frame.grid(row=0, column=0, padx=30)
    add_rule_button = Button(another_frame, text="Add rule...",command=lambda: Rule.AddItem(ruleListbox, rules))
    add_rule_button.grid(row=0, column=0)
    ruleListbox.bind("<<ListboxSelect>>", lambda event, arg=rules: Rule.OpenView(event, arg))

    
    objectLists = []
    objectListListbox = Listbox(policy_objectLists_frame,selectmode=SINGLE)
    objectListListbox.grid(row=0, column=2)
    add_objectList_button = Button(policy_objectLists_frame, text="Add object list...",command=lambda: ObjectList.AddItem(objectListListbox, objectLists, objList_entry))
    add_objectList_button.grid(row=0, column=0)
    objectListListbox.bind("<<ListboxSelect>>", lambda event, arg=objectLists: ObjectList.OpenView(event, arg))
    objList_entry = Entry(policy_objectLists_frame)
    objList_entry.grid(row=1,column=0)


    dictionaries = []
    dictionaryListbox = Listbox(policy_dictionaries_frame,selectmode=SINGLE)
    dictionaryListbox.grid(row=0, column=2)
    add_dictionary_button = Button(policy_dictionaries_frame, text="Add dictionary...",command=lambda: Dictionary.AddItem(dictionaryListbox, dictionaries, dictionary_entry))
    add_dictionary_button.grid(row=0, column=0)
    dictionaryListbox.bind("<<ListboxSelect>>", lambda event, arg=dictionaries: Dictionary.OpenView(event, arg))
    dictionary_entry = Entry(policy_dictionaries_frame)
    dictionary_entry.grid(row=1,column=0)


    description = Description("")
    description_entry = Text(policy_description_frame, width=50, height=5)
    description_entry.grid(row=1,column=0)
    add_description_button = Button(policy_description_frame, text="Add description...",command=lambda: description.UpdateDescription(description_entry.get("1.0",'end-1c')))
    add_description_button.grid(row=0, column=0)

    
    mainloop()

    CreateXMLFile(rules, objectLists, dictionaries, description)


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
   