param(
    [string]$BaseUrl = "http://127.0.0.1:8100",
    [string]$Username = "admin",
    [string]$Password = "123456",
    [int]$KbId = 1
)

$ErrorActionPreference = "Stop"

Write-Host "1) Login..."
$loginBody = @{ username = $Username; password = $Password } | ConvertTo-Json
$loginResp = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/auth/login" -Body $loginBody -ContentType "application/json"
$token = $loginResp.access_token
if (-not $token) { throw "login failed: empty token" }
$headers = @{ Authorization = "Bearer $token" }

Write-Host "2) Me..."
$me = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/auth/me" -Headers $headers
$me | ConvertTo-Json | Write-Host

Write-Host "3) Ask..."
$sessionId = "smoke-" + [guid]::NewGuid().ToString("N")
$askBody = @{ question = "回归测试问题"; kb_id = $KbId; session_id = $sessionId } | ConvertTo-Json
$ask = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/chat/ask" -Headers $headers -Body $askBody -ContentType "application/json"
$ask | ConvertTo-Json | Write-Host
if (-not $ask.trace_id) { throw "ask failed: missing trace_id" }

Write-Host "4) History..."
$history = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/chat/history?session_id=$sessionId" -Headers $headers
$history | ConvertTo-Json | Write-Host

Write-Host "5) Usage..."
$usage = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/usage/tokens/daily" -Headers $headers
$usage | ConvertTo-Json | Write-Host

Write-Host "Phase1 regression smoke passed."

