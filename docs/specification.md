
---

# MusicLog – 音楽再生履歴トラッカー API 仕様書

## 🎧 概要
MusicLog は、ユーザーの音楽再生履歴を記録・検索・分析するためのバックエンド API です。  
Flutter クライアントアプリから利用され、楽曲情報管理、再生ログ記録、統計取得などを提供します。

---

## 📐 基本仕様

### ベース URL
```
/api/v1
```

### 認証方式
- JWT（アクセストークン / リフレッシュトークン）
- 認証が必要な API は `Authorization: Bearer <token>` を要求

---

## 🧑‍💻 エンティティ定義

### User（ユーザー）
| フィールド | 型 | 説明 |
|-----------|----|------|
| id | int | 主キー |
| username | str | ユーザー名（ユニーク） |
| email | str | メールアドレス（ユニーク） |
| password_hash | str | ハッシュ化されたパスワード |
| created_at | datetime | 登録日時 |

---

### Track（楽曲）
| フィールド | 型 | 説明 |
|-----------|----|------|
| id | int | 主キー |
| title | str | 曲名 |
| artist | str | アーティスト名 |
| album | str | アルバム名 |
| duration_sec | int | 再生時間（秒） |
| created_at | datetime | 登録日時 |

---

### PlayLog（再生履歴）
| フィールド | 型 | 説明 |
|-----------|----|------|
| id | int | 主キー |
| user_id | int | 再生したユーザー |
| track_id | int | 再生した曲 |
| played_at | datetime | 再生日時 |
| device | str | 再生デバイス（任意） |

---

## 🔐 認証 API

### POST `/auth/signup`
ユーザー登録。

**Request**
```json
{
  "username": "kensei",
  "email": "test@example.com",
  "password": "password123"
}
```

**Response**
```json
{
  "id": 1,
  "username": "kensei",
  "email": "test@example.com"
}
```

---

### POST `/auth/login`
ログインして JWT を発行。

**Request**
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**Response**
```json
{
  "access_token": "xxxx",
  "refresh_token": "yyyy",
  "token_type": "bearer"
}
```

---

## 🎵 楽曲 API

### GET `/tracks`
楽曲一覧を取得（検索・ページング対応）。

**Query**
- `q`: 曲名・アーティスト検索（任意）
- `limit`: 取得件数（任意）
- `offset`: オフセット（任意）

**Response**
```json
[
  {
    "id": 1,
    "title": "Pretender",
    "artist": "Official髭男dism",
    "album": "Traveler",
    "duration_sec": 330
  }
]
```

---

### POST `/tracks`
楽曲を登録。

**Request**
```json
{
  "title": "Pretender",
  "artist": "Official髭男dism",
  "album": "Traveler",
  "duration_sec": 330
}
```

---

## 📊 再生履歴 API

### POST `/playlogs`
再生履歴を登録。

**Request**
```json
{
  "track_id": 1,
  "played_at": "2026-03-17T23:50:00",
  "device": "iPhone"
}
```

---

### GET `/playlogs`
ユーザーの再生履歴を取得。

**Query**
- `from`: 開始日時（任意）
- `to`: 終了日時（任意）
- `limit`: 件数（任意）
- `offset`: オフセット（任意）

---

## 📈 統計 API

### GET `/stats/top-tracks`
再生回数が多い曲ランキング。

**Response**
```json
[
  {
    "track_id": 1,
    "title": "Pretender",
    "artist": "Official髭男dism",
    "play_count": 42
  }
]
```

---

### GET `/stats/daily`
日別再生数。

**Response**
```json
[
  {
    "date": "2026-03-17",
    "count": 12
  }
]
```

---

## 🗂 推奨ディレクトリ構成

```
musiclog/
  ├── backend/
  │     ├── app/
  │     │     ├── main.py
  │     │     ├── routers/
  │     │     ├── schemas/
  │     │     ├── models/
  │     │     └── services/
  ├── docs/
  │     └── specification.md  ← このファイル
  └── README.md
```

---

## 🚀 GitHub に反映する手順（最短）

```
mkdir docs
```

VS Code で `docs/specification.md` を作成してこの内容を貼り付ける。

```
git add docs/specification.md
git commit -m "Add API specification"
git push
```

---

必要なら、**ER 図・API エラー仕様・レスポンスコード一覧・ユースケース図**も追加できます。  
次にどの部分を仕様書に追加したいか教えてください。
