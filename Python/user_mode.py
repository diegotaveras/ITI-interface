from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET
import inspect
import json
from xmlparser import xmlparser
import subprocess
import os
from networkx import DiGraph, topological_sort, simple_cycles, selfloop_edges
from policy_parse_v2 import gatherDataObjects, parseFunctionCall, DataObject, cycles, function_dict
from user_functions import evaluate_functions, compute_functions
import sys

class Description:
    def __init__(self, desc):
        self.description = desc

    def UpdateDescription(self, desc):
        self.description = desc

class Rule:
    num_rules = 0
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
            rule_num = Rule.num_rules + 1
            ruleList.insert(END, "Policy Rule " + str(rule_num))
            rules.append(Rule(str(rule_num)))
            Rule.num_rules += 1
    
    def OpenView(self,event,objectLists, dictionaries):
        
        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)
        
            

        top = Toplevel()
        top.title(data)

        top.geometry("600x350")
        frame = Frame(top)
        frame.pack()
        policy_id_frame = Label(frame, text="Rule " + str(self.id))
        policy_id_frame.grid(row=1,column=0)

        policy_quantifier_frame = LabelFrame(frame, text="Quantifier")
        policy_quantifier_frame.grid(row=1,column=1, padx=20)

        quantifier_options = {1:'for_all', 2: 'not_forall', 3:'exists', 4:'not_exists'}
        quantifier_to_options = { value:str(key) for key, value in quantifier_options.items()}

        v = IntVar(value= quantifier_to_options[self.quantifier] if self.quantifier != "" else 1)
    
        def Change(event):
            self.quantifier = quantifier_options[v.get()]

        for_all = Radiobutton(policy_quantifier_frame, variable=v, value=1,text="for_all",command=lambda:Change(event)).pack(anchor=W)
        not_forall = Radiobutton(policy_quantifier_frame, variable=v, value=2,text="not_forall",command=lambda:Change(event)).pack(anchor=W)
        exists = Radiobutton(policy_quantifier_frame, variable=v, value=3,text="exists",command=lambda:Change(event)).pack(anchor=W)
        not_exists = Radiobutton(policy_quantifier_frame, variable=v, value=4,text="not_exists",command=lambda:Change(event)).pack(anchor=W)
    
        policy_evaluate_frame = LabelFrame(frame, text="Evaluate")
        policy_evaluate_frame.grid(row=1,column=2)

        evaluate =  Listbox(policy_evaluate_frame)
        evaluate.pack()

        policy_description_frame = LabelFrame(frame, text="Description")
        policy_description_frame.grid(row=2,column=0, columnspan=4)

        description = Entry(policy_description_frame)
        description.pack()

        evaluateFunctions = getEvaluateFunctions()

        for i in range(len(evaluateFunctions)):                
            evaluate.insert(END, evaluateFunctions[i] + "()")

        eval_args = LabelFrame(frame,text="Function arguments")
        eval_args.grid(row=1,column=3,padx=20)  

        args_listbox = Listbox(eval_args, selectmode=MULTIPLE, activestyle='none')    
        args_listbox.grid(row=0,column=1) 
        currEvaluate = Label(frame, text= "Current evaluate: " + self.evaluate)
        currEvaluate.grid(row=0, column=2, columnspan=3, pady=20)
        evaluate.bind("<<ListboxSelect>>" , lambda event: EvaluateFunctionView(event, currEvaluate, self, objectLists, dictionaries, args_listbox))
        
        description.insert(INSERT, self.description)

        def BuildRule():
            self.setFields(quantifier_options[v.get()], self.evaluate, Description(description.get()))
            top.destroy()

        Button(frame, text= "Build rule", background='#86C5D8', command= lambda: BuildRule()).grid(row=3,columnspan=4,pady=10)

        top.mainloop()

class ObjectList:
    def __init__(self, name):
        self.name = name
        self.imported = False
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
        objectListListbox.insert(END, name)
        objectLists.append(ObjectList(name))
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

        objList_name_frame = Label(frame, text="Object List: " + str(objectLists[index].name))
        objList_name_frame.grid(row=0,column=0)
        objList_imported_frame = LabelFrame(frame, text="Imported")
        objList_imported_frame.grid(row=0,column=1)

        v = BooleanVar(value=objectLists[index].imported)

        imported = Checkbutton(objList_imported_frame, variable=v, text='Imported')
        imported.pack(anchor=W)
      
        objList_compute_frame = LabelFrame(frame, text="Compute")
        objList_compute_frame.grid(row=1,column=2)


        computeFunctions = getComputeFunctions()

        compute = Listbox(objList_compute_frame)
        compute.pack()

        for i in range(len(computeFunctions)):                
            compute.insert(END, computeFunctions[i] + "()")

        compute_args = LabelFrame(frame,text="Function arguments")
        compute_args.grid(row=1,column=3,padx=20)  

        args_listbox = Listbox(compute_args, selectmode=MULTIPLE, activestyle='none')    
        args_listbox.grid(row=1,column=1) 
        currCompute = Label(frame, text= "Current compute: " + objectLists[index].compute, justify=CENTER)
        currCompute.grid(row=0, column=2, columnspan=3)
        compute.bind("<<ListboxSelect>>" , lambda event: ComputeFunctionView(event, currCompute, objectLists[index], objectLists, dictionaries, args_listbox))

        def BuildObjList():
            objectLists[index].setFields(v.get(), objectLists[index].compute)
            top.destroy()

        Button(frame, text= "Build Object List", background='#86C5D8', command= lambda: BuildObjList()).grid(row=2,columnspan=4,pady=10)

        top.mainloop()



class Dictionary:
    def __init__(self, name):
        self.name = name
        self.imported = False
        self.compute = ""

    def setFields(self, imported, compute):
        self.imported = imported
        self.compute = compute

    @staticmethod
    def AddItem(dictionaryListbox, dictionaries, entry):
        name = entry.get()
        if entry.get() == "":
            return
        dictionaryListbox.insert(END,   name)
        
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


        computeFunctions = getComputeFunctions()

        compute = Listbox(dictionary_compute_frame)
        compute.pack()

        for i in range(len(computeFunctions)):                
            compute.insert(END, computeFunctions[i] + "()")

        compute_args = LabelFrame(frame,text="Function arguments")
        compute_args.grid(row=1,column=3,padx=20)  

        args_listbox = Listbox(compute_args, selectmode=MULTIPLE, activestyle='none')    
        args_listbox.grid(row=1,column=1) 
        currCompute = Label(frame, text= "Current compute: " + dictionaries[index].compute, justify=CENTER)
        currCompute.grid(row=0, column=2, columnspan=3)
        compute.bind("<<ListboxSelect>>" , lambda event: ComputeFunctionView(event, currCompute, dictionaries[index], objectLists, dictionaries, args_listbox))

        def BuildDict():
            dictionaries[index].setFields(v.get(), dictionaries[index].compute)
            top.destroy()

        Button(frame, text= "Build Dictionary", background='#86C5D8', command= lambda: BuildDict()).grid(row=2,columnspan=4,pady=10)

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
                #the option for whether a dict or array is present in case it's just a singular item
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

class RuleGroup:
    def __init__(self):
        self.name = ""
        self.rules = []
        self.args = ""
        
    def FillRulesListbox(self, listbox):
        for rule in self.rules:
            listbox.insert(END,"Rule: " + rule.id)

    def PopulateFromJSON(self, ruleGroupJson):
        self.name = ruleGroupJson["Name"]
        for each in ruleGroupJson["Rules"]:
            
            rule = Rule(each["PolicyRule"]['name'])
            rule.setFields(each["PolicyRule"]['quantifier'], each["PolicyRule"]['evaluate'], Description(each["PolicyRule"]['Description']) if "Description" in each else Description(""))
            self.rules.append(rule)
        print(self.rules)

    
    def AddItem(self,ruleListbox, ruleGroups, itemsExist):
        print("hey")
        if itemsExist:
            ruleListbox.insert(END, self.name + "<Group>")
            ruleGroups.append(self)    
    
    def OpenView(self,event, objectLists, dictionaries):

        selection = event.widget.curselection()
        print(selection)
        index = selection[0]
        data = event.widget.get(index)

        top = Toplevel()
        top.title(data)

        top.geometry("600x350")
        frame = Frame(top)
        frame.pack()
        policy_id_frame = Label(frame, text="Rule Group: " + str(self.name))
        policy_id_frame.grid(row=1,column=0)


        rules_listbox_frame = LabelFrame(frame, text="Rules")
        rules_listbox_frame.grid(row=1,column=1, padx=20)

        rules_listbox = Listbox(rules_listbox_frame, selectmode=SINGLE, activestyle='none')    
        rules_listbox.grid(row=1,column=1) 

        self.FillRulesListbox(rules_listbox)
        rules_listbox.bind("<<ListboxSelect>>", lambda event: self.rules[event.widget.curselection()[0]].OpenView(event, objectLists,dictionaries))

        eval_args = LabelFrame(frame,text="Rule Group Arguments")
        eval_args.grid(row=1,column=2,padx=20)  

        args_listbox = Listbox(eval_args, selectmode=MULTIPLE, activestyle='none')    
        args_listbox.grid(row=1,column=1) 

        for i in range(len(objectLists)):
            args_listbox.insert(END, objectLists[i].name)
        for i in range(len(dictionaries)):
            args_listbox.insert(END, dictionaries[i].name)

        arguments = []

        currEvaluate = Label(frame, text= "Current evaluate arguments: " + self.args)
        currEvaluate.grid(row=0, column=1, columnspan=2, pady=20)

        def AddArg(event, currEvaluate, arguments):
            idx = event.widget.curselection()[0]
            if event.widget.get(idx) not in arguments:
                event.widget.itemconfig(idx, {'bg':'#90EF90'})
                arguments.append(event.widget.get(idx))
            UpdateEvaluateFunction(currEvaluate, Rule(0), data)
            print(arguments)

        args_listbox.bind("<<ListboxSelect>>",  lambda event: AddArg(event, currEvaluate, arguments))
        

        def UpdateEvaluateFunction(currEvaluate, rule, data):
            signature = data + "("
            if rule.quantifier == "for_all":
                for k in range(len(arguments) - 1):
                    signature = signature + "@" + arguments[k] + ","
                signature = signature + "@" + arguments[-1] + ")"
            else:
                for k in range(len(arguments) - 1):
                    signature = signature + arguments[k] + ","
                signature = signature + arguments[-1] + ")"
            if rule.id != 0:
                rule.evaluate = signature
            self.args = signature.split("(")[1][:-1]
            currEvaluate.config(text="Current evaluate arguments: " + self.args)
            
            
            # currEvaluate = Label(frame, text= "Current evaluate arguments: " + rule.evaluate)
            # currEvaluate.grid(row=0, column=1, columnspan=2, pady=20)

        #TODO:
        #highlight listbox args that were picked and maintain the state

        # evaluate.bind("<<ListboxSelect>>" , lambda event: EvaluateFunctionView(event, currEvaluate, ruleGroups[index], [], [], args_listbox))
        
        # description.insert(INSERT, ruleGroups[index].description)
        # EvaluateFunctionView(event, currEvaluate, rule, objectLists, dictionaries, args_listbox)
       

        def BuildRuleGroup(currEvaluate):
            for rule in self.rules:
                evaluate_func = rule.evaluate.split("(")[0]
                UpdateEvaluateFunction(currEvaluate, rule, evaluate_func)
                
            

        Button(frame, text= "Build Rule Group", background='#86C5D8', command= lambda: BuildRuleGroup(currEvaluate)).grid(row=3,columnspan=4,pady=10)

        top.mainloop()

    




class PolicyCreator:
    def __init__(self):

        self.policy = Policy()
        
    
    def EditPolicy(self):
        self.clicked_objList = False
        self.clicked_dictionary = False
        root = Tk()
        root.title("Policy Creator")
        root.geometry("600x900")

        rules = self.policy.rules
        objectLists = self.policy.objectLists
        dictionaries = self.policy.dictionaries
        description = self.policy.description
        self.ruleGroups_library = []
        self.ruleGroups = []

        frame = Frame(root)
        frame.pack()
        
        policy_rules_frame = LabelFrame(frame, text="Policy Rules")
        policy_rules_frame.grid(row=2,column=0)

        imported_rules_frame = LabelFrame(frame, text="Imported Rule Groups")
        imported_rules_frame.grid(row=2,column=1)

        policy_objectLists_frame = LabelFrame(frame, text="Policy Object Lists")
        policy_objectLists_frame.grid(row=0,column=0, columnspan=2)

        policy_dictionaries_frame = LabelFrame(frame, text="Policy Dictionaries")
        policy_dictionaries_frame.grid(row=1,column=0, columnspan=2)

        policy_description_frame = LabelFrame(frame, text="Policy Description")
        policy_description_frame.grid(row=3,column=0,columnspan=2)


        self.map = {}
        self.idx = 0
        

        ruleListbox = Listbox(policy_rules_frame,selectmode=SINGLE)
        ruleListbox.grid(row=0, column=2)

        def ViewRule(event):
            idx = event.widget.curselection()[0]
            name = ruleListbox.get(idx)
            if (name[-7:] == "<Group>"):
                for each in self.ruleGroups:
                    if each.name == name[:-7]:
                        each.OpenView(event, dictionaries, objectLists)
            else:
                for each in rules:
                    if each.id == name[-1:]:
                        rules[idx].OpenView(event, dictionaries, objectLists)

        self.FillRuleListbox(ruleListbox,rules)
        inner_rule_frame = Frame(policy_rules_frame)
        inner_rule_frame.grid(row=0, column=0, padx=30)
        add_rule_button = Button(inner_rule_frame, text="Add rule...",command=lambda: Rule.AddItem(ruleListbox, rules, dictionaries or objectLists))
        add_rule_button.grid(row=0, column=0)
        ruleListbox.bind("<<ListboxSelect>>", lambda event, arg2=objectLists, arg3=dictionaries:  ViewRule(event)) 

        
        objectListListbox = Listbox(policy_objectLists_frame,selectmode=SINGLE)
        objectListListbox.grid(row=0, column=2)
        self.FillItemListbox(objectListListbox,objectLists)
        add_objectList_button = Button(policy_objectLists_frame, text="Add object list...",command=lambda: ObjectList.AddItem(objectListListbox, objectLists, objList_entry) if self.clicked_objList else None)
        add_objectList_button.grid(row=0, column=0)
        objectListListbox.bind("<<ListboxSelect>>", lambda event, arg=dictionaries, arg2=objectLists: ObjectList.OpenView(event, arg, arg2))
        objList_entry = Entry(policy_objectLists_frame,fg="#D3D3D3")
        objList_entry.insert(0, "Enter a name")
        objList_entry.bind("<Button-1>", lambda event: self.ClickEntry(event, "clicked_objList"))
        
        objList_entry.grid(row=1,column=0)

        dictionaryListbox = Listbox(policy_dictionaries_frame,selectmode=SINGLE)
        dictionaryListbox.grid(row=0, column=2)
        self.FillItemListbox(dictionaryListbox,dictionaries)
        add_dictionary_button = Button(policy_dictionaries_frame, text="Add dictionary...",command=lambda: Dictionary.AddItem(dictionaryListbox, dictionaries, dictionary_entry) if self.clicked_dictionary else None)
        add_dictionary_button.grid(row=0, column=0)
        dictionaryListbox.bind("<<ListboxSelect>>", lambda event, arg=dictionaries, arg2=objectLists: Dictionary.OpenView(event, arg, arg2))
        dictionary_entry = Entry(policy_dictionaries_frame,fg="#D3D3D3")
        dictionary_entry.insert(0, "Enter a name")
        dictionary_entry.bind("<Button-1>", lambda event: self.ClickEntry(event, "clicked_dictionary"))

        dictionary_entry.grid(row=1,column=0)

        ruleGroupListbox = Listbox(imported_rules_frame,selectmode=SINGLE)
        ruleGroupListbox.grid(row=0, column=2)
        self.FillRuleGroupListbox(ruleGroupListbox)
        inner_rg_frame = Frame(imported_rules_frame)
        inner_rg_frame.grid(row=0, column=0, padx=30)
        add_rg_button = Button(inner_rg_frame, text="Add rule group...",command=lambda: self.ruleGroups_library[ruleGroupListbox.curselection()[0]].AddItem(ruleListbox, self.ruleGroups, dictionaries or objectLists))
        add_rg_button.grid(row=0, column=0)
        ruleGroupListbox.bind("<Double-Button-1>", lambda event, arg=self.ruleGroups_library, arg2=dictionaries, arg3=objectLists: self.ruleGroups_library[event.widget.curselection()[0]].OpenView(event, arg2, arg3))
        
        description_entry = Text(policy_description_frame, width=50, height=5)
        description_entry.grid(row=0,column=1)

        inner_desc_frame = Frame(policy_description_frame)
        inner_desc_frame.grid(row=0, column=0, padx=30)
        add_description_button = Button(inner_desc_frame, text="Add description...",command=lambda: description.UpdateDescription(description_entry.get("1.0",'end-1c') and add_description_button.config(background='#90EF90')))
        add_description_button.grid(row=0, column=0)

        def ChangeColor(event, button):
            description_entry.edit_modified(False)
            button.config(background="#ffffff")
            
        description_entry.bind("<<Modified>>", lambda event, button=add_description_button: ChangeColor(event,button))
        
        done_button_frame = Frame(frame)
        done_button_frame.grid(row=4,column=0,pady=30, columnspan=2)
       
        button_done = Button(done_button_frame, text="Done", background='#86C5D8', command= lambda: root.destroy(),padx=20).pack()
        for ruleGroup in self.ruleGroups:
            rules.extend(ruleGroup.rules)    

        self.policy.Populate(rules, objectLists, dictionaries, description)
        
        mainloop()

    def ClickEntry(self,event, clicked):
            event.widget.config(fg = "black")
            event.widget.delete(0,END)
            event.widget.unbind("<Button-1>")
            value = getattr(self, clicked)
            setattr(self, clicked, not value)

    def FillRuleListbox(self, listbox, rules):
        for i in range(len(rules)):
            listbox.insert(END, "Policy Rule: " + rules[i].id)

    def FillItemListbox(self,listbox, items):
        for i in range(len(items)):
            listbox.insert(END, items[i].name)

    def FillRuleGroupListbox(self, listbox):
        library = json.load(open('library.json'))
        loaded_ruleGroups = library["RuleGroups"]
    
        for i in range(len(loaded_ruleGroups)):
            ruleGroup = RuleGroup()
            ruleGroup.PopulateFromJSON(loaded_ruleGroups[i])
            listbox.insert(END, ruleGroup.name)
            self.ruleGroups_library.append(ruleGroup)
            map
        

def CycleDetect(dictionaries, obj_lists):
    name_graph = DiGraph()
    global data_object_dict
    data_object_dict = {}
    dictionaries = [d for d in dictionaries if d.compute != ""]
    obj_lists = [obj for obj in obj_lists if obj.compute != ""]
    
    
    #no rules used for this call so pass in empty arr
    getFuncDict(obj_lists, dictionaries, [])    
    # get names of dictionaries and ObjectLists
    for d in dictionaries:
        
        name = d.name
        imported = d.imported
        compute  = d.compute
        data_object = DataObject(name, imported, 'dict', compute)
        data_object_dict[ name ] = data_object
        # if not name_graph.has_node(name):
        name_graph.add_node( name )

    for obj in obj_lists:
        name = obj.name
        imported = obj.imported
        compute  = obj.compute
        data_object = DataObject(name, imported, 'list', compute)
        data_object_dict[ name ] = data_object
        # if not name_graph.has_node(name):
        name_graph.add_node( name )

    # visit each object_list or dict that is not imported and
    # get names of object_lists or dictionaries upon which it is dependent
    # and create an edge in the graph
    #
    for name, data_obj in data_object_dict.items():
        if data_obj.imported:
            continue

        fc = data_obj.compute
        call_params = parseFunctionCall(fc)

        # ensure that function being called is known
        for arg in call_params[1:]:
            if arg.find('\'') == 0 and arg.count('\'') == 2 and arg.rfind('\'') == len(arg)-1:
                continue

            if arg not in data_object_dict:
                print('undefined function argument',arg)
                # exit(1)
                name_graph.add_edge(name, name)
                continue
            name_graph.add_edge(arg,name)


    # check for circular dependencies
    cg = simple_cycles( name_graph )
    cycles = []
    # cycles = [cycle for cycle in cg if len(cycle) > 1]
    
    for cycle in cg:
        if len(cycle) > 1:
            cycles.append(repr(cycle))
            print('cycle detected in object_set graph', repr(cycle))
        # exit(1)

    return len(cycles) != 0

def getComputeFunctions():
    arr = []
    for each in dir(compute_functions):
        if (each[:2] != "__"):
            arr.append(each)
    
    return arr

def getEvaluateFunctions():
    arr = []
    for each in dir(evaluate_functions):
        if (each[:2] != "__"):
            arr.append(each)
    
    return arr



def FillArgsListbox(data, object, args_listbox, objectLists, dictionaries):
    for i in range(len(objectLists)):
        copy = ObjectList(object.name) 
        copy.compute = data[:-2] + "(" + objectLists[i].name + ")"
        copy.imported = object.imported
        
        print(copy.imported)
        if objectLists[i].name != object.name and (objectLists[i].imported or (objectLists[i].compute != "" and not CycleDetect(dictionaries.copy(), objectLists.copy() + [copy]))):
            args_listbox.insert(END, objectLists[i].name)
    for i in range(len(dictionaries)):
        copy = Dictionary(object.name) 
        copy.compute = data[:-2] + "(" + dictionaries[i].name + ")"
        copy.imported = object.imported

        print(dictionaries[i].imported)
        if dictionaries[i].name != object.name and (dictionaries[i].imported or (dictionaries[i].compute != "" and not CycleDetect(dictionaries.copy() + [copy], objectLists.copy()) )):
            args_listbox.insert(END, dictionaries[i].name)


def ComputeFunctionView(event, currCompute, object, objectLists, dictionaries, args_listbox):
    index = event.widget.curselection()[0]
    data = event.widget.get(index)
    
    args_listbox.delete(0,END)
    
    FillArgsListbox(data, object, args_listbox, objectLists, dictionaries)

    arguments = []

    def AddArg(event, arguments):
        
        idx = event.widget.curselection()[0]
        if event.widget.get(idx) not in arguments:
            event.widget.itemconfig(idx, {'bg':'#90EF90'})
            arguments.append(event.widget.get(idx))
        print(arguments)
        UpdateComputeFunction(data)

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
        object.compute = signature
        currCompute.config(text="Current compute: " + object.compute)
        


def EvaluateFunctionView(event, currEvaluate, rule, objectLists, dictionaries, args_listbox):
    index = event.widget.curselection()[0]
    data = event.widget.get(index)

    args_listbox.delete(0,END)

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
        UpdateEvaluateFunction(data)

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
        button_done = Button(button_frame, text="Done", background='#86C5D8', command= lambda:  root.destroy(),padx=20)
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

        
        

    def Switch(self, button_dev):
        self.switch_dev = not self.switch_dev
        if self.switch_dev == False:
            button_dev.config(background='#f0f0f0')
        else:
            button_dev.config(background='#90EF90')

    def OpenPolicyView(self, event):
        index = event.widget.curselection()[0]
        policyJson = self.loaded_policies[index]
        
        

        # policyCreator = PolicyCreator()
        # policyCreator.policy.PopulateFromJson(policyJson)
        # policyCreator.EditPolicy()
        # policy = policyCreator.policy
        policy = Policy()
        policy.PopulateFromJson(policyJson)

        top = Toplevel()
        top.title(self.loaded_policies[index]['Name'])
        
        frame = Frame(top)
        frame.pack()
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
        rulesListbox.bind("<<ListboxSelect>>", lambda event, arg2=policy.objectLists, arg3=policy.dictionaries: policy.rules[event.widget.curselection()[0]].OpenView(event, arg2, arg3))

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

        button = ""
        if not self.FindPolicy(index):
            button = Button(frame, text= "Add Policy", background='#86C5D8',command= lambda: AddPolicy()).grid(row=2, columnspan=2)
        else:
            button = Button(frame, text= "Remove Policy", background='#FA6B84',command= lambda: RemovePolicy(self.removeIndex)).grid(row=2, columnspan=2)

        top.mainloop()  

    def FindPolicy(self,index):
            for i in range(len(self.my_policies)):
                if self.my_policies[i].name == self.loaded_policies[index]['Name']:
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
        self.root = Tk()
        self.root.title("Publish Policy")
        frame = Frame(self.root)
        frame.place(in_=self.root, anchor="c", relx=.5, rely=.5)

        self.root.geometry("650x300")
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
            button_ok = Button(frame, text= "Ok", command= lambda: self.root.destroy(), background='#86C5D8').grid(row=1, column=0,ipadx=40, padx=40)
            

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
class FunctionCreator:
    def __init__(self):

        # json_str = xmlparser(policy_xml, 'output.json')      
        self.root = Tk()
        self.root.title("Function Creator")
        self.root.geometry("500x200")

        frame = Frame(self.root)
        frame.pack()                


        function_frame = LabelFrame(frame, text="Function path")
        function_frame.grid(row=0,column=0,columnspan=2, padx=20)

        type_frame = LabelFrame(frame, text="Function type")
        type_frame.grid(row=0,column=4)


        function_path = Entry(function_frame)
        function_path.grid(row=0,column=0)

        self.switch_func = False
        

        button_func_type = Button(type_frame, background='#86C5D8', text="Compute" if self.switch_func else "Evaluate",command= lambda: self.Switch(button_func_type),justify=CENTER)
        button_func_type.grid(row=0, column=0, padx=10,pady=5)

    
        button_done = Button(self.root, text="Done", background='#86C5D8', command= lambda : self.WriteFunctionIfValid(function_path.get(), button_func_type.cget("text")), padx=20, justify=CENTER)
        button_done.pack(pady=20)

        mainloop()

    def Switch(self, button):
        self.switch_func = not self.switch_func
        if self.switch_func == False:
            button.config(text="Evaluate")
        else:
            button.config(text="Compute")

    def WriteFunctionIfValid(self, path, func_type):
        self.func_path = path
        self.func_type = func_type
        if self.ValidCode():
            if not self.FunctionNameTaken():
                self.WriteFunction()
                self.root.destroy()
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
        if (self.func_path == ""):
            return False
        p = subprocess.Popen("pyflakes " + self.func_path, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)

        #if not empty means there IS an error
        if p.communicate()[1].decode('utf-8'):      
            self.ShowFunctionErrors(p.communicate()[1].decode('utf-8'))
        else:
            with open(self.func_path) as file:
                lines = file.readlines()
                for line in enumerate(lines):
                    # here we are parsing for the function name in the given file path
                    if "def" in line[1]:
                        self.name = line[1].split()[1].split("(")[0]
            return True

    def ShowFunctionErrors(self,errors):
        top = Toplevel()
        frame = Frame(top)
        frame.pack()
        import webbrowser
        err_message = Message(frame, text=errors)
        err_message.pack()
        top.bind("<FocusOut>", lambda event: event.widget.destroy())

        #open the function file but keep the function creator windows on top
        try:
            if sys.platform == "win32":
                os.startfile(self.func_path)
            elif sys.platform.startswith("linux"):
                subprocess.call(["xdg-open", self.func_path])
        except:
            webbrowser.open(self.func_path)

        
        self.root.attributes('-topmost',1)
        top.attributes('-topmost',1)
        top.mainloop()

    def WriteFunction(self):
        path1 = "user_functions/" + self.func_type.lower() + "_functions.py"
        path2 = self.func_path
        f1 = open(path1, 'a+')
        f2 = open(path2, 'r')

        # appending the contents of the valid function to its respective file.
        if os.stat(path1).st_size <= 2:
            f1.write(f2.read())
        else:
            f1.write('\n'+ '\n' + f2.read())
        
        # writing the name to the library as well
        # library = json.load(open('library.json','r'))                   
        # function_to_add = {"Name" : self.name}
        # library[self.func_type + "Functions"].append(function_to_add)
        # json_string = json.dumps(library, indent=4)
        # out = open('library.json', "w", encoding='utf-8')
        # out.write(json_string)
        # out.close()

    def FunctionNameTaken(self):
        if self.func_type == "Compute":
           if self.name in dir(compute_functions): 
               return True
        elif self.func_type == "Evaluate":
            if self.name in dir(evaluate_functions):
                return True
        return False

def getFuncDict(objLists, dictionaries, rules):
    global function_dict
    
    for objList in objLists:
        if not objList.imported:
            name = objList.compute.split('(')[0]
            function_dict.update({name: getattr(compute_functions,name)})

    for dict in dictionaries:
        if not dict.imported:
            name = dict.compute.split('(')[0]
            function_dict.update({name : getattr(compute_functions,name)})

    for rule in rules:
        name = rule.evaluate.split('(')[0]
        print(name)
        function_dict.update({name : getattr(evaluate_functions,name)})
    print(function_dict)

#this function assembles the xml tree using the policy attributes collected
# at the end the function also writes this tree to 'output.xml'
#returns the root of the xml tree object
def CreateXMLTree(rules, objectLists, dictionaries, description):           
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

    return tree

def WriteXMLTree(tree, file_name):
    with open(file_name, 'wb') as file: 
        ET.indent(tree) 
        tree.write(file,xml_declaration=True,encoding='utf-8')
   
def ShowCycles(cycles):
    root = Tk()
    root.title("Cycles Detected")
    root.geometry("600x600")

    main_frame = Frame(root)
    main_frame.pack(expand=True, fill='both')

    label_frame = Frame(main_frame)
    label_frame.pack(pady=20)

    max_width = 0
    for cycle in cycles:
        cycle_label = Label(label_frame, text="There was a cycle detected in object_set graph " + cycle + ".", wraplength=600)
        cycle_label.pack(anchor='w')
        label_width = cycle_label.winfo_reqwidth() 
        if label_width > max_width:
            max_width = label_width

    for child in label_frame.winfo_children():
        child.configure(width=max_width)

    buttons_frame = Frame(main_frame)
    buttons_frame.pack(pady=20)

    global repeat
    repeat = False 
    def OpenPolicyEditor():
        global repeat
        repeat = True
        root.destroy()
        
    
    def ClosePolicyEditor():
        global repeat
        repeat = False
        root.destroy()

    button_done = Button(buttons_frame, text="Edit Policy", background='#86C5D8', command=lambda: OpenPolicyEditor(), padx=10)
    button_done.pack(side='left')

    button_separation = Frame(buttons_frame, width=30)
    button_separation.pack(side='left')

    button_edit = Button(buttons_frame, text="Done", background='#86C5D8', command= lambda:ClosePolicyEditor(), padx=10)
    button_edit.pack(side='left')

    root.mainloop()
    return repeat

# this class evaluates the created policy based 
class PolicyEvaluator:
    def __init__(self):
        
        self.root = Tk()
        self.root.title("Policy Rule Evaluator")
        frame = Frame(self.root)
        frame.place(in_=self.root, anchor="c", relx=.5, rely=.5)

        self.root.geometry("650x300+450+200")
        policy_message_frame = Message(frame,text="Do you want to evaluate the policy rules you have assembled?", width=400, pady=20)
        policy_message_frame.grid(row=0,column=0,columnspan=3)


        policy_xml_frame = LabelFrame(frame,text="Policy file")
        policy_xml_frame.grid(row=1,column=0)
        policy_xml_entry = Entry(policy_xml_frame)
        policy_xml_entry.insert(END, "output.xml")
        policy_xml_entry.pack()


        flows_json_frame = LabelFrame(frame,text="Flows file (optional)")
        flows_json_frame.grid(row=1,column=1, padx="20px")
        flows_file_entry = Entry(flows_json_frame)
        flows_file_entry.pack()

        network_json_frame = LabelFrame(frame,text="Network file")
        network_json_frame.grid(row=1,column=2)
        network_file_entry = Entry(network_json_frame)
        network_file_entry.pack()
        
        self.policy_file = policy_xml_entry.get()
        self.flows_file = flows_file_entry.get()
        self.network_file = network_file_entry.get()
        
    
        button_no = Button(frame, text= "No", command= lambda: quit(),background='#FA6B84').grid(row=2, column=0,columnspan=2,ipadx=40, padx=40, pady=20)
        button_yes = Button(frame, text= "Yes", command= lambda: self.EvaluatePolicy(),background='#90EF90').grid(row=2, column=1,columnspan=2,ipadx=40,pady=20)
        mainloop()

    def EvaluatePolicyRules(self):

        if (self.flows_file == ""):
            p = subprocess.Popen("python ../scripts/policy_evaluate.py -xml " + self.policy_file + " -network " + self.network_file, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            print(p.communicate()[1].decode('utf-8'))
        else:
            p = subprocess.Popen("python ../scripts/policy_evaluate.py -xml " + self.policy_file + " -flows " + self.flows_file + " -network " + self.network_file, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            print(p.communicate()[1].decode('utf-8'))




def UserMode():
    my_policies = [] 
    
    #RenderLibrary has a boolean field that indicates if user picked DevMode
    #It also has a field of picked policies to be enxtended onto our my_policies array
    pickedPolicies = RenderLibrary() 
    devMode = pickedPolicies.switch_dev
    my_policies.extend(pickedPolicies.my_policies)

    if devMode:
        policyCreator = PolicyCreator()
        repeat = True
        while repeat:
            global cycles
            cycles.clear()
            policyCreator.EditPolicy()

            createdPolicy = policyCreator.policy
            getFuncDict(createdPolicy.objectLists, createdPolicy.dictionaries, createdPolicy.rules)
            
            root = CreateXMLTree(createdPolicy.rules, createdPolicy.objectLists, createdPolicy.dictionaries, createdPolicy.description)
            gatherDataObjects(root)
            print(cycles)
            if cycles:
                #returning True means we want to edit.
                repeat = ShowCycles(cycles)
                print(repeat)
            else:
                repeat = False
                    

        my_policies.append(policyCreator.policy)
        print(function_dict)
        FunctionCreator()
        
    
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
    print(my_rules)
    root = CreateXMLTree(my_rules, my_objectLists, my_dictionaries, my_description)
    WriteXMLTree(root, "output.xml")
    PolicyPublisher() 
    PolicyEvaluator()
