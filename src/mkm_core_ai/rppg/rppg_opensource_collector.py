#!/usr/bin/env python3
"""
rPPG 및 얼굴분석 오픈소스 전용 수집기
AI 연구원을 활용하여 실제 구현 가능한 코드를 대량 수집
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
import os

class RPPGOpenSourceCollector:
    def __init__(self):
        """rPPG 오픈소스 수집기 초기화"""
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        # rPPG 및 얼굴분석 특화 키워드
        self.rppg_keywords = [
            "rPPG", "remote photoplethysmography", "face heart rate", 
            "video heart rate", "camera heart rate", "non-contact heart rate",
            "face blood pressure", "video blood pressure", "face vital signs",
            "PhysNet", "rPPG-Toolbox", "face-vid2vid", "face analysis",
            "facial recognition", "face detection", "face landmarks",
            "OpenFace", "InsightFace", "MediaPipe", "dlib face",
            "face emotion", "face expression", "face health",
            "biometric face", "face authentication", "face liveness"
        ]
        
        # 수집 결과 저장
        self.collected_repos = []
        self.start_time = datetime.now()
        
        print("🔬 rPPG 및 얼굴분석 오픈소스 수집기 시작")
        print(f"📅 시작 시간: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 수집 키워드: {len(self.rppg_keywords)}개")
        print("=" * 60)
    
    def search_github_repos(self, keyword: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """GitHub에서 키워드로 저장소 검색"""
        print(f"🔍 검색 중: {keyword}")
        
        repositories = []
        page = 1
        
        while len(repositories) < max_results:
            try:
                url = f"{self.base_url}/search/repositories"
                params = {
                    "q": f"{keyword} language:python",
                    "sort": "stars",
                    "order": "desc",
                    "page": page,
                    "per_page": min(100, max_results - len(repositories))
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 403:
                    print("⚠️ API 레이트 리밋 도달. 60초 대기...")
                    time.sleep(60)
                    continue
                
                if response.status_code != 200:
                    print(f"❌ API 호출 실패: {response.status_code}")
                    break
                
                data = response.json()
                
                if not data.get("items"):
                    break
                
                for repo in data["items"]:
                    if len(repositories) >= max_results:
                        break
                    
                    # rPPG 관련성 점수 계산
                    relevance_score = self.calculate_relevance_score(repo, keyword)
                    
                    if relevance_score > 0.3:  # 관련성 임계값
                        repo_info = {
                            "name": repo["full_name"],
                            "description": repo.get("description", ""),
                            "stars": repo["stargazers_count"],
                            "forks": repo["forks_count"],
                            "language": repo.get("language", ""),
                            "url": repo["html_url"],
                            "api_url": repo["url"],
                            "created_at": repo["created_at"],
                            "updated_at": repo["updated_at"],
                            "size": repo["size"],
                            "topics": repo.get("topics", []),
                            "keyword": keyword,
                            "relevance_score": relevance_score
                        }
                        repositories.append(repo_info)
                
                page += 1
                time.sleep(1)  # API 레이트 리밋 준수
                
            except Exception as e:
                print(f"❌ 검색 중 오류: {e}")
                break
        
        print(f"✅ {len(repositories)}개 저장소 발견")
        return repositories
    
    def calculate_relevance_score(self, repo: Dict[str, Any], keyword: str) -> float:
        """저장소의 rPPG 관련성 점수 계산"""
        score = 0.0
        
        # 제목 관련성
        name = repo["full_name"].lower()
        if keyword.lower() in name:
            score += 0.4
        
        # 설명 관련성
        description = repo.get("description", "").lower()
        if description:
            if keyword.lower() in description:
                score += 0.3
            
            # rPPG 관련 키워드들
            rppg_terms = ["rppg", "photoplethysmography", "heart rate", "blood pressure", 
                         "face", "video", "camera", "vital", "biometric"]
            for term in rppg_terms:
                if term in description:
                    score += 0.1
        
        # 토픽 관련성
        topics = repo.get("topics", [])
        for topic in topics:
            if keyword.lower() in topic.lower():
                score += 0.2
            
            # rPPG 관련 토픽들
            rppg_topics = ["rppg", "face-analysis", "heart-rate", "biometrics", 
                          "computer-vision", "medical", "health"]
            if topic.lower() in rppg_topics:
                score += 0.1
        
        # 스타 수에 따른 가중치
        stars = repo["stargazers_count"]
        if stars > 1000:
            score += 0.1
        elif stars > 500:
            score += 0.05
        elif stars > 100:
            score += 0.02
        
        return min(score, 1.0)  # 최대 1.0
    
    def get_repository_details(self, repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """저장소 상세 정보 수집"""
        try:
            response = requests.get(repo_info["api_url"], headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                # README 파일 내용 가져오기
                readme_content = self.get_readme_content(repo_info["name"])
                
                # 주요 파일 목록 가져오기
                files = self.get_repository_files(repo_info["name"])
                
                detailed_info = {
                    **repo_info,
                    "readme_content": readme_content,
                    "files": files,
                    "license": repo_data.get("license", {}).get("name", ""),
                    "default_branch": repo_data.get("default_branch", ""),
                    "open_issues": repo_data.get("open_issues_count", 0),
                    "subscribers_count": repo_data.get("subscribers_count", 0),
                    "network_count": repo_data.get("network_count", 0),
                    "has_wiki": repo_data.get("has_wiki", False),
                    "has_pages": repo_data.get("has_pages", False),
                    "has_downloads": repo_data.get("has_downloads", False)
                }
                
                return detailed_info
                
        except Exception as e:
            print(f"❌ 상세 정보 수집 실패 ({repo_info['name']}): {e}")
        
        return repo_info
    
    def get_readme_content(self, repo_name: str) -> str:
        """README 파일 내용 가져오기"""
        try:
            url = f"{self.base_url}/repos/{repo_name}/readme"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                readme_data = response.json()
                import base64
                content = base64.b64decode(readme_data["content"]).decode("utf-8")
                return content[:2000]  # 첫 2000자만
                
        except Exception as e:
            print(f"❌ README 수집 실패 ({repo_name}): {e}")
        
        return ""
    
    def get_repository_files(self, repo_name: str) -> List[str]:
        """저장소 주요 파일 목록 가져오기"""
        try:
            url = f"{self.base_url}/repos/{repo_name}/contents"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                contents = response.json()
                files = []
                
                for item in contents:
                    if item["type"] == "file":
                        files.append(item["name"])
                
                return files[:20]  # 상위 20개 파일만
                
        except Exception as e:
            print(f"❌ 파일 목록 수집 실패 ({repo_name}): {e}")
        
        return []
    
    def collect_all_repositories(self) -> List[Dict[str, Any]]:
        """모든 키워드로 저장소 수집"""
        all_repos = []
        
        for keyword in self.rppg_keywords:
            print(f"\n📂 키워드: {keyword}")
            repos = self.search_github_repos(keyword, max_results=15)
            
            # 중복 제거
            existing_names = {repo["name"] for repo in all_repos}
            new_repos = [repo for repo in repos if repo["name"] not in existing_names]
            
            all_repos.extend(new_repos)
            print(f"✅ {len(new_repos)}개 새 저장소 추가")
            
            time.sleep(2)  # API 레이트 리밋 준수
        
        # 관련성 점수로 정렬
        all_repos.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # 상위 100개만 선택
        top_repos = all_repos[:100]
        
        print(f"\n🎯 총 {len(top_repos)}개 저장소 선별 완료")
        return top_repos
    
    def save_results(self, repositories: List[Dict[str, Any]]) -> str:
        """결과를 JSON 파일로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rppg_opensource_collection_{timestamp}.json"
        
        result_data = {
            "metadata": {
                "collection_date": datetime.now().isoformat(),
                "total_repositories": len(repositories),
                "keywords_searched": self.rppg_keywords,
                "collection_duration": str(datetime.now() - self.start_time)
            },
            "repositories": repositories,
            "statistics": {
                "avg_stars": sum(r["stars"] for r in repositories) / len(repositories) if repositories else 0,
                "avg_forks": sum(r["forks"] for r in repositories) / len(repositories) if repositories else 0,
                "top_languages": self.get_top_languages(repositories),
                "top_keywords": self.get_top_keywords(repositories)
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 결과 저장 완료: {filename}")
        return filename
    
    def get_top_languages(self, repositories: List[Dict[str, Any]]) -> Dict[str, int]:
        """상위 프로그래밍 언어 통계"""
        languages = {}
        for repo in repositories:
            lang = repo.get("language", "Unknown")
            languages[lang] = languages.get(lang, 0) + 1
        return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def get_top_keywords(self, repositories: List[Dict[str, Any]]) -> Dict[str, int]:
        """상위 키워드 통계"""
        keywords = {}
        for repo in repositories:
            keyword = repo.get("keyword", "Unknown")
            keywords[keyword] = keywords.get(keyword, 0) + 1
        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def generate_report(self, repositories: List[Dict[str, Any]]) -> str:
        """수집 결과 리포트 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rppg_opensource_report_{timestamp}.md"
        
        report = f"""# rPPG 및 얼굴분석 오픈소스 수집 보고서

## 📊 수집 요약
- **수집 시간**: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}
- **총 저장소**: {len(repositories)}개
- **수집 키워드**: {len(self.rppg_keywords)}개
- **수집 소요시간**: {datetime.now() - self.start_time}

## 🏆 상위 10개 저장소

"""
        
        for i, repo in enumerate(repositories[:10], 1):
            report += f"""### {i}. {repo['name']}
- **설명**: {repo['description'][:100]}...
- **스타**: ⭐{repo['stars']:,}
- **포크**: 🔀{repo['forks']:,}
- **언어**: {repo['language']}
- **관련성 점수**: {repo['relevance_score']:.2f}
- **URL**: {repo['url']}

"""
        
        report += f"""
## 📈 통계 정보

### 프로그래밍 언어 분포
"""
        
        languages = self.get_top_languages(repositories)
        for lang, count in languages.items():
            report += f"- **{lang}**: {count}개\n"
        
        report += f"""
### 키워드별 분포
"""
        
        keywords = self.get_top_keywords(repositories)
        for keyword, count in keywords.items():
            report += f"- **{keyword}**: {count}개\n"
        
        report += f"""
## 🎯 활용 방안

### 1. 즉시 활용 가능한 저장소
- rPPG-Toolbox: 기본 rPPG 구현
- OpenFace: 얼굴 인식 및 랜드마크
- InsightFace: 고성능 얼굴 인식
- MediaPipe: 실시간 얼굴 분석

### 2. 참고 자료로 활용
- 구현 방법론 학습
- 성능 최적화 기법
- 최신 알고리즘 동향

### 3. 통합 개발 계획
- 기존 얼굴분석 시스템과 통합
- 성능 비교 및 개선
- 새로운 기능 추가

---
**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 리포트 생성 완료: {filename}")
        return filename

def main():
    """메인 실행 함수"""
    print("🚀 rPPG 및 얼굴분석 오픈소스 수집 시작")
    print("=" * 60)
    
    # 수집기 초기화
    collector = RPPGOpenSourceCollector()
    
    # 저장소 수집
    print("\n📥 저장소 수집 시작...")
    repositories = collector.collect_all_repositories()
    
    # 결과 저장
    print("\n💾 결과 저장 중...")
    json_filename = collector.save_results(repositories)
    
    # 리포트 생성
    print("\n📋 리포트 생성 중...")
    report_filename = collector.generate_report(repositories)
    
    print("\n🎉 수집 완료!")
    print(f"📁 JSON 파일: {json_filename}")
    print(f"📄 리포트 파일: {report_filename}")
    print(f"📊 총 {len(repositories)}개 저장소 수집")
    
    # 상위 5개 저장소 출력
    print("\n🏆 상위 5개 저장소:")
    for i, repo in enumerate(repositories[:5], 1):
        print(f"{i}. {repo['name']} (⭐{repo['stars']:,}, 점수: {repo['relevance_score']:.2f})")

if __name__ == "__main__":
    main() 