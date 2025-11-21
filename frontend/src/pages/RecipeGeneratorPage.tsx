import React, { useState } from "react";
import { Button, Form, Input, Select, message } from "antd";
import api from "../services/api";
const { TextArea } = Input;
import type { RecipeGenerationRequest, RecipeResponse } from '../types/recipe';

const { Option } = Select;

interface Preferences {
  foodLikes: string;
  foodDislikes: string;
  dietaryPreferences: string[];
  healthConditions: string;
  nutritionGoals: string;
  cookingTimeLimit: string;
  difficulty: string;
  cuisine: string;
}

const RecipeGeneratorPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState<RecipeResponse | null>(null);

  // 映射中文难度到英文枚举值
  const difficultyMap: Record<string, string> = {
    '简单': 'easy',
    '中等': 'medium',
    '困难': 'hard'
  };

  // 映射中文字体到英文枚举值
  const cuisineMap: Record<string, string> = {
    '无': 'none',
    '中餐': 'chinese',
    '西餐': 'western',
    '日料': 'japanese',
    '韩餐': 'korean',
    '泰餐': 'thai',
    '印度餐': 'indian',
    '意大利餐': 'italian',
    '墨西哥餐': 'mexican',
    '中东餐': 'middle_eastern',
    '东南亚餐': 'south_east_asian',
    '其他': 'other'
  };

  // 映射中文饮食偏好到英文枚举值
  const dietaryPreferenceMap: Record<string, string> = {
    '素食': 'vegetarian',
    '纯素': 'vegan',
    '无麸质': 'gluten_free',
    '无乳糖': 'lactose_free',
    '低碳水': 'low_carb',
    '高蛋白': 'high_protein',
    '无坚果': 'nut_free',
    '无海鲜': 'seafood_free',
    '无红肉': 'red_meat_free',
    '无酒精': 'alcohol_free'
  };

  const handleGenerate = async (values: Preferences) => {
    console.log('开始生成食谱，表单值:', values);
    setLoading(true);
    setRecipe(null);

    try {
      // 准备请求数据
      const requestData: RecipeGenerationRequest = {
        food_likes: values.foodLikes ? values.foodLikes.split(',').map(item => item.trim()).filter(Boolean) : [],
        food_dislikes: values.foodDislikes ? values.foodDislikes.split(',').map(item => item.trim()).filter(Boolean) : [],
        // 转换饮食偏好为后端所需的格式
        dietary_preferences: values.dietaryPreferences.map(pref => 
          dietaryPreferenceMap[pref] || pref
        ),
        health_conditions: values.healthConditions ? values.healthConditions.split(',').map(item => item.trim()).filter(Boolean) : [],
        nutrition_goals: values.nutritionGoals ? values.nutritionGoals.split(',').map(item => item.trim()).filter(Boolean) : [],
        cooking_time_limit: values.cookingTimeLimit ? parseInt(values.cookingTimeLimit) : 0,
        difficulty: difficultyMap[values.difficulty] || 'any',
        cuisine: cuisineMap[values.cuisine] || 'none'
      };

      console.log('发送请求数据:', requestData);
      console.log('API基础URL:', api.defaults.baseURL);
      console.log('请求路径: /ai/generate-recipe');

      // 使用原生fetch API直接请求，避免axios拦截器可能的问题
      console.log('准备使用fetch API发送POST请求');
      const fetchResponse = await fetch('http://localhost:8000/ai/generate-recipe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // 添加token如果有的话
          ...(localStorage.getItem('token') ? {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          } : {})
        },
        body: JSON.stringify(requestData)
      });

      console.log('Fetch响应状态:', fetchResponse.status);
      
      if (!fetchResponse.ok) {
        // 尝试获取错误详情
        let errorMessage = `请求失败: ${fetchResponse.status} ${fetchResponse.statusText}`;
        try {
          const errorData = await fetchResponse.json();
          console.error('API错误详情:', errorData);
          errorMessage = `API错误: ${errorData.detail || errorData.message || errorMessage}`;
        } catch (jsonError) {
          console.error('无法解析错误响应:', jsonError);
        }
        throw new Error(errorMessage);
      }

      // 确保响应体不为空
      const responseText = await fetchResponse.text();
      console.log('原始响应文本:', responseText);
      
      if (!responseText.trim()) {
        console.error('响应体为空');
        throw new Error('API返回空响应');
      }
      
      let responseData;
      try {
        responseData = JSON.parse(responseText);
        console.log('解析后的响应数据:', responseData);
        console.log('响应数据类型:', typeof responseData);
      } catch (parseError) {
        console.error('JSON解析错误:', parseError);
        throw new Error('无法解析API响应为JSON格式');
      }
      
      // 更灵活的数据处理逻辑
      if (responseData && typeof responseData === 'object') {
        // 检查是否有嵌套的recipe或data字段
        const recipeData = responseData.recipe || responseData.data || responseData;
        console.log('使用的食谱数据:', recipeData);
        
        // 即使没有title，也尝试创建一个基本的食谱对象
        const formattedRecipe: RecipeResponse = {
          title: recipeData.title || recipeData.name || '未知食谱',
          description: recipeData.description || recipeData.summary || '',
          // 处理各种可能的食材格式
          ingredients: Array.isArray(recipeData.ingredients) 
            ? recipeData.ingredients.map((ing: any) => 
                typeof ing === 'object' 
                  ? `${ing.name || ing.ingredient || ''} ${ing.quantity || ''} ${ing.unit || ''}`.trim() 
                  : String(ing)
              ).filter(Boolean)
            : [recipeData.ingredients || ''],
          // 处理各种可能的步骤格式
          instructions: Array.isArray(recipeData.instructions) 
            ? recipeData.instructions 
            : Array.isArray(recipeData.steps) 
              ? recipeData.steps 
              : recipeData.instructions || recipeData.steps 
                ? [recipeData.instructions || recipeData.steps]
                : [],
          cooking_time: recipeData.cooking_time || recipeData.cook_time || recipeData.time || 0,
          preparation_time: recipeData.preparation_time || recipeData.prep_time || 0,
          difficulty: recipeData.difficulty || 'unknown',
          nutritional_info: recipeData.nutritional_info || recipeData.nutrition || recipeData.nutrition_info,
          tips: Array.isArray(recipeData.tips) ? recipeData.tips : [recipeData.tips || ''].filter(Boolean),
          servings: recipeData.servings || recipeData.yield || 1
        };
        
        console.log('格式化后的食谱数据:', formattedRecipe);
        
        // 验证食谱是否有足够的内容
        if (formattedRecipe.ingredients.length > 0 || formattedRecipe.instructions.length > 0) {
          setRecipe(formattedRecipe);
          message.success('食谱生成成功!');
        } else {
          console.error('食谱数据缺少关键内容:', formattedRecipe);
          message.warning('生成的食谱内容不完整');
          setRecipe(formattedRecipe); // 仍然显示已有的内容
        }
      } else {
        console.error('无效的响应数据结构，期望对象类型:', responseData);
        message.error('收到的数据格式错误');
        // 尝试使用原始数据作为最简单的食谱展示
        setRecipe({
          title: '生成的食谱',
          description: String(responseData),
          ingredients: [],
          instructions: [],
          cooking_time: 0,
          preparation_time: 0,
          difficulty: 'unknown',
          nutritional_info: undefined,
          tips: [],
          servings: 1
        });
      }
    } catch (error: any) {
      console.error('食谱生成失败:', error);
      // 增强错误处理，获取详细错误信息
      if (error.response) {
        console.error('错误响应数据:', error.response.data);
        message.error(`生成失败: ${error.response.data.detail || '参数验证失败'}`);
      } else if (error.request) {
        console.error('请求已发送但无响应:', error.request);
        message.error('网络错误，请检查连接');
      } else {
        message.error(`生成失败: ${error.message || '未知错误'}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyText = (difficulty: string): string => {
    const reverseMap: Record<string, string> = {};
    Object.entries(difficultyMap).forEach(([key, value]) => {
      reverseMap[value] = key;
    });
    return reverseMap[difficulty] || difficulty;
  };

  return (
    <div className="recipe-generator-container">
      <h1>生成个性化食谱</h1>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleGenerate}
        className="recipe-generator-form"
      >
        <Form.Item
          name="foodLikes"
          label="喜欢的食材或菜品"
          tooltip="请输入您喜欢的食材或菜品，多个用逗号分隔"
        >
          <TextArea
            placeholder="例如：鸡肉, 番茄, 米饭"
            autoSize={{ minRows: 2 }}
          />
        </Form.Item>

        <Form.Item
          name="foodDislikes"
          label="不喜欢的食材或菜品"
          tooltip="请输入您不喜欢的食材或菜品，多个用逗号分隔"
        >
          <TextArea
            placeholder="例如：洋葱, 香菜, 苦瓜"
            autoSize={{ minRows: 2 }}
          />
        </Form.Item>

        <Form.Item
          name="dietaryPreferences"
          label="饮食偏好"
          tooltip="请选择您的饮食偏好，可多选"
          initialValue={[]}
        >
          <Select
            mode="multiple"
            placeholder="请选择饮食偏好"
          >
            <Option value="素食">素食</Option>
            <Option value="纯素">纯素</Option>
            <Option value="无麸质">无麸质</Option>
            <Option value="无乳糖">无乳糖</Option>
            <Option value="低碳水">低碳水</Option>
            <Option value="高蛋白">高蛋白</Option>
            <Option value="无坚果">无坚果</Option>
            <Option value="无海鲜">无海鲜</Option>
            <Option value="无红肉">无红肉</Option>
            <Option value="无酒精">无酒精</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="healthConditions"
          label="健康状况"
          tooltip="请输入您的健康状况或特殊需求"
        >
          <TextArea
            placeholder="例如：高血压, 糖尿病, 减肥"
            autoSize={{ minRows: 1 }}
          />
        </Form.Item>

        <Form.Item
          name="nutritionGoals"
          label="营养目标"
          tooltip="请输入您的营养目标"
        >
          <TextArea
            placeholder="例如：增肌, 减重, 维持健康"
            autoSize={{ minRows: 1 }}
          />
        </Form.Item>

        <div className="form-row">
          <Form.Item
            name="cookingTimeLimit"
            label="烹饪时间限制(分钟)"
            className="form-item-half"
          >
            <Input
              placeholder="例如：30"
              addonAfter="分钟"
            />
          </Form.Item>

          <Form.Item
            name="difficulty"
            label="难度"
            className="form-item-half"
          >
            <Select placeholder="请选择难度">
              <Option value="简单">简单</Option>
              <Option value="中等">中等</Option>
              <Option value="困难">困难</Option>
            </Select>
          </Form.Item>
        </div>

        <Form.Item
          name="cuisine"
          label="菜系"
        >
          <Select placeholder="请选择菜系">
            <Option value="无">无</Option>
            <Option value="中餐">中餐</Option>
            <Option value="西餐">西餐</Option>
            <Option value="日料">日料</Option>
            <Option value="韩餐">韩餐</Option>
            <Option value="泰餐">泰餐</Option>
            <Option value="印度餐">印度餐</Option>
            <Option value="意大利餐">意大利餐</Option>
            <Option value="墨西哥餐">墨西哥餐</Option>
            <Option value="中东餐">中东餐</Option>
            <Option value="东南亚餐">东南亚餐</Option>
            <Option value="其他">其他</Option>
          </Select>
        </Form.Item>

        <Form.Item>
          <div style={{ display: 'flex', gap: '10px' }}>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              className="generate-button"
              style={{ flex: 1 }}
            >
              生成食谱
            </Button>
            <Button
              onClick={async () => {
                message.info('正在测试API连接...');
                try {
                  // 测试状态API
                  console.log('测试状态API: GET /ai/status');
                  const statusFetchResponse = await fetch('http://localhost:8000/ai/status');
                  console.log('状态API响应状态:', statusFetchResponse.status);
                  
                  if (statusFetchResponse.ok) {
                    const statusData = await statusFetchResponse.json();
                    console.log('状态API响应数据:', statusData);
                    message.success(`状态API测试成功: ${statusFetchResponse.status} ${statusData.status}`);
                  } else {
                    throw new Error(`状态API返回错误: ${statusFetchResponse.status}`);
                  }
                  
                  // 测试食谱生成API
                  const testRecipeData = {
                    food_likes: ['鸡肉', '米饭'],
                    food_dislikes: [],
                    dietary_preferences: [],
                    health_conditions: [],
                    nutrition_goals: [],
                    cooking_time_limit: 30,
                    difficulty: 'easy',
                    cuisine: 'chinese'
                  };
                  
                  console.log('测试食谱生成API: POST /ai/generate-recipe');
                  const recipeFetchResponse = await fetch('http://localhost:8000/ai/generate-recipe', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(testRecipeData)
                  });
                  
                  console.log('食谱生成API响应状态:', recipeFetchResponse.status);
                  
                  if (recipeFetchResponse.ok) {
                    const recipeData = await recipeFetchResponse.json();
                    console.log('食谱生成API响应数据:', recipeData);
                    message.success(`食谱生成API测试成功: ${recipeFetchResponse.status}`);
                    message.info(`生成的食谱标题: ${recipeData.title}`);
                  } else {
                    const errorData = await recipeFetchResponse.json().catch(() => ({}));
                    throw new Error(`食谱生成API错误: ${errorData.detail || recipeFetchResponse.status}`);
                  }
                } catch (error) {
                  console.error('API测试失败:', error);
                  message.error(`API测试失败: ${error instanceof Error ? error.message : String(error)}`);
                }
              }}
            >
              测试API
            </Button>
          </div>
        </Form.Item>
      </Form>

      {recipe && (
        <div className="recipe-result">
          <h2>{recipe.title}</h2>
          <div className="recipe-info">
            <span>难度：{getDifficultyText(recipe.difficulty)}</span>
            <span>烹饪时间：{recipe.cooking_time}分钟</span>
            <span>准备时间：{recipe.preparation_time}分钟</span>
          </div>
          
          <div className="recipe-section">
            <h3>食材</h3>
            <ul className="ingredients-list">
              {recipe.ingredients.map((ingredient: string, index: number) => (
                <li key={index}>{ingredient}</li>
              ))}
            </ul>
          </div>
          
          <div className="recipe-section">
            <h3>烹饪步骤</h3>
            <ol className="instructions-list">
              {recipe.instructions.map((instruction: string, index: number) => (
                <li key={index}>{instruction}</li>
              ))}
            </ol>
          </div>
          
          {recipe.nutritional_info && (
            <div className="recipe-section">
              <h3>营养信息</h3>
              <div className="nutrition-info">
                <div className="nutrition-item">
                  <span className="nutrition-label">卡路里:</span>
                  <span className="nutrition-value">{recipe.nutritional_info.calories}千卡</span>
                </div>
                <div className="nutrition-item">
                  <span className="nutrition-label">蛋白质:</span>
                  <span className="nutrition-value">{recipe.nutritional_info.protein}克</span>
                </div>
                <div className="nutrition-item">
                  <span className="nutrition-label">碳水化合物:</span>
                  <span className="nutrition-value">{recipe.nutritional_info.carbs}克</span>
                </div>
                <div className="nutrition-item">
                  <span className="nutrition-label">脂肪:</span>
                  <span className="nutrition-value">{recipe.nutritional_info.fat}克</span>
                </div>
              </div>
            </div>
          )}
          
          {recipe.tips && recipe.tips.length > 0 && (
            <div className="recipe-section">
              <h3>烹饪小贴士</h3>
              <ul className="tips-list">
                {recipe.tips.map((tip: string, index: number) => (
                    <li key={index}>{tip}</li>
                  ))}
              </ul>
            </div>
          )}
          
          <div className="save-recipe-section">
            <Button
              type="primary"
              onClick={async () => {
                try {
                  message.info('正在保存食谱...');
                  const response = await fetch('http://localhost:8000/ai/save-generated-recipe', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                      ...(localStorage.getItem('token') ? {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                      } : {})
                    },
                    body: JSON.stringify({
                      recipe_data: recipe
                    })
                  });
                  
                  if (!response.ok) {
                    throw new Error('保存失败');
                  }
                  
                  // 不需要使用response.json()的结果
                  message.success('食谱已添加到您的收藏！');
                } catch (error) {
                  console.error('保存食谱失败:', error);
                  message.error('保存失败，请重试');
                }
              }}
              style={{ marginTop: '20px', width: '100%' }}
            >
              添加到我的食谱
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecipeGeneratorPage;