from snippets.sample_config import config

from devops.tools.database.libSQLServer import Connect as SQLServerConnect
from devops.tools.database.libMySQL import Connect as MySQLConnect
from devops.tools.database import simple_value


db_devops = MySQLConnect(config.db_devops)
db_user_crm = SQLServerConnect(config.db_user_crm)
db_product_crm = MySQLConnect(config.db_product_crm)
db_project_oms = MySQLConnect(config.db_project_oms)

projects = db_project_oms.execute('''
SELECT
    project.PROJECTNUM PROJECT_NUM,
    project.PROJECTNAME PROJECT_NAME,
    tbl_pm_user.LOGIN_NAME PM_LOGIN,
    tbl_pm_user.NAME PM_NAME,
    tbl_pm_mail.MAIL_USER PM_MAIL,
    tbl_dm_user.LOGIN_NAME DM_LOGIN,
    tbl_dm_user.NAME DM_NAME,
    tbl_dm_mail.MAIL_USER DM_MAIL
FROM
    oms.project_inplement project
    JOIN oms.mail_config tbl_pm_mail ON DEVELOPMENT_MANAGER = tbl_pm_mail.USERID
    JOIN oms.mail_config tbl_dm_mail ON PROJECTMANAGER = tbl_dm_mail.USERID
	JOIN oms.fw_t_ems_user tbl_pm_user ON tbl_pm_mail.USERID = tbl_pm_user.USER_ID
    JOIN oms.fw_t_ems_user tbl_dm_user ON tbl_dm_mail.USERID = tbl_dm_user.USER_ID
''')

template = 'INSERT INTO gsafety_resource.gsafety_project ({header}) VALUES ({values})'
for row in projects:
    db_devops.execute(
        template.format(header=', '.join(row.keys()), values=', '.join([simple_value(value) for value in row.values()]))
    )