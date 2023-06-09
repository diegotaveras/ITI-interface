from tkinter import *

import xml.etree.ElementTree as ET
import inspect
import json
from xmlparser import xmlparser
import subprocess
import os

class Description:
    def __init__(self, desc):
        self.description = desc

    def UpdateDescription(self, desc):
        self.description = desc

class Rule:
    def __init__(self, id):
        self.id = id
        self.quantifier = "for_all"
        self.evaluate = ""
        self.description = ""
    def setFields(self, quant, eval, desc):
        self.quantifier = quant
        self.evaluate = eval
        self.description = desc.description

    @staticmethod
    #only allows adding a rule if at least an object list or dictionary exists
    def AddItem(ruleList, rules, itemsExist):
        if itemsExist:
            ruleList.insert(END, "Policy Rule " + str(ruleList.size() + 1))
            rules.append(Rule(ruleList.size()))

    @staticmethod
    def OpenView(event,rules,objectLists, dictionaries):
        
        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)

        top = Toplevel()
        top.title(data)

        top.geometry("400x500")
        frame = Frame(top)
        frame.pack()
        policy_id_frame = Label(frame, text="Rule " + str(rules[index].id))
        policy_id_frame.grid(row=0,column=0)

        policy_quantifier_frame = LabelFrame(frame, text="Quantifier")
        policy_quantifier_frame.grid(row=0,column=1)

        quantifier_options = {1:'for_all', 2: 'not_forall', 3:'exists', 4:'not_exists'}
        quantifier_to_options = { value:str(key) for key, value in quantifier_options.items()}

        v = IntVar(value= quantifier_to_options[rules[index].quantifier] if rules[index].quantifier != "" else 1)
    
        def Change(event):
            rules[index].quantifier = quantifier_options[v.get()]

        for_all = Radiobutton(policy_quantifier_frame, variable=v, value=1,text="for_all",command=lambda:Change(event)).pack(anchor=W)
        not_forall = Radiobutton(policy_quantifier_frame, variable=v, value=2,text="not_forall",command=lambda:Change(event)).pack(anchor=W)
        exists = Radiobutton(policy_quantifier_frame, variable=v, value=3,text="exists",command=lambda:Change(event)).pack(anchor=W)
        not_exists = Radiobutton(policy_quantifier_frame, variable=v, value=4,text="not_exists",command=lambda:Change(event)).pack(anchor=W)
    
        policy_evaluate_frame = LabelFrame(frame, text="Evaluate")
        policy_evaluate_frame.grid(row=1,column=2)

        evaluate =  Listbox(policy_evaluate_frame)
        evaluate.pack()

        policy_description_frame = LabelFrame(frame, text="Description")
        policy_description_frame.grid(row=2,column=2)

        description = Entry(policy_description_frame)
        description.pack()

        library = json.load(open('library.json'))
        evaluateFunctions = library["EvaluateFunctions"]

        for i in range(len(evaluateFunctions)):                
            evaluate.insert(END, evaluateFunctions[i]["Name"] + "()")

        
        currEvaluate = Label(frame, text= "Current evaluate: " + rules[index].evaluate)
        currEvaluate.grid(row=0, column=2, columnspan=3)
        evaluate.bind("<Double-Button-1>" , lambda event: EvaluateFunctionView(event, currEvaluate, rules[index], objectLists, dictionaries))
        
        description.insert(INSERT, rules[index].description)

        def BuildRule():
            rules[index].setFields(quantifier_options[v.get()], rules[index].evaluate, Description(description.get()))
            top.destroy()

        Button(frame, text= "Build rule", background='#86C5D8', command= lambda: BuildRule()).grid(row=3,columnspan=3,pady=10)

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

    @staticmethod
    def OpenView(event,objectLists, dictionaries):
        selection = event.widget.curselection()
        index = selection[0]
        data = event.widget.get(index)

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
        objList_compute_frame.grid(row=1,column=2)

        library = json.load(open('library.json'))
        computeFunctions = library["ComputeFunctions"]
        
        compute = Listbox(objList_compute_frame)
        compute.pack()

        for i in range(len(computeFunctions)):                
            compute.insert(END, computeFunctions[i]["Name"] + "()")


        currCompute = Label(frame, text= "Current compute: " + objectLists[index].compute)
        currCompute.grid(row=0, column=2, columnspan=3)
        compute.bind("<Double-Button-1>" , lambda event: ComputeFunctionView(event, currCompute, objectLists[index], objectLists, dictionaries))
        # compute = Entry(objList_compute_frame)
        # compute.pack()
        # compute.insert(INSERT, objectLists[index].compute)

        def BuildObjList():
            objectLists[index].setFields(v.get(), objectLists[index].compute)
            top.destroy()
        
        Button(frame, text= "Build Object List", background='#86C5D8', command= lambda: BuildObjList()).grid(row=2,columnspan=3,pady=10)
        
        top.mainloop()

class Dictionary:
    def __init__(self, name):
        self.name = name
        self.imported = True
        self.compute = ""

    def setFields(self, imported, compute):
        self.imported = imported
        self.compute = compute

    @staticmethod
    def AddItem(dictionaryListbox, dictionaries, entry):
        name = entry.get()
        if entry.get() == "":
            return
        dictionaryListbox.insert(END, "Dictionary: " + name)
        
        dictionaries.append(Dictionary(name))
        entry.delete(0,END)

    @staticmethod
    def OpenView(event,dictionaries, objectLists):
        selection = event.widget.curselection()
        index = selection[0]
        data = event.widget.get(index)
        
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
        dictionary_compute_frame.grid(row=1,column=2)

        library = json.load(open('library.json'))
        computeFunctions = library["ComputeFunctions"]
        
        compute = Listbox(dictionary_compute_frame)
        compute.pack()

        for i in range(len(computeFunctions)):                
            compute.insert(END, computeFunctions[i]["Name"] + "()")


        currCompute = Label(frame, text= "Current compute: " + dictionaries[index].compute)
        currCompute.grid(row=0, column=2, columnspan=3)
        compute.bind("<Double-Button-1>" , lambda event: ComputeFunctionView(event, currCompute, dictionaries[index], objectLists, dictionaries))

        def BuildDict():
            dictionaries[index].setFields(v.get(), dictionaries[index].compute)
            top.destroy()

        Button(frame, text= "Build Dictionary", background='#86C5D8', command= lambda: BuildDict()).grid(row=2,columnspan=3,pady=10)

        top.mainloop()

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

    # This function creates a policy object from a given JSON policy structure. 
    # This is used to create and manage the policy objects that are read from the library.
    def PopulateFromJson(self,policy):
        self.name = policy["Name"]
        policyJson = policy["PolicyRuleSet"]
        for each in policyJson:
            if each == "PolicyRule":
                if type(policyJson[each]) is dict:
                    rule = Rule(policyJson[each]['name'])
                    rule.setFields(policyJson[each]['quantifier'], policyJson[each]['evaluate'], Description(policyJson[each]['Description']) if "Description" in policyJson[each] else Description(""))
                    self.rules.append(rule)
                else:
                    for i in range(len(policyJson[each])):
                        rule = Rule(policyJson[each][i]['name'])
                        rule.setFields(policyJson[each][i]['quantifier'], policyJson[each][i]['evaluate'], Description(policyJson[each][i]['Description']) if "Description" in policyJson[each][i] else Description(""))
                        self.rules.append(rule)

            elif each == "ObjectList":
                if type(policyJson[each]) is dict:
                    objectList = ObjectList(policyJson[each]['name'])
                    objectList.setFields(policyJson[each]['imported'], policyJson[each]['compute'])
                    self.objectLists.append(objectList)
                else:
                    for i in range(len(policyJson[each])):
                        objectList = ObjectList(policyJson[each][i]['name'])
                        objectList.setFields(policyJson[each][i]['imported'], policyJson[each][i]['compute'])
                        self.objectLists.append(objectList)
                
            elif each == "Dictionary":
                if type(policyJson[each]) is dict:
                    dictionary = Dictionary(policyJson[each]['name'])
                    dictionary.setFields(policyJson[each]['imported'], policyJson[each]['compute'])
                    self.dictionaries.append(dictionary)
                else:
                    for i in range(len(policyJson[each])):
                        dictionary = Dictionary(policyJson[each][i]['name'])
                        dictionary.setFields(policyJson[each][i]['imported'], policyJson[each][i]['compute'])
                        self.dictionaries.append(dictionary)
                
            elif each == "Description":
                self.description.UpdateDescription(policyJson[each])

def PolicyCreator(my_policies):
    root = Tk()
    root.title("Policy Creator")
    root.geometry("600x900")

    rules = []
    objectLists = []
    dictionaries = []
    description = Description("")

    frame = Frame(root)
    frame.pack()
    
    policy_rules_frame = LabelFrame(frame, text="Policy Rules")
    policy_rules_frame.grid(row=2,column=0)

    policy_objectLists_frame = LabelFrame(frame, text="Policy Object Lists")
    policy_objectLists_frame.grid(row=0,column=0)

    policy_dictionaries_frame = LabelFrame(frame, text="Policy Dictionaries")
    policy_dictionaries_frame.grid(row=1,column=0)

    policy_description_frame = LabelFrame(frame, text="Policy Description")
    policy_description_frame.grid(row=3,column=0)

    ruleListbox = Listbox(policy_rules_frame,selectmode=SINGLE)
    ruleListbox.grid(row=0, column=2)
    another_frame = Frame(policy_rules_frame)
    another_frame.grid(row=0, column=0, padx=30)
    add_rule_button = Button(another_frame, text="Add rule...",command=lambda: Rule.AddItem(ruleListbox, rules, dictionaries or objectLists))
    add_rule_button.grid(row=0, column=0)
    ruleListbox.bind("<<ListboxSelect>>", lambda event, arg=rules, arg2=objectLists, arg3=dictionaries: Rule.OpenView(event, arg, arg2, arg3))

    objectListListbox = Listbox(policy_objectLists_frame,selectmode=SINGLE)
    objectListListbox.grid(row=0, column=2)
    add_objectList_button = Button(policy_objectLists_frame, text="Add object list...",command=lambda: ObjectList.AddItem(objectListListbox, objectLists, objList_entry))
    add_objectList_button.grid(row=0, column=0)
    objectListListbox.bind("<<ListboxSelect>>", lambda event, arg=objectLists, arg2=dictionaries: ObjectList.OpenView(event, arg, arg2))
    objList_entry = Entry(policy_objectLists_frame)
    objList_entry.grid(row=1,column=0)

    dictionaryListbox = Listbox(policy_dictionaries_frame,selectmode=SINGLE)
    dictionaryListbox.grid(row=0, column=2)
    add_dictionary_button = Button(policy_dictionaries_frame, text="Add dictionary...",command=lambda: Dictionary.AddItem(dictionaryListbox, dictionaries, dictionary_entry))
    add_dictionary_button.grid(row=0, column=0)
    dictionaryListbox.bind("<<ListboxSelect>>", lambda event, arg=dictionaries, arg2=objectLists: Dictionary.OpenView(event, arg, arg2))
    dictionary_entry = Entry(policy_dictionaries_frame)
    dictionary_entry.grid(row=1,column=0)

    description_entry = Text(policy_description_frame, width=50, height=5)
    description_entry.grid(row=0,column=1)

    another_frame2 = Frame(policy_description_frame)
    another_frame2.grid(row=0, column=0, padx=30)
    add_description_button = Button(another_frame2, text="Add description...",command=lambda: description.UpdateDescription(description_entry.get("1.0",'end-1c')))
    add_description_button.grid(row=0, column=0)    

    done_button_frame = Frame(frame)
    done_button_frame.grid(row=4,column=0,pady=30)
    button_done = Button(done_button_frame, text="Done", background='#86C5D8', command= lambda: root.destroy(),padx=20).pack()

    my_policy = Policy()
    my_policy.Populate(rules, objectLists, dictionaries, description)
    my_policies.append(my_policy)

    mainloop()

def ComputeFunctionView(event, currCompute, objList, objectLists, dictionaries):
    index = event.widget.curselection()[0]
    data = event.widget.get(index)

    root = Toplevel()
    root.title(data)
    # root.geometry("500x900")
    frame = Frame(root)
    frame.pack()                
  
    eval_args = LabelFrame(frame,text="Function arguments")
    eval_args.grid(row=0,column=1,padx=20)  

    args_listbox = Listbox(eval_args, selectmode=MULTIPLE, activestyle='none')    
    args_listbox.grid(row=0,column=1) 

    for i in range(len(objectLists)):
        args_listbox.insert(END, objectLists[i].name)
    for i in range(len(dictionaries)):
        args_listbox.insert(END, dictionaries[i].name)

    arguments = []

    def AddArg(event, arguments):
        idx = event.widget.curselection()[0]
        if event.widget.get(idx) not in arguments:
            event.widget.itemconfig(idx, {'bg':'#90EF90'})
            arguments.append(event.widget.get(idx))
        print(arguments)
    args_listbox.bind("<<ListboxSelect>>",  lambda event: AddArg(event, arguments))

    def UpdateComputeFunction(data):
        data = data[:-2]
        signature = data + "("
        # if rule.quantifier == "for_all":
        #     for k in range(len(arguments) - 1):
        #         signature = signature + "@" + arguments[k] + ","
        #     signature = signature + "@" + arguments[-1] + ")"
        
        for k in range(len(arguments) - 1):
            signature = signature + arguments[k] + ","
        signature = signature + arguments[-1] + ")"
        objList.compute = signature
        currCompute.config(text="Current evaluate: " + objList.compute)
        root.destroy()

    button_done = Button(frame, text="Done", background='#86C5D8', command= lambda: UpdateComputeFunction(data), padx=20)
    button_done.grid(row=1,columnspan=2,pady=20)

    root.mainloop()  

def EvaluateFunctionView(event, currEvaluate, rule, objectLists, dictionaries):
    index = event.widget.curselection()[0]
    data = event.widget.get(index)

    root = Toplevel()
    root.title(data)
    # root.geometry("500x900")
    frame = Frame(root)
    frame.pack()                
  
    eval_args = LabelFrame(frame,text="Function arguments")
    eval_args.grid(row=0,column=1,padx=20)  

    args_listbox = Listbox(eval_args, selectmode=MULTIPLE, activestyle='none')    
    args_listbox.grid(row=0,column=1) 

    for i in range(len(objectLists)):
        args_listbox.insert(END, objectLists[i].name)
    for i in range(len(dictionaries)):
        args_listbox.insert(END, dictionaries[i].name)

    arguments = []

    def AddArg(event, arguments):
        idx = event.widget.curselection()[0]
        if event.widget.get(idx) not in arguments:
            event.widget.itemconfig(idx, {'bg':'#90EF90'})
            arguments.append(event.widget.get(idx))
        print(arguments)
    args_listbox.bind("<<ListboxSelect>>",  lambda event: AddArg(event, arguments))

    def UpdateEvaluateFunction(data):
        data = data[:-2]
        signature = data + "("
        if rule.quantifier == "for_all":
            for k in range(len(arguments) - 1):
                signature = signature + "@" + arguments[k] + ","
            signature = signature + "@" + arguments[-1] + ")"
        else:
            for k in range(len(arguments) - 1):
                signature = signature + arguments[k] + ","
            signature = signature + arguments[-1] + ")"
        rule.evaluate = signature
        currEvaluate.config(text="Current evaluate: " + rule.evaluate)
        root.destroy()

    button_done = Button(frame, text="Done", background='#86C5D8', command= lambda: UpdateEvaluateFunction(data), padx=20)
    button_done.grid(row=1,columnspan=2,pady=20)

    root.mainloop()  

#This class loads and renders the library the user to pick from. 
class RenderLibrary:
    def  __init__(self):
        self.my_policies = []
        library = json.load(open('library.json'))
        self.loaded_policies = library["Policies"]
        
        root = Tk()
        root.title("Policy Creator Library")
        root.geometry("500x600")
        frame = Frame(root)
        frame.pack()

        policies_frame = LabelFrame(frame, text="Policies",padx=40)
        policies_frame.pack(side=LEFT)

        self.switch_dev = False
        
        button_frame = Frame(frame, padx=40)
        button_frame.pack(side=RIGHT,pady=40)
        button_dev = Button(root, text="Dev Mode", command= lambda: self.Switch(button_dev))
        button_dev.place(rely=.01, relx=.85)
        button_done = Button(button_frame, text="Done", background='#86C5D8', command= lambda:  self.OpenPolicyCreator(root) if self.switch_dev else root.destroy(),padx=20)
        button_done.pack(side=TOP, pady=150)

        if (not self.loaded_policies):
            no_policy_msg = Message(policies_frame,text="No policies available.")
            no_policy_msg.pack()
            mainloop()

        scrollbar = Scrollbar(policies_frame)
        scrollbar.pack( side = RIGHT, fill = Y )
        library_listbox = Listbox(policies_frame, height=30, activestyle='none',  yscrollcommand = scrollbar.set)
        library_listbox.pack()
        library_listbox.bind("<Double-Button-1>", lambda event: self.OpenPolicyView(event))
        scrollbar.config( command = library_listbox.yview )

        for i in range(len(self.loaded_policies)):
            library_listbox.insert(END, self.loaded_policies[i]["Name"])        
            
        mainloop()

    def OpenPolicyCreator(self,root):
        root.destroy()
        PolicyCreator(self.my_policies)

    def Switch(self, button_dev):
        self.switch_dev = not self.switch_dev
        if self.switch_dev == False:
            button_dev.config(background='#f0f0f0')
        else:
            button_dev.config(background='#90EF90')

    def OpenPolicyView(self, event):
        index = event.widget.curselection()[0]
        policyJson = self.loaded_policies[index]
        top = Toplevel()
        top.title(self.loaded_policies[index]['Name'])
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
        self.FillRuleListbox(rulesListbox, policy.rules)
        rulesListbox.grid(row=0, column=0)
        rulesListbox.bind("<<ListboxSelect>>", lambda event, arg=policy.rules, arg2=policy.objectLists, arg3=policy.dictionaries: Rule.OpenView(event, arg, arg2, arg3))

        objectListsListbox = Listbox(policy_objectLists_frame,selectmode=SINGLE)
        self.FillObjectListListbox(objectListsListbox, policy.objectLists)
        objectListsListbox.grid(row=0, column=0)
        objectListsListbox.bind("<<ListboxSelect>>", lambda event, arg=policy.objectLists, arg2=policy.dictionaries: ObjectList.OpenView(event, arg, arg2))

        dictionariesListbox= Listbox(policy_dictionaries_frame,selectmode=SINGLE)
        self.FillDictionariesListbox(dictionariesListbox, policy.dictionaries)
        dictionariesListbox.grid(row=0, column=0)
        dictionariesListbox.bind("<<ListboxSelect>>", lambda event, arg=policy.dictionaries, arg2=policy.objectLists: Dictionary.OpenView(event, arg, arg2))

        description_view = Text(policy_description_frame)
        description_view.insert(END, policy.description.description)
        description_view.grid(row=0, column=0)
        
        def AddPolicy():
            top.destroy()
            event.widget.itemconfig(index, {'bg':'#90EF90'})
            event.widget.selection_clear(index)
            self.my_policies.append(policy)

        def RemovePolicy(removeIndex):
            top.destroy()
            event.widget.itemconfig(index, {'bg':'white'})
            event.widget.selection_clear(index)
            self.my_policies.pop(removeIndex)

            
        if not self.FindPolicy(index):
            Button(frame, text= "Add Policy", background='#86C5D8',command= lambda: AddPolicy()).grid(row=2, columnspan=2)
        else:
            Button(frame, text= "Remove Policy", background='#FA6B84',command= lambda: RemovePolicy(self.removeIndex)).grid(row=2, columnspan=2)

        top.mainloop()  

    def FindPolicy(self,index):
            self.removeIndex 
            for i in range(len(self.my_policies)):
                if self.my_policies[i].name == self.policies[index]['Name']:
                    self.removeIndex = i
                    return True
            return False
    def FillRuleListbox(self, listbox, rules):
        for i in range(len(rules)):
            listbox.insert(END, "Policy Rule: " + rules[i].id)

    def FillObjectListListbox(self,listbox, objectLists):
        for i in range(len(objectLists)):
            listbox.insert(END, objectLists[i].name)

    def FillDictionariesListbox(self,listbox, dictionaries):
        for i in range(len(dictionaries)):
            listbox.insert(END, dictionaries[i].name)

#this class asks whether to 'publish' their assembled policy and does so if it's valid
class PolicyPublisher:  
    def __init__(self):                    
        root = Tk()
        root.title("Publish Policy")
        frame = Frame(root)
        frame.place(in_=root, anchor="c", relx=.5, rely=.5)

        root.geometry("650x300")
        policy_message_frame = Message(frame,text="Do you want to publish your policy to the library?", width=400)
        policy_message_frame.grid(row=0,columnspan=2)

        my_policy_name = Entry(frame)
        my_policy_name.grid(row=1,columnspan=2,pady=10)
        button_no = Button(frame, text= "No", command= lambda: quit(),background='#FA6B84').grid(row=2, column=0,ipadx=40, padx=40)
        button_yes = Button(frame, text= "Yes", command= lambda: self.AddPolicyIfValid(my_policy_name.get()),background='#90EF90').grid(row=2, column=1,ipadx=40)
        mainloop()

    #This function validates the given policy name. It cannot be an empty string
    #and the name cannot already be present in the library
    def AddPolicyIfValid(self,name):                          
        top = Toplevel()
        frame = Frame(top)
        frame.place(in_=top, anchor="c", relx=.5, rely=.5)
        top.geometry("650x300")
        self.name = name
        if self.name == "":
            top.title("Name Not Valid")
            policy_message_frame = Message(frame,text="Name cannot be blank. Please enter a name in the field provided.", width=400)
            button_ok = Button(frame, text= "Ok", command= lambda: top.destroy(),background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)
        elif self.PolicyNameTaken():
            top.title("Name Not Valid")
            policy_message_frame = Message(frame,text="The name your provided is already present in the library. Please provide a unique name.", width=400)
            button_ok = Button(frame, text= "Ok", command= lambda: top.destroy(),background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)
        else:
            self.WritePolicyToLibrary('output.xml')
            top.title("Succesfully Published " + name)
            policy_message_frame = Message(frame,text="Your policy \"" + name + "\" has been successfully added to the library!", width=400)
            button_ok = Button(frame, text= "Ok", command= lambda: quit(), background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)
            

        policy_message_frame.grid(row=0,columnspan=2)

        top.mainloop()

    #check if policy name to be added to the library is already present in the library
    def PolicyNameTaken(self):
        library = json.load(open('library.json','r'))
        for each in library["Policies"]:
            if each["Name"] == self.name:
                return True
        return False
    
    #this function parses the xml file of the user's newly created policy
    #it creates a json object out of this policy to then write to the library.json
    def WritePolicyToLibrary(self,policy_xml):
        json_str = xmlparser(policy_xml, 'output.json')                        
        library = json.load(open('library.json','r'))                   

        policy_to_add = {"Name" : self.name}
        policy_to_add.update({"PolicyRuleSet": json.loads(json_str)["PolicyRuleSet"]})

        library["Policies"].append(policy_to_add)
        json_string = json.dumps(library, indent=4)

        out = open('library.json', "w", encoding='utf-8')
        out.write(json_string)
        out.close()
        return 

#this class displays the user with the option to add a new compute/evaluate function. It tests the submitted code and function name.
class FunctionCreator():
    def __init__(self):

        # json_str = xmlparser(policy_xml, 'output.json')      
        root = Tk()
        root.title("Function Creator")
        root.geometry("900x600")

        frame = Frame(root)
        frame.pack()                

        func_name = LabelFrame(frame, text="Function name")
        func_name.grid(row=0,column=0,padx=20)  

        name_entry = Entry(func_name) 
        name_entry.grid(row=0,column=0)

        function_frame = LabelFrame(frame, text="Function code")
        function_frame.grid(row=1,columnspan=2)

        function_code = Text(function_frame)
        function_code.pack()

        self.switch_func = False
        def Switch(self):
            self.switch_func = not self.switch_func
            if self.switch_func == False:
                button_func_type.config(text="Evaluate")
            else:
                button_func_type.config(text="Compute")

        button_func_type = Button(frame, background='#86C5D8', text="Compute" if self.switch_func else "Evaluate",command= lambda: Switch(self))
        button_func_type.grid(row=0, column=1)
    
        button_done = Button(frame, text="Done", background='#86C5D8', command= lambda : self.WriteFunctionIfValid(root, name_entry.get(), function_code.get("1.0",'end-1c'), button_func_type.cget("text")), padx=20)
        button_done.grid(row=2,columnspan=2,pady=20)

        mainloop()

    def WriteFunctionIfValid(self,root, name, code, func_type):
        if (name.replace(" ", "").strip() == ""):
            return
        self.name = name
        self.func_code = code
        self.func_type = func_type
        if self.ValidCode():
            if not self.FunctionNameTaken():
                self.WriteFunction()
                root.destroy()
            else:
                top = Toplevel()
                frame = Frame(top)
                frame.place(in_=top, anchor="c", relx=.5, rely=.5)
                top.geometry("650x300")
                top.title("Name Not Valid")
                function_message_frame = Message(frame,text="Function \"" +  self.name + "\" already exists.", width=400)
                function_message_frame.grid(row=0,columnspan=2)
                button_ok = Button(frame, text= "Ok", command= lambda: top.destroy(),background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)

    def ValidCode(self):
        with open("user_functions/check_function.py", 'w',encoding='utf-8') as file: 
            file.write("def " + self.name + "(funcArgs):" + '\n')
            file.write(self.func_code)

        p = subprocess.Popen("pyflakes user_functions/check_function.py", stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)

        #if not empty means there IS an error
        if p.communicate()[1].decode('utf-8'):      
            self.ShowFunctionErrors(p.communicate()[1].decode('utf-8'))
        else:
            return True

    def ShowFunctionErrors(self,errors):
        top = Toplevel()
        frame = Frame(top)
        frame.pack()

        err_message = Message(frame, text=errors)
        err_message.pack()
        top.bind("<FocusOut>", lambda event: event.widget.destroy())
        top.mainloop()

    def WriteFunction(self):
            
    

        path1 = "user_functions/" + self.func_type.lower() + "_functions.py"
        path2 = "user_functions/check_function.py"
        f1 = open(path1, 'a+')
        f2 = open(path2, 'r')

        
        # appending the contents of the valid function to its respective file
        if os.stat(path1).st_size <= 2:
            f1.write(f2.read())
        else:
            f1.write('\n'+ '\n' + f2.read())

        # writing the name to the library as well
        library = json.load(open('library.json','r'))                   

        function_to_add = {"Name" : self.name}

        library[self.func_type + "Functions"].append(function_to_add)
        json_string = json.dumps(library, indent=4)
        
        out = open('library.json', "w", encoding='utf-8')
        out.write(json_string)
        out.close()

    def FunctionNameTaken(self):
        from user_functions import evaluate_functions, compute_functions
        if self.func_type == "Compute":
           if self.name in dir(compute_functions): 
               return True
        elif self.func_type == "Evaluate":
            if self.name in dir(evaluate_functions):
                return True
        return False

#this function assembles the xml tree using the policy attributes collected
# at the end the function also writes this tree to 'output.xml'
def CreateXMLFile(rules, objectLists, dictionaries, description):           
    policyRuleSet = ET.Element("PolicyRuleSet")                                 
    policyRuleSet.set("dtdVersion","0.1")

    for i in range(len(rules)):
        policyRule = ET.SubElement(policyRuleSet, "PolicyRule")
        policyRule.set("name", str(rules[i].id))
        policyRule.set("quantifier", str(rules[i].quantifier))
        policyRule.set("evaluate", str(rules[i].evaluate))
        if (rules[i].description != ""):
            rule_description = ET.SubElement(policyRule, "Description")
            rule_description.text = rules[i].description

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
   
def UserMode():
    my_policies = [] 

    #RenderLibrary has a boolean field that indicates if user picked DevMode
    #It also has a field of picked policies to be enxtended onto our my_policies array
    pickedPolicies = RenderLibrary() 
    devMode = pickedPolicies.switch_dev
    my_policies.extend(pickedPolicies.my_policies)

    FunctionCreator() if devMode else None

    my_rules = []
    my_objectLists = []
    my_dictionaries = []

    #when creating my_policies, we overwrite the rule id's to be sequentially increasing,
    #regardless of their original id's in their respective Policies.
    ruleNum = 1
    for i in range(len(my_policies)):
        for k in range(len(my_policies[i].rules)):       
            my_policies[i].rules[k].id = str(ruleNum)    
            my_rules.append(my_policies[i].rules[k])
            ruleNum = ruleNum + 1
        my_objectLists.extend(my_policies[i].objectLists)
        my_dictionaries.extend(my_policies[i].dictionaries)

    #we can only have one Description object per PolicyRuleSet. In our case it is
    #the description of the last policy that makes up my_policies
    my_description = my_policies[len(my_policies) - 1].description if my_policies else Description("")  

    CreateXMLFile(my_rules, my_objectLists, my_dictionaries, my_description)
    PolicyPublisher() if devMode else None  
