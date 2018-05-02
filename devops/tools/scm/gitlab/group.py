from .helper import Helper


class GroupHelper(Helper):
    def collect(self, full_path):
        collection = self.pager('groups?search={keyword}'.format(keyword=full_path.split('/')[-1]))
        print('collected : {count}'.format(count=len(collection)))
        if collection:
            result = filter(lambda x: full_path == x['full_path'], collection)
            return list(result)

    def create(self, path, name=None, description=None):
        response = self.request(method='post', path='groups', data={
            'name': name if name is not None else path,
            'path': path,
            'parent_id': None,
            'description': description,
        })

        if 201 == response.status_code:
            result = response.json()
            print('group ({id}) {fullpath} created'.format(id=result['id'], fullpath=result['full_path']))
            return result
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

    def delete_member(self, userid, groupid):
        response = self.request(method='delete', path='groups/{id}/members/{uid}'.format(id=groupid, uid=userid),
                                data={'user_id': userid})

        if 204 == response.status_code:
            return None
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

    def add_member(self, userid, access_level, groupid):
        try:
            self.delete_member(userid, groupid)
        except Exception as e:
            pass
        response = self.request(
            method='post',
            path='groups/{id}/members'.format(id=groupid),
            data={'user_id': userid, 'access_level': access_level})

        if 201 == response.status_code:
            result = response.json()
            return result
        else:
            print(response.status_code)
            print(response.content)
            raise Exception

    def get_members(self, groupid):
        response = self.request(method='get',path='groups/{id}/members'.format(id=groupid))
        if 200 == response.status_code:
            result = response.json()
            # print('added {user} as {role}'.format(user=result['name'], role=LEVEL_2_ROLE['s']))
            return result
        else:
            print(response.status_code)
            print(response.content)
            raise Exception
