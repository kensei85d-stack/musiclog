"""
MusicLog API テストスイート
pytest で全 API エンドポイントをテスト
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.app.core.database import get_db, get_session
from backend.app.models.user import User
from backend.app.models.artist import Artist
from backend.app.models.track import Track
from sqlalchemy.orm import Session

# TestClient を初期化
client = TestClient(app)

# グローバル変数でトークンを保存
ACCESS_TOKEN = None
REFRESH_TOKEN = None
USER_ID = None


class TestAuth:
    """認証 API のテスト"""
    
    def test_01_signup(self):
        """ユーザー登録"""
        response = client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data
        global USER_ID
        USER_ID = data["id"]
        print(f"✅ テスト 1 成功: ユーザー登録 (ID: {USER_ID})")
    
    def test_02_login(self):
        """ログイン - JWT トークン取得"""
        response = client.post(
            "/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
        global ACCESS_TOKEN, REFRESH_TOKEN
        ACCESS_TOKEN = data["access_token"]
        REFRESH_TOKEN = data["refresh_token"]
        print(f"✅ テスト 2 成功: ログイン")
        print(f"   access_token: {ACCESS_TOKEN[:50]}...")
    
    def test_03_me(self):
        """認証確認 - Me"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == USER_ID
        assert data["email"] == "test@example.com"
        print(f"✅ テスト 3 成功: 認証確認 (Me)")


class TestHistory:
    """再生履歴 API のテスト"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """各テスト前に実行"""
        pass
    
    def test_04_record_history_1(self):
        """再生ログ記録 #1"""
        response = client.post(
            "/history/",
            json={"track_id": 1},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == USER_ID
        assert data["track_id"] == 1
        assert "played_at" in data
        print(f"✅ テスト 4 成功: 再生ログ記録 #1")
    
    def test_05_record_history_2(self):
        """再生ログ記録 #2"""
        response = client.post(
            "/history/",
            json={"track_id": 2},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        print(f"✅ テスト 5 成功: 再生ログ記録 #2")
    
    def test_06_record_history_3(self):
        """再生ログ記録 #3"""
        response = client.post(
            "/history/",
            json={"track_id": 1},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        print(f"✅ テスト 6 成功: 再生ログ記録 #3")
    
    def test_07_record_history_4(self):
        """再生ログ記録 #4"""
        response = client.post(
            "/history/",
            json={"track_id": 3},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        print(f"✅ テスト 7 成功: 再生ログ記録 #4")
    
    def test_08_record_history_5(self):
        """再生ログ記録 #5"""
        response = client.post(
            "/history/",
            json={"track_id": 1},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        print(f"✅ テスト 8 成功: 再生ログ記録 #5")
    
    def test_09_record_history_6(self):
        """再生ログ記録 #6"""
        response = client.post(
            "/history/",
            json={"track_id": 4},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        print(f"✅ テスト 9 成功: 再生ログ記録 #6")
    
    def test_10_get_history(self):
        """再生履歴取得"""
        response = client.get(
            "/history/",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 6, f"期待: 6件以上, 実際: {len(data)}件"
        assert all("played_at" in item for item in data)
        print(f"✅ テスト 10 成功: 再生履歴取得 ({len(data)}件)")


class TestStats:
    """統計 API のテスト"""
    
    def test_11_stats_summary(self):
        """統計- 概要"""
        response = client.get(
            "/stats/",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_logs" in data
        assert data["total_logs"] >= 6
        print(f"✅ テスト 11 成功: 統計概要 (total_logs: {data['total_logs']})")
    
    def test_12_stats_artist(self):
        """統計 - アーティスト別"""
        response = client.get(
            "/stats/artist",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert all("artist" in item and "count" in item for item in data)
        print(f"✅ テスト 12 成功: 統計 - アーティスト別 ({len(data)}件)")
    
    def test_13_stats_hourly(self):
        """統計 - 時間帯別"""
        response = client.get(
            "/stats/hourly",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ テスト 13 成功: 統計 - 時間帯別 ({len(data)}件)")
    
    def test_14_stats_weekday(self):
        """統計 - 曜日別"""
        response = client.get(
            "/stats/weekday",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ テスト 14 成功: 統計 - 曜日別 ({len(data)}件)")
    
    def test_15_stats_daily(self):
        """統計 - 日付別"""
        response = client.get(
            "/stats/daily",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ テスト 15 成功: 統計 - 日付別 ({len(data)}件)")
    
    def test_16_stats_yearly(self):
        """統計 - 年別"""
        response = client.get(
            "/stats/yearly",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ テスト 16 成功: 統計 - 年別 ({len(data)}件)")


class TestTokenRefresh:
    """トークン更新のテスト"""
    
    def test_17_refresh_token(self):
        """トークン更新"""
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": REFRESH_TOKEN}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        print(f"✅ テスト 17 成功: トークン更新")


class TestAuthError:
    """認証エラーのテスト"""
    
    def test_18_stats_without_auth(self):
        """認証なしで統計 API アクセス - 401 エラー"""
        response = client.get("/stats/")
        assert response.status_code == 403
        print(f"✅ テスト 18 成功: 認証なしで 403 エラー")
    
    def test_19_invalid_token(self):
        """無効なトークンで API アクセス - 401 エラー"""
        response = client.get(
            "/stats/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        print(f"✅ テスト 19 成功: 無効なトークンで 401 エラー")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 MusicLog API 総合テスト実行")
    print("="*60 + "\n")
    pytest.main([__file__, "-v", "-s"])
