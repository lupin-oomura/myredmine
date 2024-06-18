import requests
import json

class myredmine:
    redmine_url = None
    api_key = None
    headers = None

    def __init__(self, url, api_key):
        self.redmine_url = url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': api_key
        }

    def get_project(self):
        url = f'{self.redmine_url}/projects.json'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            projects = response.json()['projects']
            return projects
        else:
            print("プロジェクトの取得に失敗しました。")
            print("ステータスコード:", response.status_code)

    def get_tracker_id(self):
        url = f'{self.redmine_url}/trackers.json'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            trackers = response.json()['trackers']
            return trackers
        else:
            print("トラッカーの取得に失敗しました。")
            print("ステータスコード:", response.status_code)

    def get_issue_id(self):
        url = f'{self.redmine_url}/issue_statuses.json'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            statuses = response.json()['issue_statuses']
            return statuses
        else:
            print("ステータスの取得に失敗しました。")
            print("ステータスコード:", response.status_code)

    def get_priority_id(self):
        url = f'{self.redmine_url}/enumerations/issue_priorities.json'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            priorities = response.json()['issue_priorities']
            return priorities
        else:
            print("優先度の取得に失敗しました。")
            print("ステータスコード:", response.status_code)

    def make_ticket(self, project_id, subject, description="", tracker_id=1, status_id=1, priority_id=1, assigned_to_id=None):
        issue_data = {
            "issue": {
                "project_id": project_id,
                "subject": subject,
                "description": description,
                "tracker_id": tracker_id,
                "status_id": status_id,
                "priority_id": priority_id,
            }
        }

        if assigned_to_id is not None:
            issue_data["issue"]["assigned_to_id"] = assigned_to_id

        url = f'{self.redmine_url}/issues.json'
        response = requests.post(url, headers=self.headers, data=json.dumps(issue_data))

        if response.status_code == 201:
            print("チケットが正常に作成されました。")
            print("チケットID:", response.json()['issue']['id'])
        else:
            print("チケットの作成に失敗しました。")
            print("ステータスコード:", response.status_code)
            print("レスポンス:", response.json())

    def get_tickets(self, project_id:int, user_id:int=None, is_closed:bool=None):
        url = f'{self.redmine_url}/issues.json'
        params = {
            'project_id': project_id, 
            'status_id': '*', 
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            issues = response.json()['issues']
            if user_id is not None :
                issues = [ x for x in issues if 'assigned_to' in x and user_id == x['assigned_to']['id'] ]
            if is_closed is not None :
                issues = [ x for x in issues if is_closed == x['status']['is_closed'] ]

            return issues
        else:
            print("タスクの取得に失敗しました。")
            print("ステータスコード:", response.status_code)
    
    def get_tickets_simple(self, project_id:int, user_id:int=None, is_closed:bool=None):
        tickets = self.get_tickets(project_id, user_id, is_closed)
        simpletickets = []

        for t in tickets :
            d = {
                "id": t['id'],
                "tracker": t['tracker']['name'],
                "status": t['status']['name'],
                "is_closed": t['status']['is_closed'],
                "subject": t['subject'],
                "due_date": t['due_date'],
            }
            if 'assigned_to' in t :
                d["assigned_to"] = t["assigned_to"]['id']
            else :
                d["assigned_to"] = None

            simpletickets.append(d)

        return simpletickets
    
        # [
        #     {
        #         'id': 6, 
        #         'project': {'id': 1, 'name': 'ビジネス立ち上げフェーズ'}, 
        #         'tracker': {'id': 2, 'name': 'Task'}, 
        #         'status': {'id': 1, 'name': 'Before Start', 'is_closed': False}, 
        #         'priority': {'id': 1, 'name': 'normal'}, 
        #         'author': {'id': 1, 'name': '真 大村'}, 
        #         'subject': 'test', 'description': '', 
        #         'start_date': '2024-06-14', 
        #         'due_date': None, 
        #         'done_ratio': 0, 
        #         'is_private': False, 
        #         'estimated_hours': None, 
        #         'total_estimated_hours': None, 
        #         'created_on': '2024-06-14T07:15:59Z', 
        #         'updated_on': '2024-06-14T07:15:59Z', 
        #         'assigned_to': {'id': 1, 'name': '真 大村'},
        #         'closed_on': None
        #     }, {
        #         'id': 5, 
        #         'project': {'id': 1, 'name': 'ビジネス立ち上げフェーズ'}, 
        #     }
        # ]



    def get_news(self, project_id) :
        news_url = f"{self.redmine_url}/projects/{project_id}/news.json"
        response = requests.get(news_url, headers=self.headers)

        # レスポンスが成功したか確認します
        if response.status_code == 200:
            news_data = response.json()['news']
            return news_data
        else:
            print(f"エラーが発生しました: {response.status_code}")


    def get_wiki(self, project_id, wiki_page_title:str="wiki") :
        # wiki_url = f"{self.redmine_url}/projects/{project_id}/wiki/index.json"
        # response = requests.get(wiki_url, headers=self.headers)
        # if response.status_code == 200:
        #     wiki_pages = response.json()['wiki_pages']
        #     return wiki_pages            
        # else:
        #     print(f"エラーが発生しました: {response.status_code}")


        wiki_page_url = f"{self.redmine_url}/projects/{project_id}/wiki/{wiki_page_title}.json"
        response = requests.get(wiki_page_url, headers=self.headers)

        if response.status_code == 200:
            # JSONデータをパースします
            wiki_page = response.json()['wiki_page']
            return wiki_page
        else:
            print(f"エラーが発生しました: {response.status_code}")




    def get_members_simple(self, project_id) :
        memberships_url = f"{self.redmine_url}/projects/{project_id}/memberships.json"
        response = requests.get(memberships_url, headers=self.headers)

        # レスポンスが成功したか確認します
        if response.status_code == 200:
            memberships = response.json()['memberships']
            mems = []
            for x in memberships :
                mems.append( {"id": x['user']['id'], "name": x['user']['name']} )
            return mems
        else:
            print(f"エラーが発生しました: {response.status_code}")




    # def get_issue_details(self, issue_id):
    #     url = f'{self.redmine_url}/issues/{issue_id}.json'
    #     response = requests.get(url, headers=self.headers)

    #     if response.status_code == 200:
    #         issue = response.json()['issue']
    #         return issue
    #     else:
    #         print("チケット詳細の取得に失敗しました。")
    #         print("ステータスコード:", response.status_code)

    # def update_ticket(self, issue_id, update_fields):
    #     issue_data = {
    #         "issue": update_fields
    #     }

    #     url = f'{self.redmine_url}/issues/{issue_id}.json'
    #     response = requests.put(url, headers=self.headers, data=json.dumps(issue_data))

    #     if response.status_code == 200:
    #         print("チケットが正常に更新されました。")
    #     else:
    #         print("チケットの更新に失敗しました。")
    #         print("ステータスコード:", response.status_code)
    #         print("レスポンス:", response.json())

    # def delete_ticket(self, issue_id):
    #     url = f'{self.redmine_url}/issues/{issue_id}.json'
    #     response = requests.delete(url, headers=self.headers)

    #     if response.status_code == 204:
    #         print("チケットが正常に削除されました。")
    #     else:
    #         print("チケットの削除に失敗しました。")
    #         print("ステータスコード:", response.status_code)

    # def add_user_to_project(self, project_id, user_id, role_id):
    #     membership_data = {
    #         "membership": {
    #             "user_id": user_id,
    #             "role_ids": [role_id]
    #         }
    #     }

    #     url = f'{self.redmine_url}/projects/{project_id}/memberships.json'
    #     response = requests.post(url, headers=self.headers, data=json.dumps(membership_data))

    #     if response.status_code == 201:
    #         print("ユーザーがプロジェクトに正常に追加されました。")
    #     else:
    #         print("ユーザーの追加に失敗しました。")
    #         print("ステータスコード:", response.status_code)
    #         print("レスポンス:", response.json())

    # def remove_user_from_project(self, membership_id):
    #     url = f'{self.redmine_url}/memberships/{membership_id}.json'
    #     response = requests.delete(url, headers=self.headers)

    #     if response.status_code == 204:
    #         print("ユーザーがプロジェクトから正常に削除されました。")
    #     else:
    #         print("ユーザーの削除に失敗しました。")
    #         print("ステータスコード:", response.status_code)



if __name__ == '__main__' :
    rd = myredmine('http://206.189.152.51', '3a1e29b83a8b19f32f2fb8a500bc54683130fbed')
    pj = rd.get_project()
    print(pj)

    mem = rd.get_members_simple(1)
    print("---members--------")
    print(mem)

    print("---tasks--------")
    tasks = rd.get_tickets_simple(1, 1)
    print(tasks)

    print("---wiki--------")
    wiki = rd.get_wiki(1)
    print(wiki)

    print("---news--------")
    news = rd.get_news(1)
    print(news)
#     print(mem)


# [
#     {
#         'id': 1, 
#         'project': {
#             'id': 1, 
#             'name': 'ビジネス立ち上げフェーズ'
#         }, 
#         'user': {
#             'id': 1, 
#             'name': '真 大村'
#         },
#         'roles': [
#             {
#                 'id': 3, 
#                 'name': 'Admin'
#             }
#         ]
#     }, 
#     {
#         'id': 2, 
#         'project': {
#             'id': 1, 
#             'name': 'ビジネス立ち上げフェーズ'
#         }, 
#         'user': {
#             'id': 6, 
#             'name': '登央  木下'
#         }, 
#         'roles': [
#             {
#                 'id': 3, 
#                 'name': 'Admin'
#             }
#         ]
#     }, 
#     {
#         'id': 3, 'project': {'id': 1, 'name': 'ビジネス立ち上げフェーズ'}, 'user': {'id': 5, 'name': '豊 根津'}, 'roles': [{'id': 3, 'name': 'Admin'}]}]

