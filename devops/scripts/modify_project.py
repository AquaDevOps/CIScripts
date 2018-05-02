import re
import time
from datetime import datetime


def switch_time(value):
    f_value = float(value)
    t_value = time.localtime(f_value)
    result = time.strftime('%Y-%m-%d %H:%M:%S', t_value)
    return result


def switch_to_time(value):
    value = switch_time(value)
    result = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    result = result.strftime('%Y-%m-%d %H:%M:%S')
    return result

def modify_project_number(s):
    int_data = re.findall('[0-9]+', s)
    str_data = re.findall('[A-Za-z]+', s)
    # print(int_data)
    # print(str_data)
    project_number =''
    for s in str_data:
        if len(s) == 2:
            project_number=project_number+ s
            break
        elif len(s) == 6:
            project_number = project_number + s
    if len(project_number)!=2 and len(project_number)!=6:
        project_number='__'
    for s in str_data:
        if len(s) == 4:
            project_number=project_number+ s
            break
    for i in int_data:
        if len(i) == 4:
            project_number = project_number + i
            break
    for i in int_data:
        if len(i) == 3:
            project_number = project_number + i
            break
    for i in int_data:
        if len(i) == 7:
            project_number = project_number + i
            break
    return project_number

# old={'owner': ['lipengfei']}
# new={'owner': ['lipengfei'], 'develop': ['A', 'B']}

def diff(old, new):
    message = '\n'+ switch_to_time(time.time())
    old_role_list =[]
    for k in old.keys():
        old_role_list.append(k)
    for n_k in new.keys():
        if n_k in old_role_list:
            for n_m in new[n_k]:
                if n_m in old[n_k]:
                    old[n_k].remove(n_m)
                else:
                    message = message +'\n' + ' add '+ n_m + ' to ' + n_k
            if len(old[n_k]):
                for o_m in old[n_k]:
                    message = message +'\n'+ ' delete '+ o_m + ' from ' + n_k
            old_role_list.remove(n_k)
        else:
            message = message +'\n'+ ' add role ' + n_k + ', memebers : ' + ','.join(new[n_k])
    if len(old_role_list):
        for o_k in old_role_list:
            message = message +'\n'+ ' delete role ' + o_k + ', members : ' + ','.join(old[o_k])
    return message

