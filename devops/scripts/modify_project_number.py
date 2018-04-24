import re


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
    if len(project_number)!=2:
        project_number='__'
    for s in str_data:
        if len(s) == 4:
            project_number=project_number+ s
            break
    if len(project_number)!=6:
        project_number=project_number+'____'
    for i in int_data:
        if len(i) == 4:
            project_number = project_number + i
            break
    if len(project_number)!= 10:
        project_number = project_number+ '____'
    for i in int_data:
        if len(i) == 3:
            project_number = project_number + i
            break
    if len(project_number)!= 13:
        project_number = project_number+ '___'
    return project_number