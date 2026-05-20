#!/usr/bin/env python3
"""
タムジレジデンス日本橋 / Care Support Pass 月次活動報告書 一括生成スクリプト
_data.json を読み込み、12ヶ月分のHTMLを出力する。
"""

import json
import os
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "_data.json")
OUT_DIR = BASE_DIR

# ===== テンプレート =====

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Noto+Serif+JP:wght@400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/css/report.css?v=20260520">
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
    <figure class="photo-figure">
      <div class="photo-placeholder">{hero_image_label}<br>(画像準備中)</div>
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

  <!-- FINANCE / 支援者の状況 -->
  <section class="report-section">
    <div class="section-title">Care Support Pass</div>
    <h2 class="section-h">支援者の状況 (累計)</h2>
    <table class="finance-tbl">
      <thead>
        <tr><th>項目</th><th style="text-align:right">数値</th></tr>
      </thead>
      <tbody>
        <tr><td>当施設を支援している会員数</td><td class="num">{total_supporters} 名</td></tr>
        <tr><td>累計の支援額 ({period_ja} 末まで)</td><td class="num">¥{total_paid_jpy_str}</td></tr>
        <tr class="total"><td>(参考) 月100円 × {months_count} ヶ月分</td><td class="num">¥{total_paid_jpy_str}</td></tr>
      </tbody>
    </table>
    <small style="margin-top:14px;color:var(--muted);font-family:var(--jp-serif);font-size:12px">
      ※ 当施設は <a href="https://carepass.tamjump.com" target="_blank" rel="noopener">Care Support Pass</a> 導入施設です。会員の方からの月額¥100の支援金を、施設運営の透明性向上と入居者の生活支援に活用しています。
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
      <div>
        前月 / 翌月の活動報告へ
      </div>
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

# 月の英語名 (Cormorant Garamond で美しく見せる用)
EN_MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}

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
        <div class="photo-placeholder">{escape(p['label'])}<br>(画像準備中)</div>
        <figcaption>{escape(p['caption'])}</figcaption>
      </figure>""")
    return "\n".join(parts)


def render_body(body_list):
    """body_list: [[heading, paragraph_or_None, list_items_or_None?], ...]"""
    parts = []
    for item in body_list:
        heading = item[0]
        # 各エントリは [heading, body_text] か [heading, body_text_or_None, [list_items]]
        body_text = item[1] if len(item) > 1 else None
        list_items = item[2] if len(item) > 2 else None
        parts.append(f"      <h3>{escape(heading)}</h3>")
        if body_text:
            parts.append(f"      <p>{escape(body_text)}</p>")
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
    # 改行は <br> に変換 (white-space: pre-line でも対応されているが、念のため両対応)
    return escape(msg).replace("\n", "<br>")


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        months = json.load(f)
    periods = [m["period"] for m in months]

    for idx, m in enumerate(months):
        period = m["period"]               # 2025-06
        year, mm = period.split("-")
        period_en = f"{EN_MONTHS[mm]} {year}"
        period_ja = m["period_ja"]
        theme = m["theme"]
        hero_image_label = m["hero_image_label"]
        hero_caption = m["hero_caption"]
        lede = m["lede"]
        kpi_blocks = render_kpi(m["kpi"])
        photo_blocks = render_photos(m["photos"])
        body_blocks = render_body(m["body"])
        message = render_message(m["message"])
        total_supporters = m["finance"]["total_supporters"]
        total_paid_jpy = m["finance"]["total_paid_jpy"]
        total_paid_jpy_str = f"{total_paid_jpy:,}"
        months_count = idx + 1
        month_nav = render_month_nav(periods, idx)

        html = REPORT_TEMPLATE.format(
            period=period,
            period_en=period_en,
            period_ja=period_ja,
            theme=escape(theme),
            hero_image_label=escape(hero_image_label),
            hero_caption=escape(hero_caption),
            lede=escape(lede),
            kpi_blocks=kpi_blocks,
            photo_blocks=photo_blocks,
            body_blocks=body_blocks,
            message=message,
            total_supporters=total_supporters,
            total_paid_jpy_str=total_paid_jpy_str,
            months_count=months_count,
            month_nav=month_nav,
        )
        out_path = os.path.join(OUT_DIR, f"{period}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  written: {out_path}")

    print(f"\nGenerated {len(months)} monthly reports.")


if __name__ == "__main__":
    main()
