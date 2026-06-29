"""
テストデータを PostgreSQL に INSERT するスクリプト
"""
from sqlalchemy.orm import Session
from backend.app.core.database import get_session
from backend.app.models.user import User
from backend.app.models.artist import Artist
from backend.app.models.track import Track
from backend.app.models.Play_history import PlayHistory

def insert_test_data():
    """テストデータをDBに挿入"""
    SessionLocal = get_session()
    db = SessionLocal()
    
    try:
        # アーティストが既に存在するか確認
        artist_count = db.query(Artist).count()
        if artist_count > 0:
            print("✅ アーティストデータは既に存在します")
            return
        
        # アーティストを追加
        artists = [
            Artist(name="Taylor Swift"),
            Artist(name="Ed Sheeran"),
            Artist(name="The Weeknd"),
        ]
        db.add_all(artists)
        db.flush()  # ID を確保
        
        print(f"✅ {len(artists)} 件のアーティストを追加しました")
        
        # トラックを追加
        tracks = [
            Track(title="Love Story", artist_id=artists[0].id),
            Track(title="Anti-Hero", artist_id=artists[0].id),
            Track(title="Shape of You", artist_id=artists[1].id),
            Track(title="Blinding Lights", artist_id=artists[2].id),
            Track(title="Shake It Off", artist_id=artists[0].id),
        ]
        db.add_all(tracks)
        db.commit()
        
        print(f"✅ {len(tracks)} 件のトラックを追加しました")
        print("\n★ テストデータの準備完了！")
        
    except Exception as e:
        db.rollback()
        print(f"❌ エラーが発生しました: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()
