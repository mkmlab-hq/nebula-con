# check_tables.py
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

client = bigquery.Client()
dataset_id = "persona-diary-service.nebula_con_kaggle"

try:
    # 데이터셋 내 모든 테이블 목록 확인
    dataset = client.get_dataset(dataset_id)
    tables = list(client.list_tables(dataset))
    
    print(f"📊 Dataset '{dataset.dataset_id}' contains {len(tables)} table(s):")
    
    if tables:
        for table in tables:
            print(f"  - {table.table_id}")
            
            # 각 테이블의 상세 정보 확인
            try:
                table_obj = client.get_table(table.reference)
                print(f"    📅 Created: {table_obj.created}")
                print(f"    📏 Rows: {table_obj.num_rows:,}")
                print(f"    💾 Size: {table_obj.num_bytes / (1024*1024):.2f} MB")
            except Exception as e:
                print(f"    ❌ Error getting table details: {e}")
    else:
        print("  (No tables found)")
        
    # 특정 테이블 존재 여부 확인
    target_table = "hacker_news_embeddings_pseudo"
    table_ref = f"{dataset_id}.{target_table}"
    
    try:
        table = client.get_table(table_ref)
        print(f"\n✅ Target table '{target_table}' EXISTS")
        print(f"   📅 Created: {table.created}")
        print(f"   📏 Rows: {table.num_rows:,}")
    except NotFound:
        print(f"\n❌ Target table '{target_table}' NOT FOUND")
    except Exception as e:
        print(f"\n❌ Error checking target table: {e}")
        
except Exception as e:
    print(f"❌ FAILURE: An unexpected error occurred: {e}") 