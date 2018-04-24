from .helper import Helper
import json




class IssueHelper(Helper):
    FIELDS_ALL = [
        'issuetype',
        'parent',
        'timespent',
        'project',
        'fixVersions',
        'aggregatetimespent',
        'resolution',
        'resolutiondate',
        'workratio',
        'lastViewed',
        'watches',
        'created',
        'priority',
        'labels',
        'timeestimate',
        'aggregatetimeoriginalestimate',
        'versions',
        'issuelinks',
        'assignee',
        'updated',
        'status',
        'components',
        'timeoriginalestimate',
        'description',
        'aggregatetimeestimate',
        'summary',
        'creator',
        'subtasks',
        'reporter',
        'aggregateprogress',
        'environment',
        'duedate',
        'progress',
        'votes',
    ]

    FIELDS_COMMON = [
        'issuetype',
        'project',
        'resolution',
        'resolutiondate',
        'created',
        'priority',
        'assignee',
        'status',
        'components',
        'description',
        'summary',
        'creator',
        'reporter',
        'duedate',
    ]

    def __init__(self, instance):
        self.instance = instance

    def search(self, jql, fields=[]):
        collection = self.pager('api/2/search', data={'jql': jql, 'fields': fields}, result_key='issues')
        print('collected : {}'.format(len(collection)))
        return collection
