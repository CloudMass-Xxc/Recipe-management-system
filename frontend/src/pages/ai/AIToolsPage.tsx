import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Container,
  Divider,
  Alert,
  Stack
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import RecipeGenerationForm from '../../components/ai/RecipeGenerationForm';
import RecipeEnhancementForm from '../../components/ai/RecipeEnhancementForm';
import RecipeGenerationResult from '../../components/ai/RecipeGenerationResult';
import RecipeEnhancementResult from '../../components/ai/RecipeEnhancementResult';
import NutritionAnalysisResult from '../../components/ai/NutritionAnalysisResult';
import AIServiceStatus from '../../components/ai/AIServiceStatus';
import { RecipeResponse } from '../../types/recipe';
import { NutritionAnalysisResponse } from '../../types/ai';

const AIToolsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [showGenerationResult, setShowGenerationResult] = useState(false);
  const [showEnhancementResult, setShowEnhancementResult] = useState(false);
  const [showNutritionResult, setShowNutritionResult] = useState(false);
  const [generatedRecipe, setGeneratedRecipe] = useState<RecipeResponse | null>(null);
  const [enhancedRecipe, setEnhancedRecipe] = useState<RecipeResponse | null>(null);
  const [originalRecipe, setOriginalRecipe] = useState<RecipeResponse | null>(null);
  const [nutritionAnalysis, setNutritionAnalysis] = useState<NutritionAnalysisResponse | null>(null);
  const [analyzedText, setAnalyzedText] = useState('');
  const [showServiceStatus, setShowServiceStatus] = useState(false);

  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
    // 切换标签时重置结果显示
    setShowGenerationResult(false);
    setShowEnhancementResult(false);
    setShowNutritionResult(false);
  };

  const handleRecipeGenerated = (recipe: RecipeResponse) => {
    setGeneratedRecipe(recipe);
    setShowGenerationResult(true);
  };

  const handleRecipeEnhanced = (original: RecipeResponse, enhanced: RecipeResponse) => {
    setOriginalRecipe(original);
    setEnhancedRecipe(enhanced);
    setShowEnhancementResult(true);
  };

  const handleNutritionAnalyzed = (analysis: NutritionAnalysisResponse, text: string) => {
    setNutritionAnalysis(analysis);
    setAnalyzedText(text);
    setShowNutritionResult(true);
  };

  const handleSaveSuccess = () => {
    // 保存成功后可以显示提示或导航到食谱列表
    alert('食谱保存成功！');
  };

  // 检查用户是否已登录，如果未登录则显示提示
  if (!isAuthenticated) {
    return (
      <Container maxWidth="md" sx={{ mt: 8, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <Alert severity="info" sx={{ mb: 4 }}>
            您需要先登录才能使用AI工具功能
          </Alert>
          <Typography variant="h6" gutterBottom>请登录后继续</Typography>
          <Button 
            variant="contained" 
            onClick={() => navigate('/login')}
          >
            前往登录
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
      <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" gutterBottom>AI食谱助手</Typography>
          <Button 
            variant="text" 
            onClick={() => setShowServiceStatus(!showServiceStatus)}
          >
            {showServiceStatus ? '隐藏服务状态' : '显示服务状态'}
          </Button>
        </Box>

        {showServiceStatus && (
          <Box sx={{ mb: 4, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
            <AIServiceStatus 
              autoRefresh={true} 
              refreshInterval={30000} 
              showDetailedInfo={true} 
            />
          </Box>
        )}

        {user && (
          <Alert severity="success" sx={{ mb: 4 }}>
            欢迎回来，{user.username}！使用下面的工具来创建、增强您的食谱或分析营养成分。
          </Alert>
        )}

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 4 }}>
          <Tabs 
            value={activeTab} 
            onChange={handleTabChange}
            variant="fullWidth"
            centered
          >
            <Tab label="生成新食谱" />
            <Tab label="增强现有食谱" />
            <Tab label="营养成分分析" />
          </Tabs>
        </Box>

        <Box sx={{ mt: 2 }}>
          {/* 生成新食谱标签页 */}
          {activeTab === 0 && (
            <div>
              {!showGenerationResult ? (
                <RecipeGenerationForm onRecipeGenerated={handleRecipeGenerated} />
              ) : (
                <RecipeGenerationResult 
                  recipe={generatedRecipe!}
                  onClose={() => {
                    setShowGenerationResult(false);
                    setGeneratedRecipe(null);
                  }}
                  onSaveSuccess={handleSaveSuccess}
                />
              )}
            </div>
          )}

          {/* 增强现有食谱标签页 */}
          {activeTab === 1 && (
            <div>
              {!showEnhancementResult ? (
                <RecipeEnhancementForm onRecipeEnhanced={handleRecipeEnhanced} />
              ) : (
                <RecipeEnhancementResult 
                  originalRecipe={originalRecipe!}
                  enhancedRecipe={enhancedRecipe!}
                  onClose={() => {
                    setShowEnhancementResult(false);
                    setOriginalRecipe(null);
                    setEnhancedRecipe(null);
                  }}
                  onSaveSuccess={handleSaveSuccess}
                />
              )}
            </div>
          )}

          {/* 营养成分分析标签页 */}
          {activeTab === 2 && (
            <div>
              {!showNutritionResult ? (
                <NutritionAnalysisForm onNutritionAnalyzed={handleNutritionAnalyzed} />
              ) : (
                <NutritionAnalysisResult 
                  analysis={nutritionAnalysis!}
                  analyzedText={analyzedText}
                  onClose={() => {
                    setShowNutritionResult(false);
                    setNutritionAnalysis(null);
                    setAnalyzedText('');
                  }}
                />
              )}
            </div>
          )}
        </Box>
      </Paper>

      <Paper elevation={2} sx={{ p: 4 }}>
        <Typography variant="h6" gutterBottom>AI工具使用提示</Typography>
        <Stack spacing={2}>
          <Typography variant="body2">
            • 生成新食谱时，请尽可能详细地描述您的口味偏好、饮食限制和可用食材，以获得更精准的结果。
          </Typography>
          <Typography variant="body2">
            • 增强现有食谱时，您可以指定想要改进的方向，如减少热量、增加蛋白质或调整口味。
          </Typography>
          <Typography variant="body2">
            • 营养分析功能可以分析食材列表或完整食谱的营养成分，帮助您了解饮食的健康状况。
          </Typography>
          <Typography variant="body2">
            • AI生成的食谱仅供参考，请根据实际情况调整食材用量和烹饪步骤。
          </Typography>
        </Stack>
      </Paper>
    </Container>
  );
};

// 营养分析表单组件
interface NutritionAnalysisFormProps {
  onNutritionAnalyzed: (analysis: NutritionAnalysisResponse, text: string) => void;
}

const NutritionAnalysisForm: React.FC<NutritionAnalysisFormProps> = ({ onNutritionAnalyzed }) => {
  const [inputText, setInputText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!inputText.trim()) {
      setError('请输入食材列表或食谱内容');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await aiService.analyzeIngredientsNutrition(inputText);
      onNutritionAnalyzed(response, inputText);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        '营养分析失败，请稍后重试'
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Paper elevation={0} sx={{ p: 3, bgcolor: 'grey.50', mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom>营养分析说明</Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          输入食材列表或完整食谱文本，我们的AI将为您分析其营养成分、健康益处和饮食建议。
        </Typography>
        <Typography variant="body2" color="text.secondary">
          示例1（食材列表）：200克鸡胸肉，100克西兰花，50克糙米，1个鸡蛋，2勺橄榄油
        </Typography>
        <Typography variant="body2" color="text.secondary">
          示例2（简单食谱）：番茄炒蛋：2个鸡蛋打散，2个番茄切块，热锅下油，倒入蛋液炒熟盛起，再下番茄炒软，加入鸡蛋翻炒均匀，加盐调味即可。
        </Typography>
      </Paper>

      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom>输入食材列表或食谱内容</Typography>
        <TextField
          fullWidth
          multiline
          rows={6}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="请输入食材列表或完整食谱文本..."
          variant="outlined"
          disabled={isAnalyzing}
        />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Button
        type="submit"
        variant="contained"
        fullWidth
        size="large"
        disabled={isAnalyzing || !inputText.trim()}
        sx={{ py: 1.5 }}
      >
        {isAnalyzing ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <CircularProgress size={16} />
            <span>分析中...</span>
          </Box>
        ) : (
          '开始分析营养成分'
        )}
      </Button>
    </form>
  );
};

// 需要导入的额外组件
import { TextField, Button, CircularProgress } from '@mui/material';
import aiService from '../../services/aiService';

export default AIToolsPage;