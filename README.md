# タムジレジデンス日本橋 — 公式サイト

東京・日本橋に佇む医療対応型 住宅型有料老人ホーム「タムジレジデンス日本橋」の公式サイト。
タムジcare株式会社 (TAMJ.Corp Care Division) が運営。

公開先: **https://residence.tamjump.com** (Cloudflare Pages)

## 構成

```
.
├── index.html             # トップ
├── about.html             # 運営者情報
├── services.html          # サービス内容
├── assets/
│   ├── css/main.css       # 共通スタイル
│   └── images/            # 施設写真 (ChatGPTで生成し追加予定)
├── carepass/
│   ├── index.html         # 月次活動報告 一覧
│   ├── 2025-06.html       # 各月の活動報告 (12枚)
│   ├── ...
│   ├── 2026-05.html
│   ├── _data.json         # 月別データ
│   ├── _generate.py       # 一括生成スクリプト
│   └── assets/css/report.css
└── README.md
```

## 月次報告書を再生成する

```bash
cd carepass
python3 _generate.py
```

`_data.json` を編集すると12枚のHTMLが一気に更新される。

## Cloudflare Pages デプロイ

1. このリポジトリを GitHub に push
2. Cloudflare Pages から GitHub 連携で接続
3. ビルド設定:
   - Build command: (なし)
   - Build output directory: `/`
4. カスタムドメイン `residence.tamjump.com` を追加 (CNAME 自動設定)

## 画像差し替え

`carepass/2025-06.html` 〜 `2026-05.html` および `index.html` のプレースホルダー
(`<div class="photo-placeholder">`) を、ChatGPT (DALL·E 3) で生成した画像で順次置き換える。

画像生成プロンプトは別途管理。スタイル: ダークネイビーのTAMJ.Corpスクラブセット、
入居者の顔は写さない、editorial photography トーン。

## Care Support Pass 連携

当施設は `https://carepass.tamjump.com` の導入施設 (facility_id=`facility_demo`)。
月次報告書のベースURL: `https://residence.tamjump.com/carepass/{period}.html`
