from .helper import Helper


class UserHelpder(Helper):
    # search = {'username': 'blah blah'}
    # search = {'custom_attributes[key]': 'value'}
    def list(self, search={}):
        collection = self.pager(
            'users?{search}'.format(
                search='&'.join(['{key}={value}'.format(key=key, value=value) for key, value in search.items()])
            )
        )
        print('collected : {count}'.format(count=len(collection)))
        return collection
