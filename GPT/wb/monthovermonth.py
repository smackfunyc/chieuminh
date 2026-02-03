#!/usr/bin/env python3
"""
Monthly MoM GPT usage analysis (Dec vs Jan style) with exclusions.

Usage:
  python gpt_mom.py --prev "m2.GPT Analysis December2025.xlsx" --cur "RRA OpenAI Workspace monthly gpt report 2026-01-01.xlsx" --out "mom_summary.xlsx"

Dependencies:
  pip install pandas openpyxl
"""

import argparse
import re
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd


REQUIRED_COLS = {"gpt_name", "config_type", "is_active", "messages_workspace", "unique_messagers_workspace"}

EXCLUDE_PATTERNS = [
    r"smart[\s\-_]*pack",  # smart pack, smart-pack, smart_pack
    r"candidate[\s\-_]*letter[\s\-_]*generator",
    r"\bCLG\b",
    r"psychometric",
    r"psychometrics",
    r"consultant[\s\-_]*finder",
    r"candidate[\s\-_]*archetype",
    r"candidate[\s\-_]*archetypes",
    r"prompt[\s\-_]*coach",
    r"person[-_ ]sp[-_ ]",   # person-sp-*
    r"company[-_ ]sp[-_ ]",  # company-sp-*
    r"project[-_ ]sp[-_ ]",  # project-sp-*
]
EXCLUDE_REGEX = re.compile("|".join(EXCLUDE_PATTERNS), flags=re.IGNORECASE)


@dataclass
class MonthData:
    label: str
    df: pd.DataFrame


def find_data_sheet(path: str, explicit_sheet: Optional[str] = None) -> str:
    xl = pd.ExcelFile(path)
    if explicit_sheet:
        return explicit_sheet

    for s in xl.sheet_names:
        hdr = pd.read_excel(path, sheet_name=s, nrows=0)
        cols = set([c.strip() if isinstance(c, str) else c for c in hdr.columns])
        if REQUIRED_COLS.issubset(cols):
            return s

    raise ValueError(f"Could not find a sheet with required columns in: {path}")


def load_month(path: str, sheet: Optional[str] = None) -> MonthData:
    sheet_name = find_data_sheet(path, sheet)
    df = pd.read_excel(path, sheet_name=sheet_name)

    for col in ["period_start", "period_end", "first_day_active_in_period", "last_day_active_in_period"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in ["messages_workspace", "unique_messagers_workspace", "is_active"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["gpt_name"] = df["gpt_name"].astype("string")
    df["gpt_name_clean"] = df["gpt_name"].str.strip().fillna("")

    if "period_start" in df.columns and df["period_start"].notna().any():
        label = df["period_start"].dropna().iloc[0].strftime("%Y-%m")
    else:
        label = "unknown"

    return MonthData(label=label, df=df)


def apply_exclusions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["_kw_excluded"] = out["gpt_name_clean"].fillna("").str.contains(EXCLUDE_REGEX, na=False)

    if "Exclude" in out.columns:
        out["_flag_excluded"] = out["Exclude"].astype("string").str.lower().fillna("").ne("keep")
    else:
        out["_flag_excluded"] = False

    out["_excluded"] = out["_kw_excluded"] | out["_flag_excluded"]
    return out


def month_metrics(df: pd.DataFrame) -> dict:
    d = df.copy()

    live = d[d["config_type"].astype("string").str.lower() == "live"]
    live_used = live[live["messages_workspace"] > 0]

    all_used = d[d["messages_workspace"] > 0]

    def top_share(x: pd.DataFrame, n: int) -> float:
        total = x["messages_workspace"].sum()
        if total <= 0:
            return 0.0
        return float(x.sort_values("messages_workspace", ascending=False)["messages_workspace"].head(n).sum() / total)

    return {
        "rows_total": int(len(d)),
        "gpts_named": int((d["gpt_name_clean"] != "").sum()),
        "gpts_live_named": int(((d["gpt_name_clean"] != "") & (d["config_type"].astype("string").str.lower() == "live")).sum()),
        "gpts_draft_named": int(((d["gpt_name_clean"] != "") & (d["config_type"].astype("string").str.lower() == "draft")).sum()),
        "messages_total": int(d["messages_workspace"].sum()),
        "live_messages_total": int(live["messages_workspace"].sum()),
        "active_gpts_any": int(len(all_used)),
        "active_live_gpts": int(len(live_used)),
        "live_activation_rate": float(len(live_used) / max(1, (live["gpt_name_clean"] != "").sum())),
        "top10_live_share": top_share(live_used, 10),
        "top5_live_share": top_share(live_used, 5),
    }


def aggregate_live(df: pd.DataFrame) -> pd.DataFrame:
    live = df[df["config_type"].astype("string").str.lower() == "live"].copy()
    g = (
        live.groupby("gpt_name_clean", dropna=False)[["messages_workspace", "unique_messagers_workspace"]]
        .sum()
        .reset_index()
    )
    g = g[g["gpt_name_clean"] != ""]
    return g


def mom_changes(prev_df: pd.DataFrame, cur_df: pd.DataFrame) -> pd.DataFrame:
    prev = aggregate_live(prev_df).rename(
        columns={"messages_workspace": "messages_prev", "unique_messagers_workspace": "unique_prev"}
    )
    cur = aggregate_live(cur_df).rename(
        columns={"messages_workspace": "messages_cur", "unique_messagers_workspace": "unique_cur"}
    )

    m = prev.merge(cur, on="gpt_name_clean", how="outer").fillna(0)
    m["delta_messages"] = m["messages_cur"] - m["messages_prev"]
    m["status"] = np.select(
        [
            (m["messages_prev"] > 0) & (m["messages_cur"] > 0),
            (m["messages_prev"] == 0) & (m["messages_cur"] > 0),
            (m["messages_prev"] > 0) & (m["messages_cur"] == 0),
        ],
        ["continuing", "new_in_cur", "dropped_in_cur"],
        default="inactive_both",
    )
    return m.sort_values("delta_messages", ascending=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prev", required=True, help="Previous month xlsx path")
    ap.add_argument("--cur", required=True, help="Current month xlsx path")
    ap.add_argument("--prev-sheet", default=None, help="Optional explicit sheet name for prev")
    ap.add_argument("--cur-sheet", default=None, help="Optional explicit sheet name for cur")
    ap.add_argument("--out", default=None, help="Optional output Excel path")
    args = ap.parse_args()

    prev = load_month(args.prev, args.prev_sheet)
    cur = load_month(args.cur, args.cur_sheet)

    prev_f = apply_exclusions(prev.df)
    cur_f = apply_exclusions(cur.df)

    prev_inc = prev_f[~prev_f["_excluded"]].copy()
    cur_inc = cur_f[~cur_f["_excluded"]].copy()

    exc_prev_msgs = int(prev_f.loc[prev_f["_excluded"], "messages_workspace"].sum())
    exc_cur_msgs = int(cur_f.loc[cur_f["_excluded"], "messages_workspace"].sum())

    prev_m = month_metrics(prev_inc)
    cur_m = month_metrics(cur_inc)

    print(f"Prev month: {prev.label}")
    print(f"Cur  month: {cur.label}")
    print()
    print(f"Excluded messages (prev, cur): {exc_prev_msgs:,} , {exc_cur_msgs:,}")
    print()
    print(f"Messages total (prev to cur): {prev_m['messages_total']:,} to {cur_m['messages_total']:,}  delta {cur_m['messages_total']-prev_m['messages_total']:,}")
    print(f"Live messages (prev to cur):   {prev_m['live_messages_total']:,} to {cur_m['live_messages_total']:,}  delta {cur_m['live_messages_total']-prev_m['live_messages_total']:,}")
    print(f"Active live GPTs:              {prev_m['active_live_gpts']:,} to {cur_m['active_live_gpts']:,}")
    print(f"Live activation rate:          {prev_m['live_activation_rate']:.2%} to {cur_m['live_activation_rate']:.2%}")
    print(f"Top10 live share:              {prev_m['top10_live_share']:.2%} to {cur_m['top10_live_share']:.2%}")
    print()

    mom = mom_changes(prev_inc, cur_inc)

    top_new = mom[mom["status"] == "new_in_cur"].sort_values("messages_cur", ascending=False).head(10)
    top_up = mom[mom["status"] == "continuing"].sort_values("delta_messages", ascending=False).head(10)
    top_down = mom[mom["status"] == "continuing"].sort_values("delta_messages", ascending=True).head(10)
    dropped = mom[mom["status"] == "dropped_in_cur"].sort_values("messages_prev", ascending=False).head(10)

    print("Top new (live) by messages:")
    for _, r in top_new.iterrows():
        print(f"  {r['gpt_name_clean']}: {int(r['messages_cur']):,}")

    print()
    print("Top movers up (continuing live):")
    for _, r in top_up.iterrows():
        print(f"  {r['gpt_name_clean']}: {int(r['messages_prev']):,} to {int(r['messages_cur']):,}  delta {int(r['delta_messages']):,}")

    print()
    print("Top movers down (continuing live):")
    for _, r in top_down.iterrows():
        print(f"  {r['gpt_name_clean']}: {int(r['messages_prev']):,} to {int(r['messages_cur']):,}  delta {int(r['delta_messages']):,}")

    print()
    print("Dropped to zero (live) from prev:")
    for _, r in dropped.iterrows():
        print(f"  {r['gpt_name_clean']}: {int(r['messages_prev']):,}")

    if args.out:
        with pd.ExcelWriter(args.out, engine="openpyxl") as w:
            prev_inc.to_excel(w, index=False, sheet_name=f"{prev.label}_clean")
            cur_inc.to_excel(w, index=False, sheet_name=f"{cur.label}_clean")
            pd.DataFrame([prev_m, cur_m], index=[prev.label, cur.label]).to_excel(w, sheet_name="overview")
            mom.to_excel(w, index=False, sheet_name="mom_live_changes")
        print()
        print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
