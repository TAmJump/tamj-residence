#!/usr/bin/env python3
"""
_data.json の finance ブロックと CSP関連の本文セクションを、
資料 (project_tortoise_rebuild_v14) のPL構造に従って書き直す。

設計:
- スケール: 1棟 60室、目標支援者 12万人/月、月¥3,000万、年¥3.6億
- CSP原資は「本業売上とは別枠」「雑収入扱い」
- 5使途内訳: 本人負担軽減 45% / スタッフ強化 30% / 初期支援 10% / 運営透明性 10% / 予備費 5%
- 介護度の低い層に意図的に寄せる (要支援〜要介護1・2)
- スタッフは削らず増やす (人数増+賃金改善)
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "_data.json")

# === 月別データ ===
# (period, total_supporters, monthly_revenue_jpy)
# 目標 12万人 / 月¥3,000万 を 2025-11に達成、その後微増
MONTHLY = [
    ("2025-06",   6000),   # 導入初月 5.0%
    ("2025-07",  18000),   # 15.0%
    ("2025-08",  42000),   # 35.0%
    ("2025-09",  72000),   # 60.0%
    ("2025-10", 102000),   # 85.0%
    ("2025-11", 123000),   # 102.5% ★達成
    ("2025-12", 128000),
    ("2026-01", 132000),
    ("2026-02", 135000),
    ("2026-03", 138000),
    ("2026-04", 141000),
    ("2026-05", 144000),
]

TARGET_SUPPORTERS = 120000   # 目標
TARGET_MONTHLY = 30000000    # 目標月¥3,000万
UNIT_PRICE = 250             # 1人250円/月 (60室・250円/口 を踏襲)

# 使途別配分 (達成月以降の標準配分)
ALLOCATION_RATIOS = {
    "support_resident":    0.45,  # 本人負担軽減
    "support_staff":       0.30,  # スタッフ配置増・賃金改善
    "support_initial":     0.10,  # 初期費用・住み替え・家財整理
    "ops_transparency":    0.10,  # 月次報告・監査・事務局
    "reserve":             0.05,  # 予備費
}

# 使途ラベル
ALLOCATION_LABELS = {
    "support_resident":    "本人負担軽減原資",
    "support_staff":       "スタッフ配置増・賃金改善原資",
    "support_initial":     "初期費用・住み替え・家財整理支援",
    "ops_transparency":    "月次報告・監査・事務局",
    "reserve":             "予備費",
}

# 月別の追加注釈 (each month's "use_of_funds" の主要内容)
# = 何に重点的に使ったか
MONTHLY_USE_OF_FUNDS = {
    "2025-06": {
        "main": "導入初月。本月の支援金は翌月以降の本人負担軽減・スタッフ強化原資として留保。施設PLは本業売上の落ち込み(本人負担¥215k→¥100k への段階引下げ)を予備費でカバー。",
        "summary": "導入初月。原資留保期",
    },
    "2025-07": {
        "main": "本人負担軽減原資の本格運用開始。入居者本人徴収を ¥215,000/月 → ¥150,000/月 に減額(月¥65,000 × 9名 = ¥585,000の負担軽減)。スタッフ強化原資から見守り時間の確保(夜間1名増員)。",
        "summary": "本人負担¥215k→¥150kへ第一段階引下げ",
    },
    "2025-08": {
        "main": "スタッフ強化原資から夏季手当 (¥30,000 × 14名)、夏季電気代の入居者負担を施設側でカバー。本人負担減額継続。要支援〜要介護1・2の方の新規入居受付開始 (国費依存を下げる方針)。",
        "summary": "スタッフ夏季手当 + 軽介護度受入開始",
    },
    "2025-09": {
        "main": "スタッフ強化原資から看護師1名常勤雇用 (年俸¥4,800,000)、本人負担軽減原資の累計が ¥3,450万に到達。敬老月特別: ご家族の祝膳費用も施設負担化。",
        "summary": "看護師常勤化 (3→4名)、敬老月家族招待",
    },
    "2025-10": {
        "main": "スタッフ強化原資から理学療法士1名常駐化 (月¥380,000)。初期費用支援原資の運用開始: 入居者の家財整理・住み替え支援費を施設負担化。月1回までの外出費 (介護タクシー代) を本人負担軽減原資から拠出。",
        "summary": "リハ常駐化 + 外出支援拡充",
    },
    "2025-11": {
        "main": "★ 目標支援者 12万人 達成 (累計123,000名、達成率102.5%)。本人負担を更に ¥150,000 → ¥30,000/月 へ引下げ (年金で払える水準)。スタッフ全員賞与¥50,000支給。資料規定の標準配分 (本人負担軽減45% / スタッフ強化30% / 初期支援10% / 運営透明性10% / 予備費5%) を開始。",
        "summary": "★目標達成、本人負担¥150k→¥30k完全実施",
    },
    "2025-12": {
        "main": "資料規定の標準5原資配分が定常運転に移行。年末年始24時間医療体制を本人負担軽減原資でカバー (従来¥18,000/6日 → 完全無料)。透明性原資から第三者監査の準備開始 (来月の年次活動報告監査に向けて)。",
        "summary": "年末年始医療体制を本人負担軽減でカバー",
    },
    "2026-01": {
        "main": "スタッフ配置数 70名 → 82名 (+12名) 体制が安定稼働。賃金原資 月¥800/人 のベース改善継続。初期支援原資から新規入居者2名分の家財整理・引越支援費を全額施設負担。",
        "summary": "スタッフ70→82名 (+12) 体制が安定稼働",
    },
    "2026-02": {
        "main": "嚥下対応個別調整食の追加料金 (従来 月¥15,000) を本人負担軽減原資で完全無償化。透明性原資から月次活動報告の体制整備 (写真撮影・栄養士監修・施設長記述の標準化)。",
        "summary": "嚥下対応食 完全無償化",
    },
    "2026-03": {
        "main": "ご家族通信費補助 (月¥2,000) を本人負担軽減原資から開始。スタッフ強化原資の運用が定常化、1人あたり作業密度は前年比 22% 低下 (見守り時間が実測+3.5時間/日に増加、事故報告ゼロを継続)。",
        "summary": "通信費補助開始、作業密度22%低減",
    },
    "2026-04": {
        "main": "月1回までの介護タクシー外出費 (月¥8,000 × 22名 = ¥176,000) を本人負担軽減原資で施設負担化。資料規定の「販管費・紹介料依存を下げる」方針通り、今月の新規入居者2名は全てCSP会員からの紹介経由 (採用紹介料ゼロ)。",
        "summary": "外出費施設負担化、紹介料ゼロ達成",
    },
    "2026-05": {
        "main": "★ Care Support Pass 導入1周年。スタッフ強化原資から初年度昇給+10% (基本給+月¥30,000)、初期費用支援原資から新規入居者の入居一時金 (¥500,000) を実質免除。本人負担¥215k→¥30k、要介護度1・2を含む軽介護度者中心の運営体制、スタッフ82名・賃金平均384万円/年への引上げ — すべて達成。",
        "summary": "★1周年: 昇給+10%、入居一時金実質免除",
    },
}


def fmt_yen_man(yen):
    """整数円 → '¥1,200万' / '¥1.2億' 形式"""
    if yen >= 100_000_000:
        return f"¥{yen/100_000_000:.1f}億"
    elif yen >= 10000:
        return f"¥{yen//10000:,}万"
    else:
        return f"¥{yen:,}"


def build_finance(period, total_supporters, cumulative_so_far):
    """月別の finance ブロックを生成"""
    monthly_revenue = total_supporters * UNIT_PRICE  # 1人250円/月
    cumulative = cumulative_so_far + monthly_revenue
    progress_pct = round(total_supporters / TARGET_SUPPORTERS * 100, 1)

    # 使途内訳: 達成前は本人負担軽減を優先的に厚く
    if total_supporters >= TARGET_SUPPORTERS:
        # 達成後: 資料の標準配分
        ratios = ALLOCATION_RATIOS
    else:
        # 達成前: 本人負担軽減と運営透明性を厚く、初期支援と予備費を後回し
        # 累計が小さいうちはまず本人負担と運営透明性に集中
        if total_supporters < 30000:
            ratios = {"support_resident": 0.55, "support_staff": 0.20,
                      "support_initial": 0.05, "ops_transparency": 0.15, "reserve": 0.05}
        elif total_supporters < 70000:
            ratios = {"support_resident": 0.50, "support_staff": 0.25,
                      "support_initial": 0.08, "ops_transparency": 0.12, "reserve": 0.05}
        else:
            ratios = {"support_resident": 0.47, "support_staff": 0.28,
                      "support_initial": 0.10, "ops_transparency": 0.10, "reserve": 0.05}

    breakdown = {
        k: round(monthly_revenue * v) for k, v in ratios.items()
    }
    # 端数調整: 合計が monthly_revenue と一致するように予備費で調整
    diff = monthly_revenue - sum(breakdown.values())
    breakdown["reserve"] += diff

    use = MONTHLY_USE_OF_FUNDS[period]
    return {
        "total_supporters": total_supporters,
        "monthly_revenue_jpy": monthly_revenue,
        "cumulative_revenue_jpy": cumulative,
        "progress_pct": progress_pct,
        "use_of_funds": use["main"],
        "use_of_funds_summary": use["summary"],
        "breakdown": breakdown,  # 5使途内訳 (円)
        "breakdown_ratios": ratios,
    }


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        months = json.load(f)

    # 既存データを period でインデックス
    months_by_period = {m["period"]: m for m in months}

    cumulative = 0
    for period, total_supporters in MONTHLY:
        m = months_by_period[period]
        cumulative_new = cumulative + total_supporters * UNIT_PRICE
        m["finance"] = build_finance(period, total_supporters, cumulative)
        cumulative = cumulative_new

    # period 順を維持して書き戻し
    months_out = [months_by_period[p] for p, _ in MONTHLY]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(months_out, f, ensure_ascii=False, indent=2)

    # 確認用にスケールサマリーを出力
    print("=== 新しい収支構造 ===")
    cumulative = 0
    for period, total_supporters in MONTHLY:
        monthly = total_supporters * UNIT_PRICE
        cumulative += monthly
        pct = total_supporters / TARGET_SUPPORTERS * 100
        print(f"  {period}: 支援者 {total_supporters:>7,}名 / 月 {fmt_yen_man(monthly):>8} / 累計 {fmt_yen_man(cumulative):>8} / {pct:5.1f}%")
    print(f"\n12ヶ月累計支援額: {fmt_yen_man(cumulative)}")
    print(f"安定期 月額収入: {fmt_yen_man(144000 * UNIT_PRICE)} = 目標 {fmt_yen_man(TARGET_MONTHLY)} の {144000/120000*100:.0f}%")


if __name__ == "__main__":
    main()
