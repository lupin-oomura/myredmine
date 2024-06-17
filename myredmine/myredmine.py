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

    def make_ticket(self, project_id, subject, description="", tracker_id=1, status_id=1, priority_id=1):
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

        url = f'{self.redmine_url}/issues.json'
        response = requests.post(url, headers=self.headers, data=json.dumps(issue_data))

        if response.status_code == 201:
            print("チケットが正常に作成されました。")
            print("チケットID:", response.json()['issue']['id'])
        else:
            print("チケットの作成に失敗しました。")
            print("ステータスコード:", response.status_code)
            print("レスポンス:", response.json())

    def get_tasks(self, project_id):
        url = f'{self.redmine_url}/issues.json'
        params = {
            'project_id': project_id, 
            'status_id': '*', 
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            issues = response.json()['issues']
            return issues
        else:
            print("タスクの取得に失敗しました。")
            print("ステータスコード:", response.status_code)
    
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