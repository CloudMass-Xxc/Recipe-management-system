import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Divider,
  Chip,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  IconButton,
  Collapse
} from '@mui/material';
import { Save, Share, Info, ArrowBack, Download } from '@mui/icons-material';
import { NutritionAnalysisResponse, DietaryRecommendation } from '../../types/ai';

interface NutritionAnalysisResultProps {
  analysis: NutritionAnalysisResponse;
  analyzedText: string; // 被分析的食材列表或食谱文本
  onClose: () => void;
}

const NutritionAnalysisResult: React.FC<NutritionAnalysisResultProps> = ({ 
  analysis, 
  analyzedText,
  onClose 
}) => {
  const [showDetailedAnalysis, setShowDetailedAnalysis] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);

  const handleExportAnalysis = async () => {
    setIsExporting(true);
    try {
      // 这里可以实现导出功能，例如导出为PDF或CSV
      // 目前只是模拟导出操作
      await new Promise(resolve => setTimeout(resolve, 1000));
      setExportSuccess(true);
      setTimeout(() => setExportSuccess(false), 3000);
    } catch (error) {
      alert('导出失败，请稍后重试');
    } finally {
      setIsExporting(false);
    }
  };

  const getNutritionRating = (value: number): { label: string; color: string } => {
    if (value >= 8) return { label: '优秀', color: 'success.main' };
    if (value >= 6) return { label: '良好', color: 'info.main' };
    if (value >= 4) return { label: '一般', color: 'warning.main' };
    return { label: '需改进', color: 'error.main' };
  };

  const renderNutritionBar = (value: number, maxValue: number, label: string) => {
    const percentage = Math.min((value / maxValue) * 100, 100);
    
    return (
      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="body2" color="text.secondary">{label}</Typography>
          <Typography variant="body2" fontWeight="bold">{value.toFixed(1)}</Typography>
        </Box>
        <Box sx={{ bgcolor: 'grey.200', borderRadius: 1, overflow: 'hidden' }}>
          <Box 
            sx={{ 
              bgcolor: percentage > 100 ? 'error.main' : 
                      percentage > 80 ? 'warning.main' : 'success.main',
              width: `${percentage}%`,
              height: 8,
              borderRadius: 1
            }}
          />
        </Box>
      </Box>
    );
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton onClick={onClose}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" gutterBottom>营养分析报告</Typography>
        </Box>
        <Button 
          variant="outlined" 
          startIcon={<Download />}
          onClick={handleExportAnalysis}
          disabled={isExporting}
        >
          {isExporting ? <CircularProgress size={16} /> : '导出报告'}
        </Button>
      </Box>

      {exportSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          报告导出成功！
        </Alert>
      )}

      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          分析内容:
        </Typography>
        <Paper elevation={0} sx={{ p: 2, bgcolor: 'grey.50' }}>
          <Typography variant="body2" fontFamily="monospace">
            {analyzedText}
          </Typography>
        </Paper>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card elevation={2} sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>营养评分</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box 
                  sx={{ 
                    width: 80, 
                    height: 80, 
                    borderRadius: '50%', 
                    bgcolor: getNutritionRating(analysis.overall_score).color, 
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <Typography variant="h4" color="white" fontWeight="bold">
                    {analysis.overall_score}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h6" 
                    sx={{ color: getNutritionRating(analysis.overall_score).color }}
                  >
                    {getNutritionRating(analysis.overall_score).label}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    满分10分，基于营养均衡性、热量分布和健康指标
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>

          <Card elevation={2} sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="subtitle1">主要营养成分</Typography>
                <IconButton onClick={() => setShowDetailedAnalysis(!showDetailedAnalysis)}>
                  <Info fontSize="small" />
                </IconButton>
              </Box>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Box sx={{ textAlign: 'center', p: 1 }}>
                    <Typography variant="h5" color="primary.main">{analysis.macros.calories}</Typography>
                    <Typography variant="body2" color="text.secondary">卡路里</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box sx={{ textAlign: 'center', p: 1 }}>
                    <Typography variant="h5" color="primary.main">{analysis.macros.protein}g</Typography>
                    <Typography variant="body2" color="text.secondary">蛋白质</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box sx={{ textAlign: 'center', p: 1 }}>
                    <Typography variant="h5" color="primary.main">{analysis.macros.carbs}g</Typography>
                    <Typography variant="body2" color="text.secondary">碳水化合物</Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box sx={{ textAlign: 'center', p: 1 }}>
                    <Typography variant="h5" color="primary.main">{analysis.macros.fat}g</Typography>
                    <Typography variant="body2" color="text.secondary">脂肪</Typography>
                  </Box>
                </Grid>
              </Grid>
              
              <Collapse in={showDetailedAnalysis}>
                <Divider sx={{ my: 2 }} />
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    详细营养数据
                  </Typography>
                  {renderNutritionBar(analysis.macros.fiber, 30, `膳食纤维: ${analysis.macros.fiber}g`)}
                  {analysis.macros.sugar !== undefined && 
                    renderNutritionBar(analysis.macros.sugar, 50, `糖分: ${analysis.macros.sugar}g`)}
                  {analysis.macros.sodium !== undefined && 
                    renderNutritionBar(analysis.macros.sodium, 2300, `钠: ${analysis.macros.sodium}mg`)}
                  {analysis.macros.cholesterol !== undefined && 
                    renderNutritionBar(analysis.macros.cholesterol, 300, `胆固醇: ${analysis.macros.cholesterol}mg`)}
                  {analysis.micros.calcium !== undefined && 
                    renderNutritionBar(analysis.micros.calcium, 1000, `钙: ${analysis.micros.calcium}mg`)}
                  {analysis.micros.iron !== undefined && 
                    renderNutritionBar(analysis.micros.iron, 18, `铁: ${analysis.micros.iron}mg`)}
                  {analysis.micros.vitamin_c !== undefined && 
                    renderNutritionBar(analysis.micros.vitamin_c, 90, `维生素C: ${analysis.micros.vitamin_c}mg`)}
                  {analysis.micros.vitamin_a !== undefined && 
                    renderNutritionBar(analysis.micros.vitamin_a, 900, `维生素A: ${analysis.micros.vitamin_a}μg`)}
                </Box>
              </Collapse>
            </CardContent>
          </Card>

          {analysis.health_benefits && analysis.health_benefits.length > 0 && (
            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>健康益处</Typography>
                <ul>
                  {analysis.health_benefits.map((benefit, index) => (
                    <li key={index} style={{ marginBottom: '8px' }}>
                      <Typography variant="body2">• {benefit}</Typography>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </Grid>

        <Grid item xs={12} md={6}>
          {analysis.dietary_recommendations && analysis.dietary_recommendations.length > 0 && (
            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>饮食建议</Typography>
                {analysis.dietary_recommendations.map((rec: DietaryRecommendation, index) => (
                  <Box key={index} sx={{ mb: 2, p: 1.5, bgcolor: rec.type === 'improvement' ? 'error.light' : 'success.light', borderRadius: 1 }}>
                    <Typography variant="body2" fontWeight="bold" sx={{ mb: 1 }}>
                      {rec.type === 'improvement' ? '改进建议' : '保持建议'}:
                    </Typography>
                    <Typography variant="body2">{rec.description}</Typography>
                    {rec.specifics && (
                      <ul style={{ marginTop: '4px', paddingLeft: '20px' }}>
                        {rec.specifics.map((specific, specIndex) => (
                          <li key={specIndex}>
                            <Typography variant="caption">• {specific}</Typography>
                          </li>
                        ))}
                      </ul>
                    )}
                  </Box>
                ))}
              </CardContent>
            </Card>
          )}

          {analysis.nutrient_imbalances && analysis.nutrient_imbalances.length > 0 && (
            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>营养失衡提示</Typography>
                <ul>
                  {analysis.nutrient_imbalances.map((imbalance, index) => (
                    <li key={index} style={{ marginBottom: '8px' }}>
                      <Typography variant="body2" color="error.main">
                        • {imbalance}
                      </Typography>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {analysis.suitable_diets && analysis.suitable_diets.length > 0 && (
            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>适合的饮食类型</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysis.suitable_diets.map((diet, index) => (
                    <Chip key={index} label={diet} color="success" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {analysis.unsuitable_diets && analysis.unsuitable_diets.length > 0 && (
            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>不适合的饮食类型</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysis.unsuitable_diets.map((diet, index) => (
                    <Chip key={index} label={diet} color="error" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}

          {analysis.substitute_suggestions && Object.keys(analysis.substitute_suggestions).length > 0 && (
            <Card elevation={2}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>食材替代建议</Typography>
                {Object.entries(analysis.substitute_suggestions).map(([ingredient, substitutes], index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Typography variant="body2" fontWeight="bold">
                      {ingredient} → 可替代为:
                    </Typography>
                    <Typography variant="body2">
                      {substitutes.join('、')}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Paper>
  );
};

export default NutritionAnalysisResult;