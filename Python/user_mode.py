from tkinter import *


def AddRule(ruleList, rules):
    
    ruleList.insert(END, "Policy Rule " + str(ruleList.size() + 1))
    rules.append({'id': ruleList.size()})
    print(rules)
    

def GetFields(rule, quant, eval, desc):
    rule.update({'quantifier':quant})
    rule.update({'evaluate':eval})
    rule.update({'description':desc})
    print(rule)


def OpenRuleView(event,rules):
    selection = event.widget.curselection()
    print(selection)
    index = selection[0]
    data = event.widget.get(index)
    print(data)


    top = Toplevel()
    top.title(data)
    frame = Frame(top)
    frame.pack()
    policy_id_frame = Label(frame, text="Policy " + str(rules[index]['id']))
    policy_id_frame.grid(row=0,column=0)

    policy_quantifier_frame = LabelFrame(frame, text="Quantifier")
    policy_quantifier_frame.grid(row=0,column=1)

    v = IntVar()

    for_all = Radiobutton(policy_quantifier_frame, variable=v, value=1,text='for_all').pack(anchor=W)
    not_forall = Radiobutton(policy_quantifier_frame, variable=v, value=2,text='not_forall').pack(anchor=W)
    exists = Radiobutton(policy_quantifier_frame, variable=v, value=3,text='exists').pack(anchor=W)
    not_exists = Radiobutton(policy_quantifier_frame, variable=v, value=4,text='not_exists').pack(anchor=W)
    
    quantifier_options = {1:'for_all', 2: 'not_forall', 3:'exists', 4:'not_exists'}

    policy_evaluate_frame = LabelFrame(frame, text="Evaluate")
    policy_evaluate_frame.grid(row=0,column=2)

    evaluate = Entry(policy_evaluate_frame)
    evaluate.pack()

    policy_description_frame = LabelFrame(frame, text="Description")
    policy_description_frame.grid(row=1,column=2)

    description = Entry(policy_description_frame)
    description.pack()

    Button(frame, text= "Click to Show", command= lambda: GetFields(rules[index], quantifier_options[v.get()], evaluate.get(), description.get())).place(relx= .7, rely= .5, anchor= CENTER)

    # rules[index].update({'description':description.get()})


    # policy_quantifier_frame = LabelFrame(frame, text="Enter the function to evaluate")
    # policy_quantifier_frame.grid(row=0,column=1)




    # top.mainloop()
    print(rules)



    
def UserMode():
    root = Tk()
    root.title("Policy Creator")

    frame = Frame(root)
    frame.pack()
    
    policy_info_frame = LabelFrame(frame, text="Policy Rules")
    policy_info_frame.grid(row=0,column=0)

    # add_rule_label = Label(policy_info_frame, text="Add rule")
    # add_rule_label.grid(row=0, column=0)
    
    ruleList = Listbox(policy_info_frame,selectmode=SINGLE)
    ruleList.grid(row=0, column=2)

    rules = []
    add_rule_button = Button(policy_info_frame, text="Add rule...",command=lambda: AddRule(ruleList, rules))
    ruleList.bind("<<ListboxSelect>>", lambda event, arg=rules: OpenRuleView(event, arg))

    print(rules)
    add_rule_button.grid(row=0, column=0)

   

    mainloop()
