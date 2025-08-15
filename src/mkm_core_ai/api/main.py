# master_data_collector_v3_web.py
import requests
import xml.etree.ElementTree as ET
import feedparser
import pandas as pd
import time
from tqdm import tqdm
import logging
import sys
from collections import deque
import random
from fastapi import FastAPI, BackgroundTasks, HTTPException
import uvicorn

# --- 작전 설정 ---
RUN_DURATION_HOURS = 12  # 이 스크립트를 실행할 총 시간
RUN_DURATION_SECONDS = RUN_DURATION_HOURS * 3600

# --- FastAPI 앱 인스턴스 생성 ---
app = FastAPI(
    title="프로메테우스 자료 수집기 API",
    description="Cloud Scheduler와 연동하여 마라톤 데이터 수집을 시작하는 API",
    version="3.0"
)

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 기존 수집기 함수들 (수정 없음) ---
def search_pubmed(query, max_results=2000, collected_ids=set()):
    """PubMed에서 논문을 검색하고, 중복을 피해 메타데이터를 수집합니다."""
    logging.info(f"PubMed에서 '{query}' 키워드로 검색을 시작합니다.")
    # ... (이하 로직은 v2와 동일) ...
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_params = {"db": "pubmed", "term": query, "retmax": max_results, "usehistory": "y"}
    try:
        search_response = requests.get(base_url + "esearch.fcgi", params=search_params, timeout=30)
        search_response.raise_for_status()
        search_root = ET.fromstring(search_response.content)
        id_list = [id_elem.text for id_elem in search_root.findall(".//Id")]
        if not id_list: return [], set()
        new_ids = [pmid for pmid in id_list if pmid not in collected_ids]
        if not new_ids: return [], set()
        web_env = search_root.find(".//WebEnv").text
        query_key = search_root.find(".//QueryKey").text
        fetch_params = {"db": "pubmed", "retmode": "xml", "webenv": web_env, "query_key": query_key, "id": ",".join(new_ids)}
        fetch_response = requests.get(base_url + "efetch.fcgi", params=fetch_params, timeout=60)
        fetch_response.raise_for_status()
        articles_root = ET.fromstring(fetch_response.content)
        articles, newly_collected_ids = [], set()
        for article_elem in articles_root.findall(".//PubmedArticle"):
            try:
                pmid = article_elem.find(".//PMID").text
                title = article_elem.find(".//ArticleTitle").text
                abstract_elem = article_elem.find(".//AbstractText")
                abstract = abstract_elem.text if abstract_elem is not None else ""
                authors_list = [f"{author.find('LastName').text} {author.find('Initials').text}" for author in article_elem.findall(".//Author") if author.find('LastName') is not None and author.find('Initials') is not None]
                articles.append({"id": pmid, "title": title, "authors": ", ".join(authors_list), "abstract": abstract, "source": "PubMed", "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"})
                newly_collected_ids.add(pmid)
            except Exception as e: logging.error(f"PubMed 아티클 처리 중 오류: {e}")
        logging.info(f"PubMed에서 '{query}' 키워드로 {len(articles)}개의 새로운 논문을 수집했습니다.")
        return articles, newly_collected_ids
    except requests.exceptions.RequestException as e:
        logging.error(f"PubMed API 요청 중 오류: {e}")
        return [], set()

def search_arxiv(query, max_results=2000, collected_ids=set()):
    """arXiv에서 논문을 검색하고, 중복을 피해 메타데이터를 수집합니다."""
    logging.info(f"arXiv에서 '{query}' 키워드로 검색을 시작합니다.")
    # ... (이하 로직은 v2와 동일) ...
    base_url = "http://export.arxiv.org/api/query?"
    params = {"search_query": f'all:"{query}"', "start": 0, "max_results": max_results, "sortBy": "relevance"}
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        articles, newly_collected_ids = [], set()
        for entry in feed.entries:
            try:
                entry_id = entry.id.split('/abs/')[-1]
                if entry_id in collected_ids: continue
                articles.append({"id": entry_id, "title": entry.title.replace('\n', ' ').strip(), "authors": ", ".join(author.name for author in entry.authors), "abstract": entry.summary.replace('\n', ' ').strip(), "source": "arXiv", "url": entry.link})
                newly_collected_ids.add(entry_id)
            except Exception as e: logging.error(f"arXiv 엔트리 처리 중 오류: {e}")
        logging.info(f"arXiv에서 '{query}' 키워드로 {len(articles)}개의 새로운 논문을 수집했습니다.")
        return articles, newly_collected_ids
    except requests.exceptions.RequestException as e:
        logging.error(f"arXiv API 요청 중 오류: {e}")
        return [], set()

def expand_keywords(articles, current_keywords_queue, processed_keywords):
    """수집된 논문 초록에서 새로운 키워드를 추출하여 큐에 추가합니다."""
    # ... (이하 로직은 v2와 동일) ...
    new_keywords_found = 0
    for article in random.sample(articles, min(len(articles), 10)):
        words = article.get('abstract', '').lower().split()
        for i in range(len(words) - 1):
            potential_keyword = f"{words[i]} {words[i+1]}"
            if potential_keyword not in processed_keywords and len(potential_keyword) > 8:
                current_keywords_queue.append(potential_keyword)
                processed_keywords.add(potential_keyword)
                new_keywords_found += 1
                if new_keywords_found >= 5: return
    if new_keywords_found > 0: logging.info(f"{new_keywords_found}개의 새로운 탐색 키워드를 발견했습니다.")


# --- 🔥 핵심 수정: 백그라운드에서 실행될 실제 작업 함수 ---
def run_marathon_collection_task():
    """12시간 동안 데이터 수집을 수행하는 메인 로직"""
    logging.info("백그라운드 마라톤 수집 작업을 시작합니다.")
    start_time = time.time()
    
    SEED_KEYWORDS = [
        "voice health analysis", "biomedical signal processing", "photoplethysmography",
        "rPPG", "traditional medicine diagnosis AI", "tongue diagnosis", "facial diagnosis",
        "medical image analysis", "wearable sensor data", "health monitoring system",
        "deep learning in healthcare", "acoustic analysis of voice", "jitter", "shimmer",
        "harmonics-to-noise ratio", "cardiovascular signal", "pulse wave analysis"
    ]
    
    keywords_queue = deque(SEED_KEYWORDS)
    processed_keywords = set(SEED_KEYWORDS)
    collected_pubmed_ids = set()
    collected_arxiv_ids = set()
    all_articles_df = pd.DataFrame()
    
    while time.time() - start_time < RUN_DURATION_SECONDS:
        if not keywords_queue:
            logging.warning("탐색할 키워드가 모두 소진되었습니다. 시드 키워드로 재시작합니다.")
            keywords_queue.extend(SEED_KEYWORDS)

        keyword = keywords_queue.popleft()
        
        # PubMed, arXiv 처리 로직은 v2와 동일
        pubmed_articles, new_pubmed_ids = search_pubmed(keyword, collected_ids=collected_pubmed_ids)
        if pubmed_articles:
            collected_pubmed_ids.update(new_pubmed_ids)
            temp_df = pd.DataFrame(pubmed_articles)
            all_articles_df = pd.concat([all_articles_df, temp_df], ignore_index=True)
            expand_keywords(pubmed_articles, keywords_queue, processed_keywords)

        arxiv_articles, new_arxiv_ids = search_arxiv(keyword, collected_ids=collected_arxiv_ids)
        if arxiv_articles:
            collected_arxiv_ids.update(new_arxiv_ids)
            temp_df = pd.DataFrame(arxiv_articles)
            all_articles_df = pd.concat([all_articles_df, temp_df], ignore_index=True)
            expand_keywords(arxiv_articles, keywords_queue, processed_keywords)
        
        # 주기적 저장 (파일 이름에 날짜/시간 추가)
        if int(time.time() - start_time) % 300 == 0: # 5분마다 저장
            filename = f"marathon_collection_live_{time.strftime('%Y%m%d_%H%M%S')}.csv"
            all_articles_df.drop_duplicates(subset=['id', 'source'], inplace=True)
            all_articles_df.to_csv(filename, index=False, encoding="utf-8-sig")
            logging.info(f"중간 저장 완료: {filename} ({len(all_articles_df)}편)")

        time.sleep(2)

    logging.info(f"총 {RUN_DURATION_HOURS}시간의 마라톤 수집 작전을 종료합니다.")
    final_filename = f"marathon_collection_final_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    all_articles_df.drop_duplicates(subset=['id', 'source'], inplace=True)
    all_articles_df.to_csv(final_filename, index=False, encoding="utf-8-sig")
    logging.info(f"최종적으로 총 {len(all_articles_df)}편의 논문 정보를 '{final_filename}' 파일에 저장했습니다.")

# --- 🔥 핵심 수정: API 엔드포인트 정의 ---
@app.post("/collect-data")
async def trigger_collection(background_tasks: BackgroundTasks):
    """
    Cloud Scheduler의 호출을 받아 데이터 수집을 백그라운드 작업으로 시작합니다.
    """
    logging.info("'/collect-data' 엔드포인트 호출됨. 백그라운드 작업을 시작합니다.")
    # 12시간 걸리는 작업을 백그라운드에서 실행하도록 추가
    background_tasks.add_task(run_marathon_collection_task)
    # 작업이 시작되었음을 즉시 클라이언트(Cloud Scheduler)에 알림
    return {"status": "success", "message": "12-hour data collection task has been started in the background."}

@app.get("/")
def read_root():
    return {"message": "MKM Data Collector API is running."}

# --- 로컬 테스트를 위한 실행 블록 ---
if __name__ == "__main__":
    # 이 파일을 직접 실행하면, uvicorn 서버가 로컬에서 가동됩니다.
    # Cloud Run 배포 시에는 이 부분이 아닌, gunicorn과 같은 WSGI 서버를 사용합니다.
    print("로컬 테스트 서버를 시작합니다. http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
