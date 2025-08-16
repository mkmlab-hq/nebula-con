import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
from google.oauth2 import service_account
from sklearn.manifold import TSNE
import numpy as np

# --- 환경 설정 ---
PROJECT_ID = "persona-diary-service"
DATASET = "nebula_con_kaggle"
KEY_PATH = "/workspaces/nebula-con/gcs-key.json"
TABLE_NAME_EMBEDDINGS = "hacker_news_embeddings"
TSNE_SAMPLE_LIMIT = 200  # 시각화 효율을 위한 샘플 제한

creds = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=creds, project=PROJECT_ID)

# --- 태그별 질문 분포 시각화 ---
def visualize_tag_distribution():
    sql = f"""
    SELECT SPLIT(tags, ',') AS tag_list FROM `bigquery-public-data.hacker_news.full` WHERE tags IS NOT NULL LIMIT 10000
    """
    df = client.query(sql).to_dataframe()
    # 태그를 1차원 리스트로 변환
    tags = [tag.strip() for sublist in df['tag_list'] for tag in sublist if tag]
    tag_counts = pd.Series(tags).value_counts().head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(x=tag_counts.values, y=tag_counts.index, palette="viridis")
    plt.title("Top 10 Most Popular Tags in Hacker News")
    plt.xlabel("Count")
    plt.ylabel("Tag")
    plt.tight_layout()
    plt.savefig("tag_distribution.png")
    plt.close()
    print("✅ 태그 분포 시각화(tag_distribution.png) 저장 완료.")

# --- 임베딩 t-SNE 시각화 ---
def visualize_embedding_tsne():
    sql = f"""
    SELECT id, title, embedding FROM `{PROJECT_ID}.{DATASET}.{TABLE_NAME_EMBEDDINGS}` LIMIT {TSNE_SAMPLE_LIMIT}
    """
    df = client.query(sql).to_dataframe()
    # 임베딩 벡터를 numpy array로 변환
    embeddings = np.vstack(df['embedding'].values)
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    tsne_results = tsne.fit_transform(embeddings)
    plt.figure(figsize=(10,8))
    plt.scatter(tsne_results[:,0], tsne_results[:,1], alpha=0.7)
    for i, title in enumerate(df['title'].head(20)):
        plt.annotate(title, (tsne_results[i,0], tsne_results[i,1]), fontsize=8, alpha=0.7)
    plt.title("t-SNE Visualization of Hacker News Embeddings")
    plt.xlabel("t-SNE 1")
    plt.ylabel("t-SNE 2")
    plt.tight_layout()
    plt.savefig("embedding_tsne.png")
    plt.close()
    print("✅ 임베딩 t-SNE 시각화(embedding_tsne.png) 저장 완료.")

if __name__ == "__main__":
    visualize_tag_distribution()
    visualize_embedding_tsne()
