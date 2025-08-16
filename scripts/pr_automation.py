#!/usr/bin/env python3
"""
🚀 PR 자동화 스크립트
GitHub PR의 자동화 기능을 관리합니다.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class PRAutomation:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.github_dir = self.repo_path / ".github"
        self.workflows_dir = self.github_dir / "workflows"
        
    def check_github_setup(self) -> bool:
        """GitHub 설정 확인"""
        try:
            if not self.github_dir.exists():
                print("❌ .github 디렉토리가 없습니다.")
                return False
                
            if not self.workflows_dir.exists():
                print("❌ .github/workflows 디렉토리가 없습니다.")
                return False
                
            print("✅ GitHub 설정 확인 완료")
            return True
            
        except Exception as e:
            print(f"❌ GitHub 설정 확인 실패: {e}")
            return False
    
    def list_workflows(self) -> List[str]:
        """현재 워크플로우 목록 출력"""
        try:
            workflows = []
            for workflow_file in self.workflows_dir.glob("*.yml"):
                workflows.append(workflow_file.name)
            
            print(f"📋 현재 워크플로우 ({len(workflows)}개):")
            for workflow in workflows:
                print(f"   - {workflow}")
            
            return workflows
            
        except Exception as e:
            print(f"❌ 워크플로우 목록 조회 실패: {e}")
            return []
    
    def validate_workflow(self, workflow_name: str) -> bool:
        """워크플로우 파일 유효성 검사"""
        try:
            workflow_path = self.workflows_dir / workflow_name
            if not workflow_path.exists():
                print(f"❌ 워크플로우 파일이 없습니다: {workflow_name}")
                return False
            
            # YAML 문법 검사 (간단한 검사)
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 기본 YAML 구조 검사
            if 'name:' not in content:
                print(f"❌ 워크플로우 이름이 정의되지 않았습니다: {workflow_name}")
                return False
                
            if 'on:' not in content:
                print(f"❌ 트리거가 정의되지 않았습니다: {workflow_name}")
                return False
                
            if 'jobs:' not in content:
                print(f"❌ 작업이 정의되지 않았습니다: {workflow_name}")
                return False
            
            print(f"✅ 워크플로우 유효성 검사 통과: {workflow_name}")
            return True
            
        except Exception as e:
            print(f"❌ 워크플로우 검사 실패: {e}")
            return False
    
    def check_pr_status(self) -> Dict[str, any]:
        """PR 상태 확인"""
        try:
            # Git 상태 확인
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, cwd=self.repo_path
            )
            
            if result.returncode != 0:
                print("❌ Git 상태 확인 실패")
                return {}
            
            changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # 브랜치 정보 확인
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True, text=True, cwd=self.repo_path
            )
            
            current_branch = result.stdout.strip() if result.stdout else "unknown"
            
            # 원격 브랜치 정보 확인
            result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True, text=True, cwd=self.repo_path
            )
            
            remotes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            status = {
                'current_branch': current_branch,
                'changes': len(changes),
                'remotes': remotes,
                'has_changes': len(changes) > 0
            }
            
            print(f"📊 PR 상태:")
            print(f"   - 현재 브랜치: {current_branch}")
            print(f"   - 변경된 파일: {len(changes)}개")
            print(f"   - 원격 저장소: {len(remotes)}개")
            
            return status
            
        except Exception as e:
            print(f"❌ PR 상태 확인 실패: {e}")
            return {}
    
    def create_pr(self, title: str, body: str, target_branch: str = "main") -> bool:
        """PR 생성 (GitHub CLI 사용)"""
        try:
            # GitHub CLI 설치 확인
            result = subprocess.run(['gh', '--version'], capture_output=True)
            if result.returncode != 0:
                print("❌ GitHub CLI가 설치되지 않았습니다.")
                print("   설치 방법: https://cli.github.com/")
                return False
            
            # PR 생성
            cmd = [
                'gh', 'pr', 'create',
                '--title', title,
                '--body', body,
                '--base', target_branch
            ]
            
            result = subprocess.run(cmd, cwd=self.repo_path)
            
            if result.returncode == 0:
                print("✅ PR 생성 완료!")
                return True
            else:
                print("❌ PR 생성 실패")
                return False
                
        except Exception as e:
            print(f"❌ PR 생성 중 오류: {e}")
            return False
    
    def run_checks(self) -> bool:
        """모든 체크 실행"""
        try:
            print("🔍 PR 자동화 체크 시작...")
            print("=" * 50)
            
            # 1. GitHub 설정 확인
            if not self.check_github_setup():
                return False
            
            # 2. 워크플로우 목록
            workflows = self.list_workflows()
            
            # 3. 워크플로우 유효성 검사
            for workflow in workflows:
                self.validate_workflow(workflow)
            
            # 4. PR 상태 확인
            self.check_pr_status()
            
            print("=" * 50)
            print("✅ 모든 체크 완료!")
            
            return True
            
        except Exception as e:
            print(f"❌ 체크 실행 실패: {e}")
            return False
    
    def generate_pr_template(self, pr_type: str = "feature") -> str:
        """PR 템플릿 생성"""
        templates = {
            "feature": {
                "title": "✨ 새로운 기능 추가",
                "body": """## 📝 변경 사항 요약
새로운 기능을 추가했습니다.

## 🎯 해결한 이슈
- Related to #(이슈번호)

## 🔍 변경 내용 상세
### 추가된 기능
- [ ] 새로운 기능 1
- [ ] 새로운 기능 2

## 🧪 테스트 방법
1. 기능 테스트
2. 예상 결과 확인

## ✅ 체크리스트
- [ ] 코드가 기존 스타일을 따르는가?
- [ ] 자체 테스트를 수행했는가?
- [ ] 문서를 업데이트했는가?
"""
            },
            "bugfix": {
                "title": "🐛 버그 수정",
                "body": """## 📝 변경 사항 요약
버그를 수정했습니다.

## 🎯 해결한 이슈
- Fixes #(이슈번호)

## 🔍 변경 내용 상세
### 수정된 기능
- [ ] 버그 수정 1
- [ ] 버그 수정 2

## 🧪 테스트 방법
1. 버그 재현 확인
2. 수정 결과 확인

## ✅ 체크리스트
- [ ] 코드가 기존 스타일을 따르는가?
- [ ] 자체 테스트를 수행했는가?
- [ ] 문서를 업데이트했는가?
"""
            },
            "refactor": {
                "title": "♻️ 코드 리팩토링",
                "body": """## 📝 변경 사항 요약
코드를 리팩토링했습니다.

## 🎯 해결한 이슈
- Related to #(이슈번호)

## 🔍 변경 내용 상세
### 리팩토링 내용
- [ ] 코드 구조 개선
- [ ] 성능 최적화

## 🧪 테스트 방법
1. 기존 기능 동작 확인
2. 성능 테스트

## ✅ 체크리스트
- [ ] 코드가 기존 스타일을 따르는가?
- [ ] 자체 테스트를 수행했는가?
- [ ] 문서를 업데이트했는가?
"""
            }
        }
        
        if pr_type not in templates:
            pr_type = "feature"
        
        template = templates[pr_type]
        return template["title"], template["body"]

def main():
    """메인 실행 함수"""
    automation = PRAutomation()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            automation.run_checks()
        elif command == "create-pr":
            if len(sys.argv) < 3:
                print("사용법: python pr_automation.py create-pr <PR타입>")
                print("PR 타입: feature, bugfix, refactor")
                return
            
            pr_type = sys.argv[2]
            title, body = automation.generate_pr_template(pr_type)
            
            print(f"📝 PR 제목: {title}")
            print(f"📄 PR 내용:\n{body}")
            
            if input("\n이 PR을 생성하시겠습니까? (y/N): ").lower() == 'y':
                automation.create_pr(title, body)
        else:
            print("사용법:")
            print("  python pr_automation.py check          - 체크 실행")
            print("  python pr_automation.py create-pr <타입> - PR 생성")
    else:
        automation.run_checks()

if __name__ == "__main__":
    main() 