import React from 'react';
import { Paper, Typography, FormGroup, FormControlLabel, Checkbox, Box } from '@mui/material';

interface RestrictionSelectorProps {
  restrictions: string[];
  onRestrictionChange: (restrictions: string[]) => void;
}

const RestrictionSelector: React.FC<RestrictionSelectorProps> = ({ 
  restrictions, 
  onRestrictionChange 
}) => {
  const availableRestrictions = [
    { label: '素食', value: 'vegetarian' },
    { label: '纯素食', value: 'vegan' },
    { label: '无麸质', value: 'gluten-free' },
    { label: '无乳糖', value: 'dairy-free' },
    { label: '无坚果', value: 'nut-free' },
    { label: '无海鲜', value: 'seafood-free' },
    { label: '低卡路里', value: 'low-calorie' },
    { label: '低碳水', value: 'low-carb' },
    { label: '低糖', value: 'low-sugar' },
    { label: '低盐', value: 'low-sodium' },
  ];

  const handleRestrictionChange = (value: string) => {
    let newRestrictions: string[];
    if (restrictions.includes(value)) {
      newRestrictions = restrictions.filter(r => r !== value);
    } else {
      newRestrictions = [...restrictions, value];
    }
    onRestrictionChange(newRestrictions);
  };

  return (
    <Paper sx={{ p: 3, borderRadius: 2, backgroundColor: '#fafafa', mt: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
        2. 设置饮食禁忌
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        选择您需要避免的食材或饮食类型
      </Typography>
      
      <FormGroup>
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2 }}>
          {availableRestrictions.map((restriction) => (
            <FormControlLabel
              key={restriction.value}
              control={
                <Checkbox
                  checked={restrictions.includes(restriction.value)}
                  onChange={() => handleRestrictionChange(restriction.value)}
                  sx={{
                    '& .MuiCheckbox-root': {
                      color: '#4caf50',
                      '&.Mui-checked': {
                        color: '#388e3c',
                      },
                    },
                  }}
                />
              }
              label={restriction.label}
              sx={{
                '& .MuiFormControlLabel-label': {
                  fontSize: '0.9rem',
                },
              }}
            />
          ))}
        </Box>
      </FormGroup>
    </Paper>
  );
};

export default RestrictionSelector;
