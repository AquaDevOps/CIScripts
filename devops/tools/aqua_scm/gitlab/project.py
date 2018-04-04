from .helper import Helper


class ProjectHelper(Helper):
    def create(self, owner, path, name=None, description=None):
        response = self.request(method='post', path='projects/user/{userid}'.format(userid=owner), data={
            'user_id': owner,
            'name': name if name is not None else path,
            'path': path,
            # 'namespace_id':
            'description': description,
        })

        if 201 == response.status_code:
            return response.json()
        else:
            print(response.status_code)
            print(response.content)
            raise Exception
