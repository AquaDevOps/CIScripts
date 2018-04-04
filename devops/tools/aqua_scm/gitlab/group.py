from .helper import Helper


class GroupHelper(Helper):
    def list(self, keyword):
        collection = self.pager('groups?search={keyword}'.format(keyword=keyword))
        print('collected : {count}'.format(count=len(collection)))
        return collection
