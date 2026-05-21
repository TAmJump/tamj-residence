#!/usr/bin/env python3
"""
タムジレジデンス日本橋 / Care Support Pass 月次活動報告書 一括生成スクリプト
_data.json を読み込み、12ヶ月分の HTML + index.html を出力する。
画像はWebPで /assets/images/ に配置されている前提。
"""

import json
import os
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "_data.json")
OUT_DIR = BASE_DIR

# 目標値 (施設プロフィール定数 / 1棟 60室)
TARGET_SUPPORTERS = 120000
TARGET_MONTHLY_REVENUE = 30000000   # ¥3,000万 (= 12万人 × 250円/口)

REPORT_TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{period_ja} 活動報告 | タムジレジデンス日本橋</title>
<meta name="description" content="タムジレジデンス日本橋 — {period_ja} の月次活動報告書 (Care Support Pass)。{theme}">
<meta property="og:title" content="{period_ja} 活動報告 | タムジレジデンス日本橋">
<meta property="og:description" content="{theme}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://residence.tamjump.com{og_image_abs}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Noto+Serif+JP:wght@400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/css/report.css?v=20260521a">
</head>
<body>

<nav class="report-nav">
  <div class="report-nav-in">
    <a href="https://residence.tamjump.com/" class="report-nav-brand" style="text-decoration:none">
      <span class="mark">TAMJ.Corp</span>
      <span class="name">タムジレジデンス日本橋</span>
    </a>
    <div class="report-nav-links">
      <a href="https://residence.tamjump.com/">トップ</a>
      <a href="./">活動報告 一覧</a>
      <a href="https://carepass.tamjump.com" target="_blank" rel="noopener">Care Support Pass</a>
    </div>
  </div>
</nav>

<main class="report">

  <!-- HERO -->
  <section class="report-hero">
    <div class="csp-mark">Monthly Care Report</div>
    <div class="report-period">{period_ja} ({period_en})</div>
    <h1>{theme}</h1>
    <p class="report-lede">{lede}</p>
  </section>

  <!-- KPI -->
  <section class="report-section">
    <div class="section-title">Numbers</div>
    <h2 class="section-h">数字で見る今月</h2>
    <div class="kpi-grid">
{kpi_blocks}
    </div>
  </section>

  <!-- HERO PHOTO -->
  <section class="report-section">
    <div class="section-title">In Focus</div>
    <h2 class="section-h">今月の主な瞬間</h2>
    <figure class="photo-figure" style="aspect-ratio:auto">
      <img src="{hero_image}" alt="{hero_image_alt}" loading="lazy">
      <figcaption>{hero_caption}</figcaption>
    </figure>
  </section>

  <!-- PHOTOS -->
  <section class="report-section">
    <div class="section-title">Album</div>
    <h2 class="section-h">今月のひとこま</h2>
    <div class="photos-grid">
{photo_blocks}
    </div>
  </section>

  <!-- BODY -->
  <section class="report-section">
    <div class="section-title">Story</div>
    <h2 class="section-h">今月の活動</h2>
    <div class="body-block">
{body_blocks}
    </div>
  </section>

  <!-- FINANCE / Care Support Pass 収支報告 -->
  <section class="report-section">
    <div class="section-title">Care Support Pass · Finance</div>
    <h2 class="section-h">支援者数 と 収支報告 — 12ヶ月推移</h2>

    <!-- 折れ線グラフ 2枚 -->
    <div class="finance-charts">
      <figure class="finance-chart">
        <figcaption class="finance-chart-title">
          <span>支援者数の推移</span>
          <small>目標 120,000 名 / 月</small>
        </figcaption>
        {chart_supporters_svg}
      </figure>
      <figure class="finance-chart">
        <figcaption class="finance-chart-title">
          <span>支援金 (雑収入) の累計</span>
          <small>本業売上とは別枠の制限付き原資</small>
        </figcaption>
        {chart_cumulative_svg}
      </figure>
    </div>

    <!-- 12ヶ月推移表 -->
    <div class="finance-table-wrap">
      <table class="finance-timeline">
        <thead>
          <tr>
            <th>月</th>
            <th class="num">支援者数</th>
            <th class="num">月の支援額</th>
            <th class="num">累計</th>
            <th class="num">達成率</th>
            <th>使い道(要約)</th>
          </tr>
        </thead>
        <tbody>
{timeline_rows}
        </tbody>
      </table>
    </div>
  </section>

  <!-- PL差額 (通常モデル vs CSP導入モデル) -->
  <section class="report-section finance-pl-section">
    <div class="section-title">PL Comparison · 年額換算 (百万円/年)</div>
    <h2 class="section-h">通常運営モデル vs Care Support Pass 導入モデル</h2>
    <p class="finance-pl-lede">
      Care Support Pass の支援金は <strong>「本業売上」ではなく「制限付き原資 (雑収入)」</strong> です。
      導入後は <strong>本業売上 (入居者本人徴収・介護/医療保険) はむしろ下がります</strong>。
      入居者本人の月額負担を ¥215,000 → ¥30,000 に大きく下げ、要介護度の低い層を中心に受け入れることで、
      国費依存も意図的に下げる設計だからです。
      その下がった分を <strong>支援者の皆様からの原資</strong> で支え、なおかつ <strong>スタッフは削らず増やす</strong>。
      これが Care Support Pass 導入施設のPLの全体像です。
    </p>
    <div class="finance-pl-wrap">
      <table class="finance-pl-table">
        <thead>
          <tr>
            <th>項目</th>
            <th class="num">通常運営<br><small>百万円/年</small></th>
            <th class="num">CSP導入<br><small>百万円/年</small></th>
            <th class="num">差額/効果<br><small>百万円/年</small></th>
            <th>意味</th>
          </tr>
        </thead>
        <tbody>
          <tr class="group"><td colspan="5">本業収入 — 入居者・保険から</td></tr>
          <tr><td>入居者本人からの徴収</td><td class="num">164.6</td><td class="num">22.95</td><td class="num neg">▲141.65</td><td>本人負担 ¥215k/月 → ¥30k/月 へ。意図的に下げる。</td></tr>
          <tr><td>介護保険・医療保険等</td><td class="num">152.9</td><td class="num">76.55</td><td class="num neg">▲76.35</td><td>要支援〜要介護1・2 中心へ。国費使用を下げる方針。</td></tr>
          <tr class="subtotal"><td>本業売上 合計</td><td class="num">317.5</td><td class="num">99.5</td><td class="num neg">▲218.0</td><td>導入後、本業売上は下がる。これが前提。</td></tr>
          <tr class="group"><td colspan="5">CSP制限付き原資 — 本業売上とは別枠の雑収入</td></tr>
          <tr><td>本人負担軽減原資 (45%)</td><td class="num">0.0</td><td class="num pos">178.2</td><td class="num pos">+178.2</td><td>家賃・管理費・サービス支援費・食費差額を支える。</td></tr>
          <tr><td>スタッフ配置増・賃金改善原資 (30%)</td><td class="num">0.0</td><td class="num pos">118.8</td><td class="num pos">+118.8</td><td>人件費増、夜勤補強、見守り、教育、休憩環境に使う。</td></tr>
          <tr><td>初期費用・住み替え・家財整理支援 (10%)</td><td class="num">0.0</td><td class="num pos">39.6</td><td class="num pos">+39.6</td><td>施設PL外の社会的支援枠。入居初期の壁を下げる。</td></tr>
          <tr><td>月次報告・監査・事務局 (10%)</td><td class="num">0.0</td><td class="num pos">39.6</td><td class="num pos">+39.6</td><td>透明性の運営コスト。未報告なら支援停止。</td></tr>
          <tr><td>予備費 (5%)</td><td class="num">0.0</td><td class="num pos">19.8</td><td class="num pos">+19.8</td><td>退去・緊急入居・補修等のバッファ。</td></tr>
          <tr class="subtotal"><td>CSP原資 合計</td><td class="num">0.0</td><td class="num pos">396.0</td><td class="num pos">+396.0</td><td>1棟 12万人支援モデル。施設PLに入るのは主に上2項目。</td></tr>
          <tr class="group"><td colspan="5">運営コスト — 削る/増やすを分ける</td></tr>
          <tr><td>人件費</td><td class="num neg">▲116.75</td><td class="num neg">▲157.5</td><td class="num neg">▲40.75</td><td>下げない。人数 35→41名、賃金334→384万/人。</td></tr>
          <tr><td>食材・原価</td><td class="num neg">▲35.7</td><td class="num neg">▲30.6</td><td class="num pos">+5.1</td><td>食費差額支援により施設側の直接負担を整理。</td></tr>
          <tr><td>賃料</td><td class="num neg">▲96.65</td><td class="num neg">▲96.65</td><td class="num">±0.0</td><td>賃借型なので固定。CSPは不動産救済に使わない。</td></tr>
          <tr><td>光熱・本部・その他</td><td class="num neg">▲24.65</td><td class="num neg">▲23.0</td><td class="num pos">+1.65</td><td>削りすぎない。無駄だけ圧縮。</td></tr>
          <tr><td>採用・集客紹介</td><td class="num neg">▲10.1</td><td class="num neg">▲6.0</td><td class="num pos">+4.1</td><td>CSP会員・地域店舗・月次レポートが紹介導線に。</td></tr>
          <tr class="total"><td>施設安定利益</td><td class="num pos">22.35</td><td class="num pos">82.75</td><td class="num pos">+60.4</td><td>本人負担・国費を下げ、人件費を増やしても利益は残す。</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- 当月の支援金 使途別内訳 -->
  <section class="report-section">
    <div class="section-title">Breakdown · 当月の支援金 使途別内訳</div>
    <h2 class="section-h">支援金 {monthly_revenue_short} の内訳 — {period_ja}</h2>
    <div class="finance-breakdown">
{breakdown_bars}
    </div>

    <div class="finance-use">
      <div class="finance-use-title">当月の主な使い道 — {period_ja}</div>
      <p class="finance-use-text">{use_of_funds}</p>
    </div>

    <small style="margin-top:18px;color:var(--muted);font-family:var(--jp-serif);font-size:12px;display:block">
      ※ 当施設は <a href="https://carepass.tamjump.com" target="_blank" rel="noopener">Care Support Pass</a> 導入施設です。会員の方からの月額¥250 / 1口の支援金を、本人負担軽減・スタッフ配置増/賃金改善・初期費用支援・月次報告監査・予備費の5原資に分けて運用しています。
      目標支援者数 12万人 (月¥3,000万 / 年¥3.6億) は、当施設規模 (60室住宅型有料老人ホーム) に基づく設定です。
    </small>
  </section>

  <!-- MESSAGE -->
  <section class="report-section">
    <div class="section-title">From the Director</div>
    <h2 class="section-h">施設長からのメッセージ</h2>
    <div class="message-block">{message}<div class="message-author">タムジレジデンス日本橋 施設長 / 大下 甚</div></div>
  </section>

  <!-- 月ナビ -->
  <div class="report-footer">
    <div class="report-footer-in">
      <div>前月 / 翌月の活動報告へ</div>
      <div class="month-nav">
{month_nav}
      </div>
    </div>
  </div>

</main>

<footer class="site-footer">
  <div class="site-footer-in">
    <div class="site-footer-top">
      <div>
        <div class="group-mark">TAMJ.Corp<b>Care Division</b></div>
        <p style="margin-top:8px;font-size:13px;color:#fff;font-family:var(--jp-serif)">タムジレジデンス日本橋</p>
        <p>東京都中央区日本橋本町2丁目 / 医療対応型 住宅型有料老人ホーム</p>
        <p>運営: タムジcare株式会社</p>
      </div>
      <div>
        <p><a href="https://residence.tamjump.com/" style="color:rgba(246,241,232,.75)">施設サイト トップ</a></p>
        <p><a href="https://residence.tamjump.com/about.html" style="color:rgba(246,241,232,.75)">運営者情報</a></p>
        <p><a href="https://carepass.tamjump.com" target="_blank" rel="noopener" style="color:rgba(246,241,232,.75)">Care Support Pass</a></p>
      </div>
    </div>
    <div class="site-footer-bot">
      © タムジcare株式会社 / TAMJ.Corp Care Division — All Rights Reserved.
    </div>
  </div>
</footer>

</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>月次活動報告書 一覧 | タムジレジデンス日本橋</title>
<meta name="description" content="タムジレジデンス日本橋の月次活動報告書一覧。Care Support Pass を通じて毎月の活動と収支を公開しています。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Noto+Serif+JP:wght@400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/css/report.css?v=20260521a">
<style>
.list-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}}
.month-card {{
  background: var(--paper-2);
  border: 1px solid var(--line);
  text-decoration: none;
  color: var(--ink);
  display: block;
  transition: all .2s ease;
  overflow: hidden;
}}
.month-card:hover {{
  border-color: var(--ink);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(15,26,43,.08);
}}
.month-card .thumb {{
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  display: block;
  border-bottom: 1px solid var(--line);
}}
.month-card .body {{
  padding: 22px 24px 24px;
  transition: background .2s ease;
}}
.month-card:hover .body {{
  background: var(--ink);
  color: var(--paper);
}}
.month-card .period-en {{
  font-family: var(--serif);
  font-style: italic;
  font-size: 14px;
  color: var(--accent);
  margin-bottom: 6px;
  letter-spacing: .04em;
}}
.month-card:hover .body .period-en {{ color: var(--accent-2); }}
.month-card .period-ja {{
  font-family: var(--jp-serif);
  font-weight: 600;
  font-size: 18px;
  margin: 0 0 12px;
}}
.month-card .theme {{
  font-family: var(--jp-serif);
  font-size: 13px;
  color: var(--ink-2);
  line-height: 1.7;
  margin: 0 0 18px;
}}
.month-card:hover .body .theme {{ color: rgba(246,241,232,.85); }}
.month-card .meta {{
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: .12em;
  color: var(--muted);
  text-transform: uppercase;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid var(--line);
}}
.month-card:hover .body .meta {{ color: rgba(246,241,232,.5); border-top-color: rgba(255,255,255,.15); }}
.month-card .arrow {{ font-family: var(--mono); font-size: 14px; color: var(--accent); }}
.month-card:hover .body .arrow {{ color: var(--accent-2); }}

/* === 年間サマリ === */
.year-summary {{
  background: linear-gradient(135deg, var(--ink), var(--ink-2));
  color: var(--paper);
  padding: 36px 32px;
  margin-bottom: 32px;
  border: 1px solid var(--ink);
}}
.year-summary-mark {{
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--accent-2);
  margin-bottom: 12px;
}}
.year-summary-title {{
  font-family: var(--jp-serif);
  font-size: 22px;
  font-weight: 600;
  margin: 0 0 24px;
}}
.year-summary-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  border-top: 1px solid rgba(255,255,255,.15);
  padding-top: 24px;
}}
.year-summary-stat-label {{
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: rgba(246,241,232,.55);
  margin-bottom: 6px;
}}
.year-summary-stat-value {{
  font-family: var(--serif);
  font-size: 28px;
  font-weight: 600;
  color: var(--paper);
  letter-spacing: -.01em;
}}
.year-summary-stat-value small {{
  font-size: 13px;
  font-family: var(--mono);
  color: rgba(246,241,232,.55);
  margin-left: 4px;
  font-weight: 400;
}}
.year-summary-note {{
  font-family: var(--jp-serif);
  font-size: 13px;
  color: rgba(246,241,232,.7);
  margin-top: 20px;
  line-height: 1.8;
}}
</style>
</head>
<body>

<nav class="report-nav">
  <div class="report-nav-in">
    <a href="https://residence.tamjump.com/" class="report-nav-brand" style="text-decoration:none">
      <span class="mark">TAMJ.Corp</span>
      <span class="name">タムジレジデンス日本橋</span>
    </a>
    <div class="report-nav-links">
      <a href="https://residence.tamjump.com/">トップ</a>
      <a href="./">活動報告 一覧</a>
      <a href="https://carepass.tamjump.com" target="_blank" rel="noopener">Care Support Pass</a>
    </div>
  </div>
</nav>

<main class="report">

  <section class="report-hero">
    <div class="csp-mark">Monthly Care Reports — Archive</div>
    <div class="report-period">2025 / 26 ─ 12 months</div>
    <h1>月次活動報告書</h1>
    <p class="report-lede">
      タムジレジデンス日本橋は <a href="https://carepass.tamjump.com" target="_blank" rel="noopener" style="color:var(--accent);font-weight:600">Care Support Pass</a> の導入施設として、毎月の活動状況・支援者数・収支の使い道を公開しています。
    </p>
  </section>

  <!-- 年間サマリ -->
  <section class="report-section">
    <div class="year-summary">
      <div class="year-summary-mark">Year-One Summary · 2025.6 — 2026.5</div>
      <h2 class="year-summary-title">Care Support Pass 導入1周年 · 累計実績</h2>
      <div class="year-summary-grid">
        <div>
          <div class="year-summary-stat-label">累計 支援者数 (最新月)</div>
          <div class="year-summary-stat-value">{latest_supporters_str}<small>名</small></div>
        </div>
        <div>
          <div class="year-summary-stat-label">12ヶ月 累計支援額</div>
          <div class="year-summary-stat-value">¥{total_cumulative_str}</div>
        </div>
        <div>
          <div class="year-summary-stat-label">目標達成率 (12万人比)</div>
          <div class="year-summary-stat-value">{latest_pct}<small>%</small></div>
        </div>
      </div>
      <p class="year-summary-note">
        2025年6月、目標支援者 6,000名(5.0%)からスタート。2025年11月に目標 12万人 を達成、現在も成長を継続しています。
        本業売上は意図的に下げる方針 (本人負担¥215k→¥30k、軽介護度受入)。Care Support Pass の制限付き原資 (本業売上とは別枠の雑収入) を 5使途に分けて運用しています。
      </p>
    </div>
  </section>

  <section class="report-section">
    <div class="section-title">Archive</div>
    <h2 class="section-h">過去の月次活動報告</h2>

    <div class="list-grid">

{month_cards}

    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="site-footer-in">
    <div class="site-footer-top">
      <div>
        <div class="group-mark">TAMJ.Corp<b>Care Division</b></div>
        <p style="margin-top:8px;font-size:13px;color:#fff;font-family:var(--jp-serif)">タムジレジデンス日本橋</p>
        <p>東京都中央区日本橋本町2丁目 / 医療対応型 住宅型有料老人ホーム</p>
        <p>運営: タムジcare株式会社</p>
      </div>
      <div>
        <p><a href="https://residence.tamjump.com/" style="color:rgba(246,241,232,.75)">施設サイト トップ</a></p>
        <p><a href="https://residence.tamjump.com/about.html" style="color:rgba(246,241,232,.75)">運営者情報</a></p>
        <p><a href="https://carepass.tamjump.com" target="_blank" rel="noopener" style="color:rgba(246,241,232,.75)">Care Support Pass</a></p>
      </div>
    </div>
    <div class="site-footer-bot">
      © タムジcare株式会社 / TAMJ.Corp Care Division — All Rights Reserved.
    </div>
  </div>
</footer>

</body>
</html>
"""

# 月別カードのテンプレ
MONTH_CARD_TEMPLATE = """      <a href="./{period}.html" class="month-card">
        <img src="/assets/images/{hero_filename}" alt="{theme}" class="thumb" loading="lazy">
        <div class="body">
        <div class="period-en">{period_en}</div>
        <div class="period-ja">{period_ja}</div>
        <p class="theme">{theme}</p>
        <div class="meta"><span>{supporters_short} / ¥{monthly_short}</span><span class="arrow">→</span></div>
      </div>
      </a>"""

EN_MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def fmt_short_number(n):
    """100,000 → '10万', 12,000 → '1.2万', 268,000 → '26.8万'"""
    if n >= 10000:
        man = n / 10000
        if man >= 100:
            return f"{int(man)}万"
        elif man == int(man):
            return f"{int(man)}万"
        else:
            return f"{man:.1f}万"
    elif n >= 1000:
        return f"{n/1000:.1f}千"
    else:
        return str(n)


def fmt_short_money(n):
    """1,200,000 → '120万', 25,600,000 → '2,560万', 29,800,000 → '2,980万'"""
    if n >= 100000000:
        return f"{n/100000000:.1f}億"
    elif n >= 10000:
        man = n // 10000
        return f"{man:,}万"
    else:
        return f"{n:,}"


def render_kpi(kpi_list):
    parts = []
    for k in kpi_list:
        parts.append(f"""      <div class="kpi">
        <div class="kpi-label">{escape(k['label'])}</div>
        <div class="kpi-value">{escape(k['value'])}<span class="kpi-unit">{escape(k['unit'])}</span></div>
      </div>""")
    return "\n".join(parts)


def render_photos(photos):
    parts = []
    for p in photos:
        parts.append(f"""      <figure class="photo-figure">
        <img src="{escape(p['image'])}" alt="{escape(p['alt'])}" loading="lazy">
        <figcaption>{escape(p['caption'])}</figcaption>
      </figure>""")
    return "\n".join(parts)


def render_body(body_list):
    parts = []
    for item in body_list:
        heading = item[0]
        body_text = item[1] if len(item) > 1 else None
        list_items = item[2] if len(item) > 2 else None
        parts.append(f"      <h3>{escape(heading)}</h3>")
        if body_text:
            # 改行(\n)を <br> に変換するため、escape 後に置換
            text_html = escape(body_text).replace("\n", "<br>")
            parts.append(f"      <p>{text_html}</p>")
        if list_items:
            parts.append("      <ul>")
            for li in list_items:
                parts.append(f"        <li>{escape(li)}</li>")
            parts.append("      </ul>")
    return "\n".join(parts)


def render_month_nav(periods, current_idx):
    parts = []
    if current_idx > 0:
        prev_p = periods[current_idx - 1]
        parts.append(f'        <a href="./{prev_p}.html">← {prev_p}</a>')
    parts.append(f'        <a href="./">一覧へ</a>')
    if current_idx < len(periods) - 1:
        next_p = periods[current_idx + 1]
        parts.append(f'        <a href="./{next_p}.html">{next_p} →</a>')
    return "\n".join(parts)


def render_message(msg):
    return escape(msg).replace("\n", "<br>")


# =====================================================================
# 12ヶ月推移表 + 折れ線グラフ (各月レポート内)
# =====================================================================

def _short_use(fin):
    """使い道テキストを推移表用に短縮: use_of_funds_summary 優先、なければ use_of_funds から自動抽出"""
    summary = fin.get("use_of_funds_summary")
    if summary:
        return summary
    use_of_funds = fin.get("use_of_funds", "")
    if not use_of_funds:
        return ""
    text = use_of_funds.replace("\n", " ").strip()
    if "。" in text:
        head = text.split("。", 1)[0]
        if len(head) <= 50:
            return head
        for sep in ["(", "(", "、"]:
            if sep in head:
                head = head.split(sep, 1)[0]
                break
        return head[:50]
    return text[:50]


def render_timeline_rows(months, current_idx):
    """全12ヶ月分の推移表 tbody を生成。現在月の行はハイライト。"""
    parts = []
    for i, m in enumerate(months):
        fin = m["finance"]
        period = m["period"]
        year, mm = period.split("-")
        period_label = f"{year[2:]}.{int(mm)}"
        supporters_short = fmt_short_number(fin["total_supporters"])
        monthly_short = fmt_short_money(fin["monthly_revenue_jpy"])
        cumulative_short = fmt_short_money(fin["cumulative_revenue_jpy"])
        progress_pct = fin["progress_pct"]
        achieved = " achieved" if progress_pct >= 100 else ""
        current = " current" if i == current_idx else ""
        use_short = escape(_short_use(fin))
        parts.append(
            f'          <tr class="finance-row{current}{achieved}">'
            f'<td class="period-cell">{period_label}</td>'
            f'<td class="num">{supporters_short}<small>名</small></td>'
            f'<td class="num">¥{monthly_short}</td>'
            f'<td class="num">¥{cumulative_short}</td>'
            f'<td class="num pct"><span class="pct-badge">{progress_pct}%</span></td>'
            f'<td class="use">{use_short}</td>'
            f'</tr>'
        )
    return "\n".join(parts)


def render_breakdown_bars(fin):
    """当月の支援金 使途別5本バーをHTMLで生成"""
    monthly = fin["monthly_revenue_jpy"]
    breakdown = fin.get("breakdown", {})
    ratios = fin.get("breakdown_ratios", {})
    labels = {
        "support_resident":    "本人負担軽減",
        "support_staff":       "スタッフ配置増・賃金改善",
        "support_initial":     "初期費用・住み替え・家財整理支援",
        "ops_transparency":    "月次報告・監査・事務局",
        "reserve":             "予備費",
    }
    # 順序を固定
    order = ["support_resident", "support_staff", "support_initial", "ops_transparency", "reserve"]
    parts = []
    for k in order:
        amount = breakdown.get(k, 0)
        ratio = ratios.get(k, 0)
        pct = round(ratio * 100, 1) if ratio else 0
        label = labels[k]
        amount_str = f"¥{fmt_short_money(amount)}"
        parts.append(
            f'      <div class="bd-row bd-{k}">'
            f'<div class="bd-row-head">'
            f'<span class="bd-label">{escape(label)}</span>'
            f'<span class="bd-amount">{amount_str}<small>({pct}%)</small></span>'
            f'</div>'
            f'<div class="bd-bar-bg"><div class="bd-bar-fill" style="width:{pct}%"></div></div>'
            f'</div>'
        )
    return "\n".join(parts)



    """全12ヶ月分の推移表 tbody を生成。現在月の行はハイライト。"""
    parts = []
    for i, m in enumerate(months):
        fin = m["finance"]
        period = m["period"]
        year, mm = period.split("-")
        period_label = f"{year[2:]}.{int(mm)}"
        supporters_short = fmt_short_number(fin["total_supporters"])
        monthly_short = fmt_short_money(fin["monthly_revenue_jpy"])
        cumulative_short = fmt_short_money(fin["cumulative_revenue_jpy"])
        progress_pct = fin["progress_pct"]
        achieved = " achieved" if progress_pct >= 100 else ""
        current = " current" if i == current_idx else ""
        use_short = escape(_short_use(fin))
        parts.append(
            f'          <tr class="finance-row{current}{achieved}">'
            f'<td class="period-cell">{period_label}</td>'
            f'<td class="num">{supporters_short}<small>名</small></td>'
            f'<td class="num">¥{monthly_short}</td>'
            f'<td class="num">¥{cumulative_short}</td>'
            f'<td class="num pct"><span class="pct-badge">{progress_pct}%</span></td>'
            f'<td class="use">{use_short}</td>'
            f'</tr>'
        )
    return "\n".join(parts)


# SVGチャートのレイアウト定数 (viewBox 座標)
# ※ CSS で width:100% にスケール。viewBox 比率は 4:1.6 ぐらい。
CHART_W = 640
CHART_H = 260
CHART_PAD_L = 56   # 左マージン(Y軸ラベル用)
CHART_PAD_R = 16
CHART_PAD_T = 18
CHART_PAD_B = 36   # 下マージン(X軸ラベル用)


def _chart_x(i, n):
    """i番目の月の X座標 (0始まり, nは全月数)"""
    if n <= 1:
        return CHART_PAD_L
    inner_w = CHART_W - CHART_PAD_L - CHART_PAD_R
    return CHART_PAD_L + (inner_w * i / (n - 1))


def _chart_y(v, y_max, y_min=0):
    """値 v を Y座標に変換"""
    if y_max == y_min:
        return CHART_H - CHART_PAD_B
    inner_h = CHART_H - CHART_PAD_T - CHART_PAD_B
    return CHART_H - CHART_PAD_B - (inner_h * (v - y_min) / (y_max - y_min))


def render_line_chart(months, current_idx, *, value_key, y_max, y_label_fn,
                      target=None, target_label=None, accent="var(--accent)"):
    """折れ線グラフのSVGを生成。
    months: データ配列
    value_key: 'total_supporters' か 'cumulative_revenue_jpy' か 'monthly_revenue_jpy'
    y_max: Y軸最大値 (グリッドはこの値を5等分)
    y_label_fn: Y軸ラベル整形関数 (例: lambda v: f"{v/10000:.0f}万")
    target: 目標値ライン (任意)
    target_label: 目標ラベル
    accent: 線色のCSS変数
    """
    n = len(months)
    values = [m["finance"][value_key] for m in months]

    # ポリライン用点列
    points = []
    for i, v in enumerate(values):
        x = _chart_x(i, n)
        y = _chart_y(v, y_max)
        points.append((x, y))

    # 塗り(area)用パス
    area_d = (
        f"M {points[0][0]:.1f},{CHART_H - CHART_PAD_B:.1f} "
        + " ".join(f"L {x:.1f},{y:.1f}" for x, y in points)
        + f" L {points[-1][0]:.1f},{CHART_H - CHART_PAD_B:.1f} Z"
    )
    # 折れ線
    line_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)

    # 目標ライン
    target_elements = ""
    if target is not None and target <= y_max:
        ty = _chart_y(target, y_max)
        target_elements = (
            f'<line class="chart-target-line" x1="{CHART_PAD_L}" y1="{ty:.1f}" '
            f'x2="{CHART_W - CHART_PAD_R}" y2="{ty:.1f}"/>'
            f'<text class="chart-target-label" x="{CHART_W - CHART_PAD_R - 6}" y="{ty - 6:.1f}" '
            f'text-anchor="end">{escape(target_label or "")}</text>'
        )

    # Y軸グリッド + ラベル (4本)
    grid_lines = []
    y_labels = []
    for step in range(0, 5):
        v = y_max * step / 4
        gy = _chart_y(v, y_max)
        grid_lines.append(
            f'<line class="chart-grid" x1="{CHART_PAD_L}" y1="{gy:.1f}" '
            f'x2="{CHART_W - CHART_PAD_R}" y2="{gy:.1f}"/>'
        )
        y_labels.append(
            f'<text class="chart-y-label" x="{CHART_PAD_L - 8}" y="{gy + 4:.1f}" '
            f'text-anchor="end">{escape(y_label_fn(v))}</text>'
        )

    # X軸ラベル (全月ラベル)
    x_labels = []
    for i, m in enumerate(months):
        x = _chart_x(i, n)
        year, mm = m["period"].split("-")
        label = f"{int(mm)}月"
        # 6月だけ年も足す
        if int(mm) == 6 or i == 0:
            label = f"'{year[2:]}.{int(mm)}"
        x_labels.append(
            f'<text class="chart-x-label" x="{x:.1f}" y="{CHART_H - 14}" '
            f'text-anchor="middle">{label}</text>'
        )

    # データ点 (現在月は大きい円, それ以外は小さい円)
    dots = []
    for i, (x, y) in enumerate(points):
        if i == current_idx:
            dots.append(
                f'<circle class="chart-dot-current" cx="{x:.1f}" cy="{y:.1f}" r="6"/>'
                f'<circle class="chart-dot-current-ring" cx="{x:.1f}" cy="{y:.1f}" r="10"/>'
            )
        else:
            dots.append(f'<circle class="chart-dot" cx="{x:.1f}" cy="{y:.1f}" r="3.5"/>')

    # 現在月の縦点線
    cur_x = points[current_idx][0]
    current_marker = (
        f'<line class="chart-current-vline" x1="{cur_x:.1f}" y1="{CHART_PAD_T}" '
        f'x2="{cur_x:.1f}" y2="{CHART_H - CHART_PAD_B}"/>'
    )

    # 現在月の値ラベル (吹き出し風)
    cur_v = values[current_idx]
    cur_y = points[current_idx][1]
    cur_label_text = y_label_fn(cur_v)
    # 上に余裕があれば上、なければ下
    label_above = cur_y > CHART_PAD_T + 28
    cur_label_y = cur_y - 14 if label_above else cur_y + 22
    current_label = (
        f'<text class="chart-current-label" x="{cur_x:.1f}" y="{cur_label_y:.1f}" '
        f'text-anchor="middle">{escape(cur_label_text)}</text>'
    )

    svg = (
        f'<svg class="chart-svg" viewBox="0 0 {CHART_W} {CHART_H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="月次推移グラフ">'
        + "".join(grid_lines)
        + (
            f'<path class="chart-area" d="{area_d}" fill="url(#chart-grad-{value_key})"/>'
            f'<defs><linearGradient id="chart-grad-{value_key}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" class="chart-grad-from"/>'
            f'<stop offset="100%" class="chart-grad-to"/>'
            f'</linearGradient></defs>'
        )
        + target_elements
        + current_marker
        + f'<path class="chart-line" d="{line_d}" fill="none"/>'
        + "".join(dots)
        + "".join(y_labels)
        + "".join(x_labels)
        + current_label
        + '</svg>'
    )
    return svg


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        months = json.load(f)
    periods = [m["period"] for m in months]

    # --- 各月のHTML生成 ---
    for idx, m in enumerate(months):
        period = m["period"]
        year, mm = period.split("-")
        period_en = f"{EN_MONTHS[mm]} {year}"
        period_ja = m["period_ja"]
        theme = m["theme"]
        hero_image = m["hero_image"]
        og_image_abs = hero_image.replace("../", "/")
        hero_image_alt = m.get("hero_image_alt", "")
        hero_caption = m["hero_caption"]
        lede = m["lede"]
        kpi_blocks = render_kpi(m["kpi"])
        photo_blocks = render_photos(m["photos"])
        body_blocks = render_body(m["body"])
        message = render_message(m["message"])

        fin = m["finance"]
        total_supporters = fin["total_supporters"]
        monthly_revenue = fin["monthly_revenue_jpy"]
        cumulative_revenue = fin["cumulative_revenue_jpy"]
        progress_pct = fin["progress_pct"]
        use_of_funds = fin.get("use_of_funds", "")

        total_supporters_str = f"{total_supporters:,}"
        monthly_revenue_str = f"{monthly_revenue:,}"
        cumulative_revenue_str = f"{cumulative_revenue:,}"

        # メーターバーは0-100%でクリップ、超過時は別クラスで色変え
        if progress_pct >= 100:
            progress_bar_pct = 100
            meter_class = " achieved"
        else:
            progress_bar_pct = progress_pct
            meter_class = ""

        # 推移表
        timeline_rows = render_timeline_rows(months, idx)

        # グラフ1: 支援者数 (目標12万ライン入り)
        # Y軸最大値は データに合わせる
        max_supporters_in_data = max(mo["finance"]["total_supporters"] for mo in months)
        y_max_supporters = max(150000, int((max_supporters_in_data * 1.1) // 25000 + 1) * 25000)
        chart_supporters_svg = render_line_chart(
            months, idx,
            value_key="total_supporters",
            y_max=y_max_supporters,
            y_label_fn=lambda v: f"{int(v/10000)}万" if v >= 10000 else f"{int(v):,}",
            target=TARGET_SUPPORTERS,
            target_label="目標 12万人",
        )

        # グラフ2: 累計支援額
        max_cum_in_data = max(mo["finance"]["cumulative_revenue_jpy"] for mo in months)
        y_max_cum = max(400000000, int((max_cum_in_data * 1.1) // 50000000 + 1) * 50000000)
        chart_cumulative_svg = render_line_chart(
            months, idx,
            value_key="cumulative_revenue_jpy",
            y_max=y_max_cum,
            y_label_fn=lambda v: f"{int(v/100000000)}億" if v >= 100000000 else f"{int(v/10000000)*1000}万",
        )

        # 使途別5本バー
        breakdown_bars = render_breakdown_bars(fin)
        monthly_revenue_short = f"¥{fmt_short_money(monthly_revenue)}"

        month_nav = render_month_nav(periods, idx)

        html = REPORT_TEMPLATE.format(
            period=period,
            period_en=period_en,
            period_ja=period_ja,
            theme=escape(theme),
            hero_image=escape(hero_image),
            og_image_abs=escape(og_image_abs),
            hero_image_alt=escape(hero_image_alt),
            hero_caption=escape(hero_caption),
            lede=escape(lede),
            kpi_blocks=kpi_blocks,
            photo_blocks=photo_blocks,
            body_blocks=body_blocks,
            message=message,
            timeline_rows=timeline_rows,
            chart_supporters_svg=chart_supporters_svg,
            chart_cumulative_svg=chart_cumulative_svg,
            breakdown_bars=breakdown_bars,
            monthly_revenue_short=monthly_revenue_short,
            use_of_funds=escape(use_of_funds),
            month_nav=month_nav,
        )
        out_path = os.path.join(OUT_DIR, f"{period}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  written: {out_path}")

    # --- index.html の生成 (新しい順) ---
    cards = []
    for m in reversed(months):
        period = m["period"]
        year, mm = period.split("-")
        period_en = f"{EN_MONTHS[mm]} {year}"
        period_ja = m["period_ja"]
        theme = m["theme"]
        hero_filename = m["hero_image"].split("/")[-1]
        supporters_short = f"{fmt_short_number(m['finance']['total_supporters'])}名"
        monthly_short = fmt_short_money(m["finance"]["monthly_revenue_jpy"])
        cards.append(MONTH_CARD_TEMPLATE.format(
            period=period,
            period_en=period_en,
            period_ja=period_ja,
            theme=escape(theme),
            hero_filename=hero_filename,
            supporters_short=supporters_short,
            monthly_short=monthly_short,
        ))

    latest = months[-1]
    latest_supporters = latest["finance"]["total_supporters"]
    total_cumulative = latest["finance"]["cumulative_revenue_jpy"]
    latest_pct = latest["finance"]["progress_pct"]

    index_html = INDEX_TEMPLATE.format(
        month_cards="\n\n".join(cards),
        latest_supporters_str=f"{latest_supporters:,}",
        total_cumulative_str=f"{total_cumulative:,}",
        latest_pct=latest_pct,
    )
    index_path = os.path.join(OUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  written: {index_path}")

    print(f"\nGenerated {len(months)} monthly reports + index.html.")


if __name__ == "__main__":
    main()
