const axios = require('axios');

// 测试食谱生成API
async function testGenerateRecipe() {
    try {
        console.log('测试食谱生成API...');
        
        // 0. 先注册一个测试用户
        console.log('0. 尝试注册新用户...');
        const registerData = {
            username: 'testUser',
            email: 'test@example.com',
            password: 'password123'
        };
        
        try {
            const registerResponse = await axios.post('http://localhost:8001/auth/register', registerData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('用户注册成功！');
        } catch (registerError) {
            if (registerError.response && registerError.response.status === 400) {
                console.log('用户已存在，继续尝试登录...');
            } else {
                console.error('注册失败:', registerError.message);
                if (registerError.response) {
                    console.error('注册响应数据:', JSON.stringify(registerError.response.data, null, 2));
                }
                return;
            }
        }
        
        // 1. 登录获取访问令牌
        console.log('1. 尝试登录...');
        const loginData = {
            identifier: 'testUser',
            password: 'password123'
        };
        
        const loginResponse = await axios.post('http://localhost:8001/auth/login', loginData, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('登录成功！');
        console.log('访问令牌:', loginResponse.data.access_token);
        
        // 2. 使用访问令牌测试食谱生成API
        console.log('\n2. 测试食谱生成API...');
        
        // 准备测试数据
        const testData = {
            ingredients: ['番茄', '鸡蛋', '米饭'],
            restrictions: ['无'],
            preferences: {
                difficulty: 'easy',
                cooking_time: '30分钟'
            }
        };
        
        // 发送请求到后端API
        const response = await axios.post('http://localhost:8001/ai/generate-recipe', testData, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${loginResponse.data.access_token}`
            }
        });
        
        console.log('API响应状态:', response.status);
        console.log('API响应数据:', JSON.stringify(response.data, null, 2));
        
        // 检查返回的数据结构
        if (response.data.image_url) {
            console.log('✓ 食谱包含image_url字段:', response.data.image_url);
        } else {
            console.log('✗ 食谱缺少image_url字段');
        }
        
    } catch (error) {
        console.error('测试失败:', error.message);
        if (error.response) {
            console.error('响应数据:', JSON.stringify(error.response.data, null, 2));
            console.error('响应状态:', error.response.status);
        }
    }
}

// 运行测试
testGenerateRecipe();