#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import json
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
METRICS_OUT = ASSETS / "github-graphics.png"
GRID_OUT = ASSETS / "contribution-grid.png"

FONT_PATHS = [
    Path("/Library/Fonts/Monaco.ttf"),
    Path("/System/Library/Fonts/Menlo.ttc"),
]
FONT_PATH = next(path for path in FONT_PATHS if path.exists())


def gh_graphql():
    query = """
query($login:String!){
  user(login:$login){
    login
    name
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            color
          }
        }
      }
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
    repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC, orderBy:{field:UPDATED_AT,direction:DESC}) {
      totalCount
      nodes {
        name
        stargazerCount
        forkCount
        primaryLanguage { name color }
      }
    }
    pullRequests(states:MERGED) { totalCount }
  }
}
"""
    raw = subprocess.check_output(
        ["gh", "api", "graphql", "-f", f"query={query}", "-f", "login=juliosuas"],
        text=True,
    )
    return json.loads(raw)["data"]["user"]


def font(size):
    return ImageFont.truetype(str(FONT_PATH), size)


def glow_text(draw, xy, text, fnt, fill="#33ff33"):
    x, y = xy
    for dx, dy in ((0, 0), (1, 0), (0, 1)):
        draw.text((x + dx, y + dy), text, font=fnt, fill="#0f6f0f")
    draw.text(xy, text, font=fnt, fill=fill)


def card(draw, box, title, value, subtitle=None):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=10, outline="#1d4f1d", width=2, fill="#050805")
    draw.text((x1 + 24, y1 + 22), title.upper(), font=font(22), fill="#7d9b7d")
    glow_text(draw, (x1 + 24, y1 + 62), value, font(42))
    if subtitle:
        draw.text((x1 + 24, y2 - 42), subtitle, font=font(20), fill="#8cff8c")


def render_metrics(user):
    repos = user["repositories"]
    cc = user["contributionsCollection"]
    calendar = cc["contributionCalendar"]
    repo_nodes = repos["nodes"]
    langs = Counter(
        node["primaryLanguage"]["name"]
        for node in repo_nodes
        if node.get("primaryLanguage")
    )
    top_langs = "  ".join(name for name, _ in langs.most_common(5))
    top_repos = sorted(
        repo_nodes,
        key=lambda n: (n["stargazerCount"], n["forkCount"]),
        reverse=True,
    )[:4]

    img = Image.new("RGB", (1450, 620), "#030603")
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, 1450, 58), fill="#111611")
    draw.ellipse((24, 20, 42, 38), fill="#ff5f57")
    draw.ellipse((58, 20, 76, 38), fill="#febc2e")
    draw.ellipse((92, 20, 110, 38), fill="#28c840")
    draw.text((520, 18), "github receipts - juliosuas", font=font(20), fill="#8c948c")

    card(draw, (34, 92, 358, 230), "public repos", str(repos["totalCount"]), "owner repositories")
    card(draw, (392, 92, 716, 230), "merged PRs", str(user["pullRequests"]["totalCount"]), "public upstream work")
    card(draw, (750, 92, 1074, 230), "year commits", str(cc["totalCommitContributions"]), "current year")
    card(draw, (1108, 92, 1416, 230), "contribs", str(calendar["totalContributions"]), "last 12 months")

    draw.text((34, 280), "top languages", font=font(24), fill="#7d9b7d")
    glow_text(draw, (34, 322), top_langs or "Python  TypeScript  JavaScript", font(32))

    draw.text((34, 396), "public repos with signal", font=font(24), fill="#7d9b7d")
    y = 436
    for repo in top_repos:
        stars = repo["stargazerCount"]
        forks = repo["forkCount"]
        lang = repo["primaryLanguage"]["name"] if repo.get("primaryLanguage") else "code"
        draw.text((34, y), f"{repo['name']:<26} {lang:<12} stars:{stars:<3} forks:{forks:<3}", font=font(23), fill="#8cff8c")
        y += 34

    img.save(METRICS_OUT)


def render_grid(user):
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    total = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]

    img = Image.new("RGB", (1450, 260), "#030603")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1450, 58), fill="#111611")
    draw.ellipse((24, 20, 42, 38), fill="#ff5f57")
    draw.ellipse((58, 20, 76, 38), fill="#febc2e")
    draw.ellipse((92, 20, 110, 38), fill="#28c840")
    draw.text((480, 18), f"contribution grid - {total} in the last year", font=font(20), fill="#8c948c")

    cell = 17
    gap = 5
    start_x = 36
    start_y = 88
    fallback = ["#071407", "#0e4429", "#006d32", "#26a641", "#39d353"]

    for x, week in enumerate(weeks):
        for y, day in enumerate(week["contributionDays"]):
            count = day["contributionCount"]
            color = day["color"] if count else fallback[0]
            px = start_x + x * (cell + gap)
            py = start_y + y * (cell + gap)
            draw.rounded_rectangle((px, py, px + cell, py + cell), radius=3, fill=color)

    draw.text((36, 230), "less", font=font(15), fill="#7d9b7d")
    for i, color in enumerate(fallback):
        x = 95 + i * 24
        draw.rounded_rectangle((x, 230, x + 14, 244), radius=2, fill=color)
    draw.text((225, 230), "more", font=font(15), fill="#7d9b7d")

    img.save(GRID_OUT)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    data = gh_graphql()
    render_metrics(data)
    render_grid(data)
    print(METRICS_OUT)
    print(GRID_OUT)
