#!/usr/bin/env python3
"""Run the daily papers pipeline and save the final recommendation into the vault."""

import argparse
import asyncio
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SHARED_DIR = _ROOT.parent / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))

from user_config import daily_papers_dir

import enrich_papers
import fetch_and_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Target date YYYY-MM-DD (default: today)")
    parser.add_argument("--days", type=int, default=1, help="Number of days to fetch")
    parser.add_argument("--start-date", help="Start date YYYY-MM-DD for explicit range mode")
    parser.add_argument("--end-date", help="End date YYYY-MM-DD for explicit range mode")
    return parser.parse_args()


def source_label(paper: dict) -> str:
    source = paper.get("source", "")
    if source == "hf-daily":
        upvotes = paper.get("hf_upvotes", 0) or 0
        return f"HF Daily, upvotes={upvotes}"
    if source == "hf-trending":
        upvotes = paper.get("hf_upvotes", 0) or 0
        return f"HF Trending, upvotes={upvotes}"
    return "arXiv"


def summarize_counts(papers: list[dict]) -> str:
    counts = Counter(p.get("source", "unknown") for p in papers)
    parts = []
    for key in ("hf-daily", "hf-trending", "arxiv"):
        if counts.get(key):
            parts.append(f"{key}={counts[key]}")
    return ", ".join(parts) if parts else "no papers"


def render_paper_section(index: int, paper: dict) -> str:
    title = paper.get("title", "Untitled")
    authors = paper.get("authors") or "Unknown"
    affiliations = paper.get("affiliations") or "Unknown"
    venue = paper.get("venue") or paper.get("preferred_venue_match") or "arXiv"
    score = paper.get("score", 0)
    method_summary = (paper.get("method_summary") or "").strip()
    abstract = (paper.get("abstract") or "").strip()
    summary = method_summary if len(method_summary) >= 80 else abstract
    summary = " ".join(summary.split())
    if len(summary) > 600:
        summary = summary[:597].rsplit(" ", 1)[0] + "..."

    lines = [
        f"### {index}. {title}",
        f"- 作者: {authors}",
        f"- 机构: {affiliations}",
        f"- 来源: {source_label(paper)}",
        f"- Venue: {venue}",
        f"- Score: {score}",
        f"- 链接: [arXiv]({paper.get('url', '')}) | [PDF]({paper.get('pdf', '')})",
    ]

    comments = (paper.get("comments") or "").strip()
    journal_ref = (paper.get("journal_ref") or "").strip()
    if comments:
        lines.append(f"- Comments: {comments}")
    if journal_ref:
        lines.append(f"- Journal Ref: {journal_ref}")
    if summary:
        lines.append(f"- 核心: {summary}")

    return "\n".join(lines)


def render_title(mode: str, start_date, end_date, days: int) -> str:
    if mode == "range":
        return f"{start_date.isoformat()} 到 {end_date.isoformat()} 论文推荐"
    return "今日论文推荐" if days == 1 else f"过去{days}天论文推荐"


def render_markdown(mode: str, target_date, start_date, end_date, days: int, papers: list[dict]) -> str:
    title = render_title(mode, start_date, end_date, days)
    intro = (
        f"共筛到 {len(papers)} 篇，来源分布：{summarize_counts(papers)}。"
        " 结果已经按当前配置写入 vault，而不是临时目录。"
    )
    if mode == "range":
        intro += " 指定时间范围模式下会跳过 history 去重，且不纳入 HF Trending。"
    body = "\n\n".join(render_paper_section(i, paper) for i, paper in enumerate(papers, start=1))
    return (
        "---\n"
        f"date: {target_date.isoformat()}\n"
        f"mode: {mode}\n"
        f"start_date: {start_date.isoformat()}\n"
        f"end_date: {end_date.isoformat()}\n"
        f"days: {days}\n"
        "tags: [daily-papers, auto-generated]\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{intro}\n\n"
        f"{body}\n"
    )


def update_history(history_path: Path, target_date, papers: list[dict]) -> None:
    if history_path.exists():
        try:
            history = json.loads(history_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            history = []
    else:
        history = []

    by_id = {}
    for item in history:
        paper_id = item.get("id")
        if paper_id and paper_id not in by_id:
            by_id[paper_id] = item

    for paper in papers:
        paper_id = fetch_and_score.extract_arxiv_id(paper.get("url", ""))
        if not paper_id:
            continue
        if paper_id not in by_id:
            by_id[paper_id] = {
                "id": paper_id,
                "date": target_date.isoformat(),
                "title": paper.get("title", ""),
            }

    cutoff = target_date - timedelta(days=30)
    kept = []
    for item in by_id.values():
        date_str = item.get("date", "")
        try:
            item_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            kept.append(item)
            continue
        if item_date >= cutoff:
            kept.append(item)

    kept.sort(key=lambda x: (x.get("date", ""), x.get("id", "")))
    history_path.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def output_stem(mode: str, start_date, end_date) -> str:
    if mode == "range":
        return f"{start_date.isoformat()}_to_{end_date.isoformat()}"
    return end_date.isoformat()


def save_debug_jsons(out_dir: Path, stem: str, top: list[dict], enriched: list[dict]) -> None:
    (out_dir / f"{stem}-top30.json").write_text(
        json.dumps(top, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / f"{stem}-enriched.json").write_text(
        json.dumps(enriched, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    window = fetch_and_score.resolve_fetch_window(
        date_str=args.date,
        days=args.days,
        start_date_str=args.start_date,
        end_date_str=args.end_date,
    )
    mode = window["mode"]
    target_date = window["target_date"]
    start_date = window["start_date"]
    end_date = window["end_date"]
    days = window["days"]
    stem = output_stem(mode, start_date, end_date)

    out_dir = daily_papers_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"[daily-papers] mode={mode} start_date={start_date} end_date={end_date} days={days}",
        file=sys.stderr,
    )
    top = fetch_and_score.merge_and_dedup(
        fetch_and_score.fetch_hf_papers(
            start_date,
            end_date,
            include_trending=window["include_trending"],
        ),
        fetch_and_score.fetch_arxiv_papers(
            start_date,
            end_date,
            days,
            strict_date_filter=window["strict_date_filter"],
        ),
        target_date,
        days=days,
        top_n=window["top_n"],
        disable_history_dedup=window["disable_history_dedup"],
    )
    enriched = asyncio.run(enrich_papers.enrich_all(top))

    save_debug_jsons(out_dir, stem, top, enriched)

    markdown = render_markdown(mode, target_date, start_date, end_date, days, enriched)
    md_path = out_dir / f"{stem}-论文推荐.md"
    md_path.write_text(markdown, encoding="utf-8")

    if mode != "range":
        update_history(out_dir / ".history.json", target_date, enriched)

    print(str(md_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
