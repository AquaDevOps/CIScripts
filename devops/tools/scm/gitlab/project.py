from .helper import (Helper, LEVEL_2_ROLE)


class ProjectHelper(Helper):
    def create(self, owner, path, groupid, name=None, description=None):
        response = self.request(method='post', path='projects/user/{userid}'.format(userid=owner), data={
            'user_id': owner,
            'name': name if name is not None else path,
            'path': path,
            'namespace_id': groupid,
            'description': description,
        })

        if 201 == response.status_code:
            result = response.json()
            print('project ({id}) {fullpath} created'.format(id=result['id'], fullpath=result['path_with_namespace']))
            return result
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

    def delete(self, projectid):
        print(projectid)
        response = self.request(method='delete', path='projects/{id}'.format(id=projectid))
        if 202 == response.status_code:
            return response.json()
        else:
            print(response.status_code)
            print(response.content)
            raise Exception


    def list(self, path_with_namespace):
        print(path_with_namespace)
        collection = self.pager('projects?search={keyword}'.format(keyword=path_with_namespace.split('/')[-1]))
        print('collected : {count}'.format(count=len(collection)))
        if collection:
            result = filter(lambda x: path_with_namespace == x['path_with_namespace'], collection)
            return list(result)
        # return collection

    def delete_member(self, userid, projectid):
        response = self.request(method='delete', path='projects/{id}/members/{uid}'.format(id=projectid, uid=userid),
                                data={'user_id': userid})

        if 201 == response.status_code:
            return response.json()
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

    def add_member(self, userid, access_level, projectid):
        # self.delete_member(userid, projectid)
        response = self.request(method='post', path='projects/{id}/members'.format(id=projectid),
                                data={'user_id': userid, 'access_level': access_level})

        if 201 == response.status_code:
            result = response.json()
            print('added {user} as {role}'.format(user=result['name'], role=LEVEL_2_ROLE[access_level]))
            return result
        else:
            print(response.status_code)
            print(response.content)
            raise Exception