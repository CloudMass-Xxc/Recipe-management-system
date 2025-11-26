# 测试登录和保存食谱的PowerShell脚本

# 登录信息
$loginBody = @{"identifier" = "xuxiaochang@qq.com"; "password" = "Xxc20001018.."} | ConvertTo-Json

# 登录获取令牌
Write-Host "正在登录..."
$loginResponse = Invoke-WebRequest -Uri http://localhost:8000/auth/login -Method Post -Body $loginBody -ContentType "application/json"
Write-Host "登录响应状态码: $($loginResponse.StatusCode)"

if ($loginResponse.StatusCode -eq 200) {
    $token = ($loginResponse.Content | ConvertFrom-Json).access_token
    Write-Host "获取到令牌: $token"
    
    # 读取测试数据
    $recipeData = Get-Content test_recipe_data.json -Raw
    
    # 测试保存食谱API
    Write-Host "\n正在测试保存食谱API..."
    $saveResponse = Invoke-WebRequest -Uri http://localhost:8000/ai/save-generated-recipe -Method Post -Body $recipeData -ContentType "application/json" -Headers @{Authorization="Bearer $token"}
    Write-Host "保存食谱响应状态码: $($saveResponse.StatusCode)"
    Write-Host "保存食谱响应内容: $($saveResponse.Content)"
} else {
    Write-Host "登录失败，无法继续测试保存食谱API"
}