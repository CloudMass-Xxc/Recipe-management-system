import React from 'react';
import { Paper, Typography, Box, FormControl, InputLabel, Select, MenuItem, Slider, FormGroup, FormControlLabel, Checkbox } from '@mui/material';

export interface Preferences {
  cooking_time?: string;
  difficulty?: string;
  flavor?: string;
  spiciness?: number;
  healthy?: boolean;
  quick_prep?: boolean;
  family_friendly?: boolean;
  budget_friendly?: boolean;
}

interface PreferenceSettingsProps {
  preferences: Preferences;
  onPreferenceChange: (preferences: Preferences) => void;
}

const PreferenceSettings: React.FC<PreferenceSettingsProps> = ({ 
  preferences, 
  onPreferenceChange 
}) => {
  const handleChange = (field: keyof Preferences, value: any) => {
    onPreferenceChange({
      ...preferences,
      [field]: value
    });
  };

  const cookingTimeOptions = [
    { label: '快速（30分钟以内）', value: 'quick' },
    { label: '中等（30-60分钟）', value: 'medium' },
    { label: '充足（60分钟以上）', value: 'long' }
  ];

  const difficultyOptions = [
    { label: '简单', value: 'easy' },
    { label: '中等', value: 'medium' },
    { label: '困难', value: 'hard' }
  ];

  const flavorOptions = [
    { label: '清淡', value: 'light' },
    { label: '适中', value: 'moderate' },
    { label: '浓郁', value: 'strong' }
  ];

  return (
    <Paper sx={{ p: 3, borderRadius: 2, backgroundColor: '#fafafa', mt: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
        3. 个人口味偏好
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        调整您的口味偏好，获取更符合您喜好的食谱
      </Typography>
      
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 4 }}>
        {/* 烹饪时间偏好 */}
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="cooking-time-label">烹饪时间偏好</InputLabel>
          <Select
            labelId="cooking-time-label"
            id="cooking-time"
            value={preferences.cooking_time || ''}
            label="烹饪时间偏好"
            onChange={(e) => handleChange('cooking_time', e.target.value)}
          >
            {cookingTimeOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* 难度偏好 */}
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="difficulty-label">难度偏好</InputLabel>
          <Select
            labelId="difficulty-label"
            id="difficulty"
            value={preferences.difficulty || ''}
            label="难度偏好"
            onChange={(e) => handleChange('difficulty', e.target.value)}
          >
            {difficultyOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* 口味偏好 */}
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="flavor-label">口味偏好</InputLabel>
          <Select
            labelId="flavor-label"
            id="flavor"
            value={preferences.flavor || ''}
            label="口味偏好"
            onChange={(e) => handleChange('flavor', e.target.value)}
          >
            {flavorOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* 辣度偏好 */}
        <Box sx={{ mb: 2 }}>
          <Typography id="spiciness-slider" gutterBottom sx={{ fontSize: '0.9rem', color: '#666' }}>
            辣度偏好
          </Typography>
          <Slider
            aria-labelledby="spiciness-slider"
            value={preferences.spiciness || 0}
            onChange={(_, value) => handleChange('spiciness', value)}
            valueLabelDisplay="auto"
            step={1}
            marks
            min={0}
            max={5}
            valueLabelFormat={(value) => {
              const labels = ['不辣', '微辣', '中辣', '特辣', '爆辣', '变态辣'];
              return labels[value as number];
            }}
            sx={{
              color: '#ff7043',
              '& .MuiSlider-thumb': {
                '&:hover, &.Mui-focusVisible': {
                  boxShadow: '0px 0px 0px 8px rgba(255, 112, 67, 0.16)',
                },
              },
            }}
          />
        </Box>
      </Box>

      {/* 特殊要求 */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="subtitle2" sx={{ mb: 2, color: '#666' }}>
          特殊要求：
        </Typography>
        <FormGroup sx={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', gap: 2 }}>
          <FormControlLabel
            control={
              <Checkbox
                checked={preferences.healthy || false}
                onChange={(e) => handleChange('healthy', e.target.checked)}
              />
            }
            label="健康饮食"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={preferences.quick_prep || false}
                onChange={(e) => handleChange('quick_prep', e.target.checked)}
              />
            }
            label="快速准备"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={preferences.family_friendly || false}
                onChange={(e) => handleChange('family_friendly', e.target.checked)}
              />
            }
            label="适合家庭"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={preferences.budget_friendly || false}
                onChange={(e) => handleChange('budget_friendly', e.target.checked)}
              />
            }
            label="经济实惠"
          />
        </FormGroup>
      </Box>
    </Paper>
  );
};

export default PreferenceSettings;
