from os import listdir as _listdir
from os.path import dirname as _dirname
from copy import deepcopy
from importlib import import_module as _import_module
from openktn.utils.targets import names as _target_names

base_package = __name__.replace('.base','')

def _not_implemented_conversion(item):
    raise NotImplementedError("This conversion has not been implemented yet")

list_api_forms=[filename.split('.')[0] for filename in _listdir(_dirname(__file__)) if filename.startswith('api')]

dict_api_forms={}
list_forms=[]

dict_is_form={}
dict_new_empty_ktn={}
dict_add_microstate={}
dict_add_transition={}
dict_get={}

for api_form in list_api_forms:
    module_api_form=_import_module('.'+api_form,base_package)
    form_name=module_api_form.form_name
    list_forms.append(form_name)
    dict_api_forms[form_name]=module_api_form
    dict_is_form.update(module_api_form.is_form)

for form_name in list_forms:

    dict_new_empty_ktn[form_name]= {}
    dict_add_microstate[form_name]= {}
    dict_add_transition[form_name]= {}
    dict_get[form_name]= {}

    for target_name in _target_names:
        dict_get[form_name][target_name]={}

    for method in dict_api_forms[form_name].__dict__.keys():
        if method.startswith('to_'):
            if method.endswith('_seq'):
                out_form_name=method[:-4].replace('to_','').replace('_','.')+':seq'
            elif method.endswith('_id'):
                out_form_name=method[:-3].replace('to_','').replace('_','.')+':id'
            else:
                out_form_name=method.replace('to_','').replace('_','.')
            dict_converter[form_name][out_form_name]= getattr(dict_api_forms[form_name],method)
        if method.startswith('get_'):
            option, target = method[4:].split('_from_')
            dict_get[form_name][target][option]=getattr(dict_api_forms[form_name], method)

    if 'new_empty_ktn' in dict_api_forms[form_name].__dict__.keys():
        dict_new_empty_ktn[form_name]=getattr(dict_api_forms[form_name],'new_empty_ktn')
    if 'add_microstate' in dict_api_forms[form_name].__dict__.keys():
        dict_add_microstate[form_name]=getattr(dict_api_forms[form_name],'add_microstate')
    if 'add_transition' in dict_api_forms[form_name].__dict__.keys():
        dict_add_transition[form_name]=getattr(dict_api_forms[form_name],'add_transition')

list_forms=sorted(list_forms)

if 'out_form_name' in globals():
    del(out_form_name)

del(list_api_forms, base_package)

