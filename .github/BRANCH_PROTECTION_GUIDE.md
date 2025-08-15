# GitHub 브랜치 보호 규칙 설정 가이드 🛡️

## 🎯 목적
이 가이드는 `nebula-con` 레포지토리에서 자동 병합 및 배포를 위한 GitHub 브랜치 보호 규칙을 설정하는 방법을 설명합니다.

## 📋 설정 단계

### 1. GitHub 레포지토리 설정 접근
1. `nebula-con` 레포지토리로 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Branches** 선택

### 2. 브랜치 보호 규칙 추가
1. **Add rule** 버튼 클릭
2. **Branch name pattern**에 `main` 입력
3. **Create** 클릭

### 3. 보호 규칙 세부 설정

#### ✅ 필수 설정 (Required)
- **Require a pull request before merging**
  - ✅ 체크
  - **Require approvals**: `1` (최소 1명의 승인 필요)
  - **Dismiss stale PR approvals when new commits are pushed**: ✅ 체크

- **Require status checks to pass before merging**
  - ✅ 체크
  - **Require branches to be up to date before merging**: ✅ 체크
  - **Status checks that are required**:
    - `NebulaCon CI` (CI 워크플로우)
    - `Enhanced PR Auto Merge` (자동 병합 워크플로우)

#### 🔒 추가 보안 설정 (Optional but Recommended)
- **Require conversation resolution before merging**: ✅ 체크
- **Require signed commits**: ✅ 체크 (커밋 서명 필수)
- **Require linear history**: ✅ 체크 (선형 히스토리 유지)
- **Restrict pushes that create files that use the gitattributes pattern**: ✅ 체크

#### 🚫 제한 설정
- **Restrict pushes to matching branches**: ✅ 체크
- **Allow force pushes**: ❌ 체크 해제
- **Allow deletions**: ❌ 체크 해제

### 4. 설정 저장
1. **Create** 또는 **Save changes** 클릭
2. 설정이 적용되었는지 확인

## 🔄 자동 병합 워크플로우와의 연동

### 현재 설정된 워크플로우
1. **`ci.yml`**: 기본 CI 검사
2. **`auto-merge-enhanced.yml`**: 향상된 자동 병합
3. **`deploy.yml`**: 자동 배포
4. **`pr-auto-merge.yml`**: 스케줄 기반 자동 병합

### 워크플로우 실행 순서
```
PR 생성 → CI 실행 → 품질 검사 → 자동 병합 → 배포 트리거
```

## 🛡️ 안전장치 설명

### 1. 품질 게이트 (Quality Gate)
- **PR 제목 검사**: WIP/DRAFT 상태 확인
- **설명 길이 검사**: 최소 50자 이상
- **품질 점수**: 80점 이상 통과

### 2. CI 상태 확인
- **모든 테스트 통과** 필수
- **구조 검증** 통과
- **코드 품질 검사** 통과

### 3. 수동 승인 (배포 시)
- **프로덕션 배포** 전 수동 승인
- **롤백 절차** 자동 안내
- **실시간 알림** 및 모니터링

## 🚨 주의사항

### 1. 권한 설정
- **GitHub Actions**에 `contents: write`, `pull-requests: write` 권한 필요
- **CODEOWNERS** 파일로 코드 소유권 명시

### 2. 롤백 준비
- **배포 실패 시** 즉시 롤백 가능
- **이전 버전**으로 빠른 복구
- **데이터 백업** 및 복원 절차

### 3. 모니터링
- **워크플로우 실행 상태** 실시간 확인
- **병합 실패** 시 즉시 알림
- **성능 지표** 지속적 추적

## 📊 설정 완료 후 확인사항

### 1. 테스트 PR 생성
1. **새로운 브랜치**에서 변경사항 생성
2. **PR 생성** 및 자동 병합 테스트
3. **워크플로우 실행** 확인

### 2. 자동화 동작 확인
- ✅ CI 자동 실행
- ✅ 품질 검사 통과
- ✅ 자동 병합 성공
- ✅ 배포 파이프라인 트리거

### 3. 알림 설정 확인
- **GitHub Actions** 실행 알림
- **PR 병합** 성공/실패 알림
- **배포** 상태 알림

## 🔧 문제 해결

### 자동 병합이 작동하지 않는 경우
1. **브랜치 보호 규칙** 설정 확인
2. **워크플로우 권한** 확인
3. **CI 상태** 통과 여부 확인
4. **PR 승인** 상태 확인

### 배포가 자동으로 시작되지 않는 경우
1. **워크플로우 트리거** 설정 확인
2. **브랜치 이름** 매칭 확인
3. **수동 승인** 대기 상태 확인

## 📚 추가 리소스

### GitHub 공식 문서
- [Branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-required-status-checks)

### MKM Lab 워크스페이스
- [워크스페이스 규칙](../mkm-lab-workspace-config/WORKSPACE_RULES.md)
- [프로젝트 구조 가이드](../mkm-lab-workspace-config/PROJECT_STRUCTURE.md)

---

**💡 팁: 브랜치 보호 규칙은 한 번 설정하면 자동으로 작동합니다. 정기적으로 설정을 검토하고 필요시 조정하세요!**

**🏆 캐글 해커톤 1위 달성을 위한 안전하고 효율적인 자동화 파이프라인이 구축되었습니다!** 