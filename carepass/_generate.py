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

# 目標値 (施設プロフィール定数)
TARGET_SUPPORTERS = 250000
TARGET_MONTHLY_REVENUE = 25000000

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
<link rel="stylesheet" href="./assets/css/report.css?v=20260520b">
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
    <h2 class="section-h">支援者数 と 収支報告</h2>

    <!-- 達成度メーター -->
    <div class="finance-meter">
      <div class="finance-meter-head">
        <div class="finance-meter-label">支援者数 / 目標 25万人</div>
        <div class="finance-meter-pct">{progress_pct}%</div>
      </div>
      <div class="finance-meter-bar">
        <div class="finance-meter-fill{meter_class}" style="width:{progress_bar_pct}%"></div>
        <div class="finance-meter-target"></div>
      </div>
      <div class="finance-meter-foot">
        <span>0</span>
        <span class="finance-meter-target-label">目標 250,000名 / 月¥25,000,000</span>
        <span>{progress_pct}%</span>
      </div>
    </div>

    <!-- 主要指標 -->
    <div class="finance-stats">
      <div class="finance-stat">
        <div class="finance-stat-label">当月 支援者数</div>
        <div class="finance-stat-value">{total_supporters_str}<small>名</small></div>
      </div>
      <div class="finance-stat">
        <div class="finance-stat-label">当月 支援額</div>
        <div class="finance-stat-value">¥{monthly_revenue_str}</div>
      </div>
      <div class="finance-stat">
        <div class="finance-stat-label">累計 支援額</div>
        <div class="finance-stat-value">¥{cumulative_revenue_str}</div>
      </div>
    </div>

    <!-- 使い道 -->
    <div class="finance-use">
      <div class="finance-use-title">支援金の使い道 — {period_ja}</div>
      <p class="finance-use-text">{use_of_funds}</p>
    </div>

    <small style="margin-top:18px;color:var(--muted);font-family:var(--jp-serif);font-size:12px;display:block">
      ※ 当施設は <a href="https://carepass.tamjump.com" target="_blank" rel="noopener">Care Support Pass</a> 導入施設です。会員の方からの月額¥100の支援金を、入居者・スタッフ・ご家族への還元施策に活用しています。
      目標支援者数 25万人(月¥2,500万)は、当施設の規模(60室住宅型有料老人ホーム + 9室宿泊型デイサービス)に基づく設定です。
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
<link rel="stylesheet" href="./assets/css/report.css?v=20260520b">
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
          <div class="year-summary-stat-label">目標達成率 (25万人比)</div>
          <div class="year-summary-stat-value">{latest_pct}<small>%</small></div>
        </div>
      </div>
      <p class="year-summary-note">
        2025年6月、目標支援者 12,000名(4.8%)からスタート。2025年11月に目標 25万人 を達成、現在も成長を継続しています。
        各月の収支の使い道は、それぞれの活動報告ページ内「Care Support Pass · Finance」セクションに記載しています。
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
            total_supporters_str=total_supporters_str,
            monthly_revenue_str=monthly_revenue_str,
            cumulative_revenue_str=cumulative_revenue_str,
            progress_pct=progress_pct,
            progress_bar_pct=progress_bar_pct,
            meter_class=meter_class,
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
