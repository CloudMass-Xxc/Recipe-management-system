import React, { useState } from 'react';
import { Box, TextField, Chip, Button, Typography, Paper } from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';

interface IngredientInputProps {
  ingredients: string[];
  onAddIngredient: (ingredient: string) => void;
  onRemoveIngredient: (index: number) => void;
}

const IngredientInput: React.FC<IngredientInputProps> = ({ 
  ingredients, 
  onAddIngredient, 
  onRemoveIngredient 
}) => {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');

  const commonIngredients = ['鸡肉', '牛肉', '土豆', '胡萝卜', '西红柿', '鸡蛋', '米饭', '面条'];

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      handleAddIngredient();
    }
  };

  const handleAddIngredient = () => {
    const trimmedValue = inputValue.trim();
    if (!trimmedValue) {
      setError('请输入食材名称');
      return;
    }
    if (ingredients.includes(trimmedValue)) {
      setError('该食材已添加');
      return;
    }
    setError('');
    onAddIngredient(trimmedValue);
    setInputValue('');
  };

  const handleCommonIngredientClick = (ingredient: string) => {
    if (!ingredients.includes(ingredient)) {
      onAddIngredient(ingredient);
    }
  };

  return (
    <Paper sx={{ p: 3, borderRadius: 2, backgroundColor: '#fafafa' }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: '#333' }}>
        1. 添加您现有的食材
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        输入食材名称，或点击下方常用食材快速添加
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="输入食材，按回车添加"
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setError('');
          }}
          onKeyPress={handleKeyPress}
          error={!!error}
          helperText={error}
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 2,
            },
          }}
        />
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddIngredient}
          sx={{
            backgroundColor: '#4caf50',
            '&:hover': {
              backgroundColor: '#388e3c',
            },
            borderRadius: 2,
          }}
        >
          添加
        </Button>
      </Box>

      <Typography variant="subtitle2" sx={{ mb: 1, color: '#666' }}>
        常用食材：
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
        {commonIngredients.map((ingredient) => (
          <Chip
            key={ingredient}
            label={ingredient}
            onClick={() => handleCommonIngredientClick(ingredient)}
            variant={ingredients.includes(ingredient) ? 'filled' : 'outlined'}
            sx={{
              backgroundColor: ingredients.includes(ingredient) ? '#e8f5e8' : 'transparent',
              color: ingredients.includes(ingredient) ? '#388e3c' : 'inherit',
              '&:hover': {
                backgroundColor: ingredients.includes(ingredient) ? '#dcedc8' : '#f0f0f0',
              },
              cursor: 'pointer',
            }}
          />
        ))}
      </Box>

      {ingredients.length > 0 && (
        <>
          <Typography variant="subtitle2" sx={{ mb: 1, color: '#666' }}>
            已添加的食材：
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {ingredients.map((ingredient, index) => (
              <Chip
                key={index}
                label={ingredient}
                onDelete={() => onRemoveIngredient(index)}
                deleteIcon={<DeleteIcon fontSize="small" />}
                sx={{
                  backgroundColor: '#e3f2fd',
                  color: '#1976d2',
                  '& .MuiChip-deleteIcon': {
                    color: '#1565c0',
                    '&:hover': {
                      color: '#0d47a1',
                    },
                  },
                }}
              />
            ))}
          </Box>
        </>
      )}
    </Paper>
  );
};

export default IngredientInput;
