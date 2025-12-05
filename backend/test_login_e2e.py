#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
端到端测试登录功能
使用正确的API端口（8002）测试完整的登录流程
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('login_e2e_test')

# API配置
API_BASE_URL = "http://localhost:8002"
LOGIN_URL = f"{API_BASE_URL}/auth/login"
CURRENT_USER_URL = f"{API_BASE_URL}/auth/me"
LOGOUT_URL = f"{API_BASE_URL}/auth/logout"

# 测试用户凭据
TEST_USER = {
    "username": "xxiaochang",
    "email": "xxiaochang@qq.com",
    "phone": "13160697108",
    "password": "password123"
}

class LoginE2ETester:
    """端到端登录测试类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
    
    def log_test_result(self, test_name, success, message=""):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "message": message
        }
        self.test_results.append(result)
        
        if success:
            logger.info(f"✅ {test_name}: {message}")
        else:
            logger.error(f"❌ {test_name}: {message}")
    
    def test_login_with_username(self):
        """测试使用用户名登录"""
        test_name = "使用用户名登录"
        
        try:
            login_data = {
                "identifier": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            
            response = self.session.post(
                LOGIN_URL,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.access_token = data["access_token"]
                    self.log_test_result(test_name, True, "登录成功，获取到访问令牌")
                    return True
                else:
                    self.log_test_result(test_name, False, f"登录成功但未返回访问令牌: {data}")
                    return False
            else:
                self.log_test_result(test_name, False, f"登录失败，状态码: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"登录过程中发生异常: {e}")
            return False
    
    def test_login_with_email(self):
        """测试使用邮箱登录"""
        test_name = "使用邮箱登录"
        
        try:
            login_data = {
                "identifier": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
            
            response = self.session.post(
                LOGIN_URL,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.access_token = data["access_token"]
                    self.log_test_result(test_name, True, "登录成功，获取到访问令牌")
                    return True
                else:
                    self.log_test_result(test_name, False, f"登录成功但未返回访问令牌: {data}")
                    return False
            else:
                self.log_test_result(test_name, False, f"登录失败，状态码: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"登录过程中发生异常: {e}")
            return False
    
    def test_login_with_phone(self):
        """测试使用手机号登录"""
        test_name = "使用手机号登录"
        
        try:
            login_data = {
                "identifier": TEST_USER["phone"],
                "password": TEST_USER["password"]
            }
            
            response = self.session.post(
                LOGIN_URL,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.access_token = data["access_token"]
                    self.log_test_result(test_name, True, "登录成功，获取到访问令牌")
                    return True
                else:
                    self.log_test_result(test_name, False, f"登录成功但未返回访问令牌: {data}")
                    return False
            else:
                self.log_test_result(test_name, False, f"登录失败，状态码: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"登录过程中发生异常: {e}")
            return False
    
    def test_login_with_wrong_password(self):
        """测试使用错误密码登录"""
        test_name = "使用错误密码登录"
        
        try:
            login_data = {
                "identifier": TEST_USER["username"],
                "password": "wrong_password_123"
            }
            
            response = self.session.post(
                LOGIN_URL,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 401:
                self.log_test_result(test_name, True, "使用错误密码登录，正确返回401状态码")
                return True
            else:
                self.log_test_result(test_name, False, f"使用错误密码登录，预期401状态码，实际: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"测试过程中发生异常: {e}")
            return False
    
    def test_login_with_nonexistent_user(self):
        """测试使用不存在的用户登录"""
        test_name = "使用不存在的用户登录"
        
        try:
            login_data = {
                "identifier": "nonexistent_user_12345",
                "password": TEST_USER["password"]
            }
            
            response = self.session.post(
                LOGIN_URL,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 401:
                self.log_test_result(test_name, True, "使用不存在的用户登录，正确返回401状态码")
                return True
            else:
                self.log_test_result(test_name, False, f"使用不存在的用户登录，预期401状态码，实际: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"测试过程中发生异常: {e}")
            return False
    
    def test_get_current_user(self):
        """测试获取当前用户信息"""
        test_name = "获取当前用户信息"
        
        if not self.access_token:
            self.log_test_result(test_name, False, "未登录，无法获取用户信息")
            return False
        
        try:
            response = self.session.get(
                CURRENT_USER_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.access_token}"
                }
            )
            
            if response.status_code == 200:
                user_data = response.json()
                if user_data.get("username") == TEST_USER["username"]:
                    self.log_test_result(test_name, True, f"获取用户信息成功: {user_data.get('username')}")
                    return True
                else:
                    self.log_test_result(test_name, False, f"获取的用户信息不匹配: {user_data}")
                    return False
            else:
                self.log_test_result(test_name, False, f"获取用户信息失败，状态码: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"测试过程中发生异常: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("=== 开始端到端登录功能测试 ===")
        logger.info(f"API基础URL: {API_BASE_URL}")
        logger.info(f"测试用户: {TEST_USER['username']}")
        
        # 运行所有测试
        self.test_login_with_username()
        self.test_get_current_user()  # 测试获取用户信息（需要先登录）
        
        # 清除会话，测试其他登录方式
        self.session = requests.Session()
        self.access_token = None
        
        self.test_login_with_email()
        self.test_login_with_phone()
        self.test_login_with_wrong_password()
        self.test_login_with_nonexistent_user()
        
        # 打印测试结果摘要
        self.print_test_summary()
    
    def print_test_summary(self):
        """打印测试结果摘要"""
        logger.info("\n=== 端到端登录测试结果摘要 ===")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"总测试数: {total_tests}")
        logger.info(f"通过测试: {passed_tests}")
        logger.info(f"失败测试: {failed_tests}")
        logger.info(f"成功率: {passed_tests / total_tests * 100:.1f}%")
        
        if failed_tests > 0:
            logger.info("\n失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    logger.info(f"  - {result['test_name']}: {result['message']}")
        
        logger.info("\n=== 测试完成 ===")
        
        # 检查是否所有核心功能测试都通过
        core_tests = ["使用用户名登录", "使用邮箱登录", "使用手机号登录", "获取当前用户信息"]
        core_test_results = [r for r in self.test_results if r["test_name"] in core_tests]
        all_core_passed = all(r["success"] for r in core_test_results)
        
        if all_core_passed:
            logger.info("🎉 所有核心登录功能测试通过！登录系统已恢复正常工作。")
        else:
            logger.error("⚠️  部分核心登录功能测试失败，需要进一步修复。")

def main():
    """主函数"""
    tester = LoginE2ETester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
