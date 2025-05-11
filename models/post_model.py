# 存放Pydantic数据模型
from typing import Optional, List
from pydantic import BaseModel, Field
# BaseModel用于定义结构化的数据模型
# Field用于为模型字段添加额外信息，如默认值、描述、校验规则等

# 这个Post是帖子的意思可以用多种方法不止post
class Post(BaseModel):
    # 对于POST请求，API不要求我们发送id，它会自动生成
    # 对于GET/PUT响应，id是存在的
    user_id: int = Field(alias="userId") # alias 允许我们在Python代码中使用 user_id
# 在 序列化（model.dict()）或发送请求时，Python 中的 user_id 字段会自动变成 userId
# 在 反序列化（解析响应）时，服务器返回的 userId 也会自动映射回 user_id
    id: Optional[int] = None    # 可以是 int 类型，也可以是 None，默认值为 None
    title: str
    body: str

# 创建帖子只能用post方法所以不需要传id
class PostCreate(BaseModel):
    user_id: int = Field(alias="userId")
    title: str
    body: str

class PostResponse(Post): # 继承自Post，确保所有字段都在
    id: int # 创建成功后，API会返回id，所以这里id是必须的

# 我们也可以直接使用 List[Post] 来表示帖子列表的响应
# 例如在测试代码中： posts: List[Post] = response.json()
# Pydantic 会自动尝试将列表中的每个字典转换为 Post 对象