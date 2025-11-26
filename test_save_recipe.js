// 测试脚本：直接调用后端API保存食谱
const fs = require('fs');
const path = require('path');

// 模拟食谱数据（根据前端生成的食谱格式）
const mockRecipe = {
  title: "番茄鸡蛋炒饭",
  description: "简单美味的家常炒饭",
  difficulty: "简单",
  cooking_time: "55",
  preparation_time: "15",
  servings: "2",
  instructions: [
    "将米饭打散备用",
    "鸡蛋打散后炒熟盛起",
    "热锅下油，爆香葱花",
    "加入番茄块炒至软烂",
    "放入米饭和炒好的鸡蛋翻炒均匀",
    "加入适量盐和生抽调味即可"
  ],
  ingredients: [
    "鸡蛋 2 个",
    "米饭 2 碗",
    "番茄 1 个",
    "葱 2 根",
    "盐 适量",
    "生抽 适量",
    "油 适量"
  ],
  nutritional_info: {
    calories: "350",
    protein: "12.5",
    carbs: "48.0",
    fat: "10.0",
    fiber: "2.5"
  },
  tags: ["家常菜", "快速"]
};

// 映射difficulty值到后端期望的枚举值
const mapDifficulty = (difficulty) => {
  const difficultyMap = {
    'easy': 'easy',
    'medium': 'medium',
    'hard': 'hard',
    '简单': 'easy',
    '中等': 'medium',
    '困难': 'hard'
  };
  return difficultyMap[difficulty.toLowerCase()] || 'medium';
};

// 转换食谱数据为后端期望的格式
const formattedRecipeData = {
  title: mockRecipe.title || '未命名食谱',
  description: mockRecipe.description || '',
  prep_time: parseInt(mockRecipe.preparation_time) || 0,
  cooking_time: parseInt(mockRecipe.cooking_time) || 0,
  servings: parseInt(mockRecipe.servings) || 1,
  difficulty: mapDifficulty(mockRecipe.difficulty), // 确保是easy/medium/hard
  ingredients: Array.isArray(mockRecipe.ingredients) ? 
    mockRecipe.ingredients.map((ingredient) => {
      // 简单拆分食材字符串为name, quantity, unit
      const match = ingredient.match(/^(.*?)\s+(\d*\.?\d+)\s+(.*)$/);
      if (match) {
        return {
          name: match[1].trim(),
          quantity: parseFloat(match[2]),
          unit: match[3].trim(),
          note: ''
        };
      } else {
        return {
          name: ingredient.trim(),
          quantity: 1,
          unit: '份',
          note: ''
        };
      }
    })
    : [],
  // 将instructions数组转换为字符串（用换行符连接），因为后端期望instructions是字符串格式
  instructions: Array.isArray(mockRecipe.instructions) ? mockRecipe.instructions.join('\n') : String(mockRecipe.instructions || ''),
  nutrition_info: {
    calories: parseInt(mockRecipe.nutritional_info?.calories) || 0,
    protein: parseFloat(mockRecipe.nutritional_info?.protein) || 0,
    carbs: parseFloat(mockRecipe.nutritional_info?.carbs) || 0,
    fat: parseFloat(mockRecipe.nutritional_info?.fat) || 0,
    fiber: parseFloat(mockRecipe.nutritional_info?.fiber) || 0
  },
  tips: mockRecipe.tips || [],
  tags: mockRecipe.tags || []
};

// 构建请求体（根据SaveRecipeRequest的结构）
const requestBody = {
  recipe_data: formattedRecipeData,
  share_with_community: false
};

// 验证请求体格式
console.log('\n=== 请求体格式验证 ===');
console.log('✓ recipe_data.title:', typeof requestBody.recipe_data.title === 'string');
console.log('✓ recipe_data.description:', typeof requestBody.recipe_data.description === 'string');
console.log('✓ recipe_data.difficulty:', ['easy', 'medium', 'hard'].includes(requestBody.recipe_data.difficulty));
console.log('✓ recipe_data.cooking_time:', typeof requestBody.recipe_data.cooking_time === 'number' && requestBody.recipe_data.cooking_time > 0);
console.log('✓ recipe_data.servings:', typeof requestBody.recipe_data.servings === 'number' && requestBody.recipe_data.servings > 0);
console.log('✓ recipe_data.instructions:', Array.isArray(requestBody.recipe_data.instructions));
console.log('✓ recipe_data.ingredients:', Array.isArray(requestBody.recipe_data.ingredients));
console.log('✓ recipe_data.nutrition_info:', typeof requestBody.recipe_data.nutrition_info === 'object');
console.log('✓ recipe_data.nutrition_info.calories:', typeof requestBody.recipe_data.nutrition_info.calories === 'number');
console.log('✓ recipe_data.nutrition_info.protein:', typeof requestBody.recipe_data.nutrition_info.protein === 'number');
console.log('✓ recipe_data.nutrition_info.carbs:', typeof requestBody.recipe_data.nutrition_info.carbs === 'number');
console.log('✓ recipe_data.nutrition_info.fat:', typeof requestBody.recipe_data.nutrition_info.fat === 'number');
console.log('✓ recipe_data.nutrition_info.fiber:', typeof requestBody.recipe_data.nutrition_info.fiber === 'number');
console.log('✓ share_with_community:', typeof requestBody.share_with_community === 'boolean');

console.log('准备保存的食谱数据:');
console.log(JSON.stringify(requestBody, null, 2));

// 保存请求体到文件，方便查看
fs.writeFileSync(path.join(__dirname, 'test_recipe_data.json'), JSON.stringify(requestBody, null, 2));
console.log('\n请求体已保存到 test_recipe_data.json 文件');

console.log('\n现在可以使用以下PowerShell命令测试API:');
console.log('$token = "YOUR_TOKEN"; $recipeData = Get-Content test_recipe_data.json -Raw; $saveResponse = Invoke-WebRequest -Uri http://localhost:8000/ai/save-generated-recipe -Method Post -Body $recipeData -ContentType "application/json" -Headers @{Authorization="Bearer $token"}; Write-Host "保存食谱响应状态码: $($saveResponse.StatusCode)"; Write-Host "保存食谱响应内容: $($saveResponse.Content)"');

// 也可以使用以下命令直接在PowerShell中测试登录和保存食谱
console.log('\n或者使用以下完整PowerShell脚本测试登录和保存食谱:');
console.log('$loginBody = ConvertTo-Json @{identifier="test_login_user2@example.com"; password="TestPassword123"};');
console.log('$loginResponse = Invoke-WebRequest -Uri http://localhost:8000/api/auth/login -Method Post -Body $loginBody -ContentType "application/json";');
console.log('$token = ($loginResponse.Content | ConvertFrom-Json).access_token;');
console.log('Write-Host "获取到令牌: $token";');
console.log('$recipeData = Get-Content test_recipe_data.json -Raw;');
console.log('$saveResponse = Invoke-WebRequest -Uri http://localhost:8000/ai/save-generated-recipe -Method Post -Body $recipeData -ContentType "application/json" -Headers @{Authorization="Bearer $token"};');
console.log('Write-Host "保存食谱响应状态码: $($saveResponse.StatusCode)";');
console.log('Write-Host "保存食谱响应内容: $($saveResponse.Content)";');
