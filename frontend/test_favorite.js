const axios = require('axios');

// 测试收藏功能的脚本
async function testFavorite() {
  try {
    // 使用之前测试成功的token
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTAwMDEiLCJ1c2VybmFtZSI6InRlc3R1c2VyX25ldzQ1NiIsImV4cCI6MTcxNDg2NjEyM30.D6eZ2Cj7I9B9eRzXZ1DcV2FgH5E7J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4';
    
    // 创建axios实例
    const api = axios.create({
      baseURL: 'http://localhost:8001',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    console.log('测试添加收藏...');
    const addResponse = await api.post('/recipes/1/favorite');
    console.log('添加收藏成功:', addResponse.status);
    
    console.log('测试取消收藏...');
    const removeResponse = await api.delete('/recipes/1/favorite');
    console.log('取消收藏成功:', removeResponse.status);
    
    console.log('测试完成！收藏功能正常工作。');
  } catch (error) {
    console.error('测试失败:', error.response?.status, error.response?.data);
  }
}

testFavorite();