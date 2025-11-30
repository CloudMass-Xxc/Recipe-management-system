import requests
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API配置
BASE_URL = "http://localhost:8001"
GENERATE_RECIPE_URL = f"{BASE_URL}/ai/generate-recipe"

# 测试数据
recipe_request = {
    "ingredients": ["米饭", "鸡蛋", "番茄"],
    "restrictions": [],
    "preferences": {
        "cooking_time": "20分钟",
        "difficulty": "简单",
        "flavor": "酸甜"
    }
}

def test_generate_recipe_with_image():
    """测试生成带图片的食谱"""
    logger.info("\n=== 测试生成带图片的食谱 ===")
    
    try:
        # 发送请求
        logger.info(f"发送请求到: {GENERATE_RECIPE_URL}")
        logger.info(f"请求体: {json.dumps(recipe_request, ensure_ascii=False)}")
        
        response = requests.post(
            GENERATE_RECIPE_URL,
            headers={"Content-Type": "application/json"},
            json=recipe_request
        )
        
        # 检查响应状态码
        logger.info(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 解析响应
            recipe_data = response.json()
            logger.info("\n=== 食谱生成结果 ===")
            logger.info(f"标题: {recipe_data.get('title')}")
            logger.info(f"描述: {recipe_data.get('description')}")
            logger.info(f"是否包含图片URL: {'image_url' in recipe_data}")
            
            if 'image_url' in recipe_data:
                logger.info(f"图片URL: {recipe_data.get('image_url')}")
                logger.info("✅ 测试通过！生成的食谱包含图片URL")
            else:
                logger.error("❌ 测试失败！生成的食谱没有包含图片URL")
        else:
            logger.error(f"❌ API调用失败: {response.status_code} - {response.text}")
    
    except Exception as e:
        logger.error(f"❌ 测试执行失败: {str(e)}")

if __name__ == "__main__":
    logger.info("开始测试食谱生成功能")
    test_generate_recipe_with_image()
    logger.info("测试完成")
