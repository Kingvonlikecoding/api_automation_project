import pytest
import allure # allure reporting
from typing import List # 用于类型提示
from utils.api_client import client # 导入我们创建的API客户端实例
from models.post_model import Post # 导入Pydantic模型
from assertpy import assert_that

@allure.feature("Posts API") # Allure特性：标记这个测试类/模块是关于Posts API的
@allure.story("Get Posts") # Allure故事：标记这个部分是关于获取帖子功能的(feature的子功能)
class TestGetPosts:

    @allure.title("Test Get All Posts - Basic Validation") # Allure标题：测试用例的标题
    @allure.description("This test verifies that the API returns a list of posts and basic status code.") # Allure描述
    def test_get_all_posts_status_and_list(self):
        with allure.step("Send GET request to /posts"): # Allure步骤：标记测试中的一个具体操作
            response = client.get_posts()

        with allure.step("Verify status code is 200"):
            assert_that(response.status_code,description=f"Expected status code 200, but got {response.status_code}").is_equal_to(200) 

        with allure.step("Verify response is a list"):
            response_data = response.json() # 转换为 Python 对象
            assert_that(response_data).described_as("Response data is not a list").is_instance_of(list)
            allure.attach(str(response.json()), name="Response JSON", attachment_type=allure.attachment_type.JSON)


    @allure.title("Test Get All Posts - Content Validation with Pydantic")
    @allure.description("This test validates the structure and data types of each post in the response using Pydantic.")
    def test_get_all_posts_pydantic_validation(self):
        with allure.step("Send GET request to /posts"):
            response = client.get_posts()

        with allure.step("Verify status code is 200"):
            assert_that(response.status_code, description=f"Expected status code 200, but got {response.status_code}").is_equal_to(200)

        response_data = response.json()
        allure.attach(str(response_data), name="Full Response JSON", attachment_type=allure.attachment_type.JSON)


        with allure.step("Validate each post in the list using Pydantic Post model"):
            assert_that(response_data).is_instance_of(list)
            assert_that(len(response_data),"Received an empty list of posts").is_greater_than(0)

            # 使用Pydantic进行列表验证
            try:
                # 类型注解使代码更清晰
                posts_validated: List[Post] = [Post.model_validate(item) for item in response_data]
                allure.attach(f"Successfully validated {len(posts_validated)} posts.", name="Pydantic Validation Log")
            except Exception as e:
                allure.attach(str(e), name="Pydantic Validation Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Pydantic validation failed: {e}") # 显式标记当前测试用例为“失败”，并附带错误信息

            # 简单抽样检查第一个post的内容 (可选，但有助于确认数据正确性)
            if posts_validated:
                first_post = posts_validated[0]
                with allure.step("Verify content of the first post"):
                    assert_that(isinstance(first_post.id, int)).is_true()
                    assert_that(isinstance(first_post.user_id, int)).is_true()
                    assert_that(isinstance(first_post.title, str) and len(first_post.title) > 0).is_true()
                    assert_that(isinstance(first_post.body, str) and len(first_post.body) > 0).is_true()
                    allure.attach(first_post.model_dump_json(indent=2), name="First Validated Post", attachment_type=allure.attachment_type.JSON)