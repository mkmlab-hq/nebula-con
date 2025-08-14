# NebulaCon 개발 도구 PowerShell 스크립트
# 사용법: .\dev.ps1 <target>

param(
    [Parameter(Position=0)]
    [string]$Target = "help"
)

function Show-Help {
    Write-Host "NebulaCon 개발 도구" -ForegroundColor Green
    Write-Host ""
    Write-Host "사용 가능한 타겟:" -ForegroundColor Yellow
    Write-Host "  install    - 개발 모드로 패키지 설치"
    Write-Host "  test       - 테스트 실행"
    Write-Host "  lint       - 코드 품질 검사 (ruff)"
    Write-Host "  clean      - 빌드 파일 및 캐시 정리"
    Write-Host "  axes       - axes 메트릭 계산 예시"
    Write-Host "  retention  - retention 메트릭 계산 예시"
    Write-Host "  full       - 전체 메트릭 계산 예시"
    Write-Host "  docs       - 문서 생성"
    Write-Host "  build      - 배포용 패키지 빌드"
    Write-Host "  verify     - 전체 검증 (test + lint + axes)"
}

function Install-Package {
    Write-Host "🔧 개발 모드로 패키지 설치 중..." -ForegroundColor Blue
    pip install -e .
    Write-Host "✅ 설치 완료!" -ForegroundColor Green
}

function Invoke-Tests {
    Write-Host "🧪 테스트 실행 중..." -ForegroundColor Blue
    pytest -v
    Write-Host "✅ 테스트 완료!" -ForegroundColor Green
}

function Invoke-Lint {
    Write-Host "🔍 코드 품질 검사 중..." -ForegroundColor Blue
    ruff check src/ tests/
    Write-Host "✅ 린트 검사 완료!" -ForegroundColor Green
}

function Clear-BuildFiles {
    Write-Host "🧹 정리 중..." -ForegroundColor Blue
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    if (Test-Path "*.egg-info") { Remove-Item -Recurse -Force "*.egg-info" }
    if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }
    if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }
    Get-ChildItem -Path "src" -Recurse -Directory -Name "__pycache__" | ForEach-Object { Remove-Item -Recurse -Force "src\$_" }
    Get-ChildItem -Path "tests" -Recurse -Directory -Name "__pycache__" | ForEach-Object { Remove-Item -Recurse -Force "tests\$_" }
    Write-Host "✅ 정리 완료!" -ForegroundColor Green
}

function Invoke-Axes {
    Write-Host "📊 Axes 메트릭 계산 예시..." -ForegroundColor Blue
    nebula-axes-run --input data/raw/sample.csv --out metrics/axes_run.json
    Write-Host "✅ Axes 메트릭 계산 완료!" -ForegroundColor Green
}

function Invoke-Retention {
    Write-Host "📈 Retention 메트릭 계산 예시..." -ForegroundColor Blue
    if (Test-Path "data/raw/sample_shifted.csv") {
        nebula-retention-run --base data/raw/sample.csv --shifted data/raw/sample_shifted.csv --out metrics/retention_run.json
    } else {
        Write-Host "⚠️  sample_shifted.csv 파일이 없습니다. 기본 데이터로 테스트합니다." -ForegroundColor Yellow
        Copy-Item "data/raw/sample.csv" "data/raw/sample_shifted.csv"
        nebula-retention-run --base data/raw/sample.csv --shifted data/raw/sample_shifted.csv --out metrics/retention_run.json
    }
    Write-Host "✅ Retention 메트릭 계산 완료!" -ForegroundColor Green
}

function Invoke-Full {
    Write-Host "🚀 전체 메트릭 계산 예시..." -ForegroundColor Blue
    if (Test-Path "data/raw/sample_shifted.csv") {
        nebula-metrics-full --input data/raw/sample.csv --shifted data/raw/sample_shifted.csv --out metrics/full_report.json
    } else {
        Write-Host "⚠️  sample_shifted.csv 파일이 없습니다. 기본 데이터로 테스트합니다." -ForegroundColor Yellow
        Copy-Item "data/raw/sample.csv" "data/raw/sample_shifted.csv"
        nebula-metrics-full --input data/raw/sample.csv --shifted data/raw/sample_shifted.csv --out metrics/full_report.json
    }
    Write-Host "✅ 전체 메트릭 계산 완료!" -ForegroundColor Green
}

function Invoke-Verify {
    Write-Host "🎯 전체 검증 시작..." -ForegroundColor Blue
    Invoke-Tests
    Invoke-Lint
    Invoke-Axes
    Write-Host "🎯 전체 검증 완료!" -ForegroundColor Green
}

# 메인 실행 로직
switch ($Target.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Package }
    "test" { Invoke-Tests }
    "lint" { Invoke-Lint }
    "clean" { Clear-BuildFiles }
    "axes" { Invoke-Axes }
    "retention" { Invoke-Retention }
    "full" { Invoke-Full }
    "verify" { Invoke-Verify }
    default { 
        Write-Host "❌ 알 수 없는 타겟: $Target" -ForegroundColor Red
        Show-Help
    }
} 