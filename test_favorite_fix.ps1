# 测试收藏功能修复的脚本
$ErrorActionPreference = "Stop"

# 测试用户凭据
$loginData = @{
    "identifier" = "xuxiaochang@qq.com"
    "password" = "Xxc20001018"
}

# 登录获取token
Write-Host "正在登录..."
$loginResponse = Invoke-WebRequest -Uri http://localhost:8000/auth/login -Method Post -Body ($loginData | ConvertTo-Json) -ContentType "application/json"
$loginResult = $loginResponse.Content | ConvertFrom-Json
$token = $loginResult.access_token

Write-Host "登录成功，获取到令牌: $token"

# 设置请求头
$headers = @{}
$headers.Add("Authorization", "Bearer $token")
$headers.Add("Content-Type", "application/json")

# 选择一个存在的食谱ID进行测试（这里使用ID为1的食谱）
$recipeId = "1"

# 测试添加收藏
Write-Host "\n测试添加收藏..."
$addResponse = Invoke-WebRequest -Uri "http://localhost:8000/recipes/$recipeId/favorite" -Method Post -Headers $headers
Write-Host "添加收藏成功! 状态码: $($addResponse.StatusCode)"
Write-Host "响应内容: $($addResponse.Content)"

# 测试取消收藏
Write-Host "\n测试取消收藏..."
$removeResponse = Invoke-WebRequest -Uri "http://localhost:8000/recipes/$recipeId/favorite" -Method Delete -Headers $headers
Write-Host "取消收藏成功! 状态码: $($removeResponse.StatusCode)"

Write-Host "\n🎉 测试完成！收藏功能修复成功！"