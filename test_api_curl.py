"""
MusicLog API テスト - curl を使用した自動テスト
"""
import subprocess
import json
import sys

BASE_URL = "http://127.0.0.1:8000"
HEADERS_JSON = "-H 'Content-Type: application/json'"

# グローバル変数
access_token = None
refresh_token = None
user_id = None

def curl_post(endpoint, data, token=None):
    """POST リクエスト"""
    cmd = f"curl -s -X POST {BASE_URL}{endpoint} {HEADERS_JSON}"
    if token:
        cmd += f" -H 'Authorization: Bearer {token}'"
    cmd += f" -d '{json.dumps(data)}'"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        print(f"❌ JSON パースエラー: {result.stdout}")
        return None

def curl_get(endpoint, token=None):
    """GET リクエスト"""
    cmd = f"curl -s -X GET {BASE_URL}{endpoint}"
    if token:
        cmd += f" -H 'Authorization: Bearer {token}'"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        print(f"❌ JSON パースエラー: {result.stdout}")
        return None

def test_signup():
    """テスト 1: ユーザー登録"""
    print("\n[テスト 1] ユーザー登録")
    data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password123"
    }
    response = curl_post("/auth/signup", data)
    
    if response and "id" in response:
        global user_id
        user_id = response["id"]
        print(f"✅ 成功: ユーザー登録 (ID: {user_id})")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_login():
    """テスト 2: ログイン"""
    print("\n[テスト 2] ログイン")
    data = {
        "email": "test2@example.com",
        "password": "password123"
    }
    response = curl_post("/auth/login", data)
    
    if response and "access_token" in response:
        global access_token, refresh_token
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        print(f"✅ 成功: ログイン")
        print(f"   access_token: {access_token[:50]}...")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_me():
    """テスト 3: 認証確認"""
    print("\n[テスト 3] 認証確認 (/auth/me)")
    response = curl_get("/auth/me", access_token)
    
    if response and response.get("id") == user_id:
        print(f"✅ 成功: 認証確認")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_record_history():
    """テスト 4-9: 再生ログ記録"""
    print("\n[テスト 4-9] 再生ログ記録（6件）")
    track_ids = [1, 2, 1, 3, 1, 4]
    
    for i, track_id in enumerate(track_ids, 1):
        data = {"track_id": track_id}
        response = curl_post("/history/", data, access_token)
        
        if response and "id" in response:
            print(f"  ✅ #{i}: track_id={track_id}")
        else:
            print(f"  ❌ #{i}: 失敗")
            return False
    
    return True

def test_get_history():
    """テスト 10: 再生履歴取得"""
    print("\n[テスト 10] 再生履歴取得 (/history/)")
    response = curl_get("/history/", access_token)
    
    if response and isinstance(response, list) and len(response) >= 6:
        print(f"✅ 成功: 再生履歴取得 ({len(response)}件)")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_stats_summary():
    """テスト 11: 統計概要"""
    print("\n[テスト 11] 統計概要 (/stats/)")
    response = curl_get("/stats/", access_token)
    
    if response and "total_logs" in response:
        print(f"✅ 成功: 統計概要 (total_logs: {response['total_logs']})")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_stats_artist():
    """テスト 12: アーティスト別統計"""
    print("\n[テスト 12] アーティスト別統計 (/stats/artist)")
    response = curl_get("/stats/artist", access_token)
    
    if response and isinstance(response, list) and len(response) > 0:
        print(f"✅ 成功: アーティスト別統計 ({len(response)}件)")
        for item in response[:3]:
            print(f"   {item['artist']}: {item['count']}回")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_stats_hourly():
    """テスト 13: 時間帯別統計"""
    print("\n[テスト 13] 時間帯別統計 (/stats/hourly)")
    response = curl_get("/stats/hourly", access_token)
    
    if response and isinstance(response, list):
        print(f"✅ 成功: 時間帯別統計")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_stats_weekday():
    """テスト 14: 曜日別統計"""
    print("\n[テスト 14] 曜日別統計 (/stats/weekday)")
    response = curl_get("/stats/weekday", access_token)
    
    if response and isinstance(response, list):
        print(f"✅ 成功: 曜日別統計")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_stats_daily():
    """テスト 15: 日付別統計"""
    print("\n[テスト 15] 日付別統計 (/stats/daily)")
    response = curl_get("/stats/daily", access_token)
    
    if response and isinstance(response, list):
        print(f"✅ 成功: 日付別統計")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_stats_yearly():
    """テスト 16: 年別統計"""
    print("\n[テスト 16] 年別統計 (/stats/yearly)")
    response = curl_get("/stats/yearly", access_token)
    
    if response and isinstance(response, list):
        print(f"✅ 成功: 年別統計")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_refresh_token():
    """テスト 17: トークン更新"""
    print("\n[テスト 17] トークン更新 (/auth/refresh)")
    data = {"refresh_token": refresh_token}
    response = curl_post("/auth/refresh", data)
    
    if response and "access_token" in response:
        print(f"✅ 成功: トークン更新")
        return True
    else:
        print(f"❌ 失敗: {response}")
        return False

def test_no_auth():
    """テスト 18: 認証なしでアクセス"""
    print("\n[テスト 18] 認証なしで /stats/ にアクセス（期待: 403 エラー）")
    cmd = f"curl -s -w '\\nStatus: %{{http_code}}' -X GET {BASE_URL}/stats/"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "Status: 403" in result.stdout:
        print(f"✅ 成功: 403 エラーが返された（認証なし）")
        return True
    else:
        print(f"❌ 失敗: {result.stdout}")
        return False

def main():
    """メインテスト実行"""
    print("="*70)
    print("🧪 MusicLog API テスト（curl 使用）")
    print("="*70)
    
    tests = [
        ("ユーザー登録", test_signup),
        ("ログイン", test_login),
        ("認証確認", test_me),
        ("再生ログ記録", test_record_history),
        ("再生履歴取得", test_get_history),
        ("統計概要", test_stats_summary),
        ("アーティスト別", test_stats_artist),
        ("時間帯別", test_stats_hourly),
        ("曜日別", test_stats_weekday),
        ("日付別", test_stats_daily),
        ("年別", test_stats_yearly),
        ("トークン更新", test_refresh_token),
        ("認証なしアクセス", test_no_auth),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 例外発生: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"📊 テスト結果: 成功 {passed}件 / 失敗 {failed}件")
    print("="*70)
    
    if failed == 0:
        print("✨ すべてのテストが成功しました！")
        print("\n🎉 Phase 2 実装完了！")
        return 0
    else:
        print(f"⚠️  {failed}件のテストが失敗しました")
        return 1

if __name__ == "__main__":
    sys.exit(main())
