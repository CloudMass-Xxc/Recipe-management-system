const axios = require('axios');

// 测试注册功能的错误处理
async function testRegister() {
  console.log('开始测试注册功能的错误处理...');
  
  try {
    // 测试1: 使用已存在的用户名
    console.log('\n测试1: 使用已存在的用户名');
    const response1 = await axios.post('http://localhost:8001/auth/register', {
      username: 'testuser',
      email: 'newemail@example.com',
      phone: '13100001111',
      password: 'Test@1234',
      display_name: 'Test User'
    });
    console.log('响应:', response1.data);
  } catch (error) {
    console.log('预期的错误:', error.response?.data);
    console.log('错误消息:', error.message);
  }
  
  try {
    // 测试2: 使用已存在的邮箱
    console.log('\n测试2: 使用已存在的邮箱');
    const response2 = await axios.post('http://localhost:8001/auth/register', {
      username: 'newuser123',
      email: 'test@example.com',
      phone: '13100002222',
      password: 'Test@1234',
      display_name: 'New User'
    });
    console.log('响应:', response2.data);
  } catch (error) {
    console.log('预期的错误:', error.response?.data);
    console.log('错误消息:', error.message);
  }
  
  try {
    // 测试3: 使用弱密码
    console.log('\n测试3: 使用弱密码');
    const response3 = await axios.post('http://localhost:8001/auth/register', {
      username: 'weakpassuser',
      email: 'weakpass@example.com',
      phone: '13100003333',
      password: 'weakpass',
      display_name: 'Weak Pass User'
    });
    console.log('响应:', response3.data);
  } catch (error) {
    console.log('预期的错误:', error.response?.data);
    console.log('错误消息:', error.message);
  }
}

testRegister().catch(console.error);
