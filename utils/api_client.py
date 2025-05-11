import requests
from config.settings import BASE_URL

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_posts(self):
        """获取所有帖子"""
        return requests.get(f"{self.base_url}/posts")

    def get_post(self, post_id: int):
        """根据ID获取单个帖子"""
        return requests.get(f"{self.base_url}/posts/{post_id}")

    def create_post(self, payload: dict):
        """创建新帖子"""
        headers = {"Content-Type": "application/json; charset=utf-8"}
        return requests.post(f"{self.base_url}/posts", json=payload, headers=headers)

    def update_post(self, post_id: int, payload: dict):
        """更新帖子"""
        headers = {"Content-Type": "application/json; charset=utf-8"}
        return requests.put(f"{self.base_url}/posts/{post_id}", json=payload, headers=headers)

    def delete_post(self, post_id: int):
        """删除帖子"""
        return requests.delete(f"{self.base_url}/posts/{post_id}")

# 创建一个客户端实例，方便在测试中导入使用
client = APIClient(base_url=BASE_URL)