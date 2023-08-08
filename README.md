# ITI-interface

GUI made with Python to provide users an easy way to create and evaluate best practice security policies on a given OT network. 

The my-app folder contains the web application made with Angular

## Running the tool:

1. Git clone this repository or download to your local machine.

2. Open a terminal window and run `cd Python` to access the folder for the tool GUI. 
### User mode

#### To run the GUI on user mode: 

    python interface.py

#### Policy Library

The first window of User Mode provides a way to pick previously created Policies which have been uploaded to the Policy library. Clicking on a policy will show the attributes (rules/object lists/dictionaries/descriptions) associated with the Policy.

You will have the option to "Add Policy" for the selected Policy. This option will add all of the attributes of the policy to your own Policy file. You may combine as many of these policies as you want.

You also have the option to remove a Policy that you have picked by clicking on it and selecting "Remove Policy" 

Picking a policy will combine **ALL** attributes of the policy into your own. If you want a way to only pick or combine specific **rules**, you must choose Dev Mode by clicking the button on the top right of the Policy Library window, and closing this window.

### Dev Mode

Windows found in Dev Mode:

1. [Policy Creator](#policy-creator) (shortcut: create-policy)
 
2. [Policy Publisher](#policy-publisher) (shortcut: publish)

3. [Policy Evaluator](#policy-evaluator) (shortcut: evaluate)

4. [Function Creator](#function-creator) (shortcut: create-function)

While the following windows/components will open as part of the Dev Mode flow, each window can be opened on its own by using the following command structure:

    python interface.py --<shortcut>
#### Policy Creator

* The policy creator allows you to create and manage your own policy file.

* The [ideal flow](#note-on-dependencies) is to begin by defining imported object-lists/dictionaries, then define non-imported.

* Imported object-lists/dictionaries will need to be added and defined in the **global_dict** map found in the *policy_parse_v2.py* file, in order for the [explicit evaluation step](#policy-rule-evaluator) for your policy to be successful. This is because the **global_dict** will be used for both user-defined, and pre-defined (imported) attributes, the ladder of which the user may have no input in creating. ***However, you may still define any attribute as imported for the purpose of generating the policy.xml file.***

* Then, you may define rules and include existing [Rule Groups](#rule-groups) in your Policy Rules section. 

* Finally, you may define a description for the policy by typing it in the respective textbox and clicking "Add Description...". You may update the description at any time but must always click "Add description..." to save.


##### Note on dependencies:

*You will notice that upon picking the compute function for each of the attributes, these functions' arguments will create dependencies on other previously defined attributes.* 

*The GUI prevents dependencies from forming by checking whether each argument option would create a dependency cycle, and if it does, the argument will not appear as a selectable option. Argument dependencies are the reason why defining imported attributes first is best practice, as they do not have a compute function and therefore successfully end the dependency chain.* 

*This also means that at least one imported attribute is necessary when defining a valid attribute set for policies.*


#### Policy Publisher

The Policy Publisher allows users to publish their created policy to the *library.json* file. This will mean that the policy will appear on the [Policy Library](#policy-library) section of the GUI, allowing for later uses. 

The policy that will be published is based on the contents of whatever is currently in the *policy.xml* file.

#### Policy Evaluator

The Policy Evaluator allows users to evaluate the Policy Rules that they have defined in the *policy.xml* file. Though the evaluator evaluates the *policy.xml* file by default, the user may change the file by providing the relative path to any other valid xml file that represents a policy.

The user should always provide a "network" file's relative path to the entry box. The "flows" file is optional.


#### Function Creator

The Function Creator is the way in which the user may easily define functions that will either be computed by object-lists/dictionaries, or evaluated by rules.

To define a function, simply enter the relative path to a defined function. Then click on the function type button to toggle between an evaluate or a compute function.

The function creator will determine whether the function code syntax is correct and the function name is valid before successfully adding the function to the *user_functions* directory.


#### Rule Groups

Rule Groups are groupings of Policy Rules that may be added in bulk to the user's policy file. This provides users a way to follow certain security standards by simply clicking the Rule Group and then clicking "Add Rule Group...".

Best practice is to first inspect your selected Rule Group by double clicking on it. From here you should select the object-lists/dictionaries that every rule in the Rule Group will be evaluated with. After the Rule Group is added to your Policy Rules, you may still change the object-lists/dictionaries that you want to evaluate it with. You may also still customize each individual Rule in the Rule Group separately by clicking on it, making your changes, and clicking "Build Rule...".



