from .helper import Helper


class UserHelpder(Helper):
    # search = {'username': 'blah blah'}
    # search = {'custom_attributes[key]': 'value'}
    def collect(self, search={}):
        collection = self.pager(
            'users?{search}'.format(
                search='&'.join(['{key}={value}'.format(key=key, value=value) for key, value in search.items()])
            )
        )
        print('collected : {count}'.format(count=len(collection)))
        return collection

    def userid(self, userid_or_username):
        return userid_or_username if isinstance(userid_or_username, int) else self.collect(
            search={'username': userid_or_username}
        )[0]['id']