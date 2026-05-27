#!/usr/bin/env python3
"""Build a GitHub Pages-ready static export from this Django project."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402

from apps.projects.models import Project  # noqa: E402

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "docs"
STATIC_SRC = ROOT / "static"
MEDIA_SRC = ROOT / "media"

EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")
HTML_EXTENSIONS = (".html", ".htm")


def _iter_routes() -> list[str]:
    routes = [
        "/",
        "/about/",
        "/team/",
        "/contact/",
        "/services/",
        "/projects/",
    ]
    project_routes = [f"/projects/{slug}/" for slug in Project.objects.filter(is_published=True).values_list("slug", flat=True)]
    return [*routes, *project_routes]


def _output_path_for_route(route: str) -> Path:
    if route == "/":
        return OUT_DIR / "index.html"
    normalized = route.strip("/")
    return OUT_DIR / normalized / "index.html"


def _depth_from_output_path(path: Path) -> int:
    if path.name != "index.html":
        return max(len(path.relative_to(OUT_DIR).parts) - 1, 0)
    parent = path.parent
    if parent == OUT_DIR:
        return 0
    return len(parent.relative_to(OUT_DIR).parts)


def _relative_prefix(depth: int) -> str:
    return "../" * depth


def _is_external(value: str) -> bool:
    return value.startswith(EXTERNAL_PREFIXES)


def _rewrite_link(value: str, prefix: str) -> str:
    stripped = value.strip()
    if not stripped or stripped.startswith("#") or _is_external(stripped):
        return value

    parsed = urlparse(stripped)
    if parsed.scheme or parsed.netloc:
        return value

    if stripped.startswith("/"):
        target = stripped.lstrip("/")
        if not target:
            return prefix or "./"
        rewritten = f"{prefix}{target}"
        return rewritten

    if stripped.startswith(("static/", "media/")):
        return f"{prefix}{stripped}"

    return value


def _rewrite_html(html: str, prefix: str) -> str:
    attrs = ('href="', "href='", 'src="', "src='", 'action="', "action='")
    output = html
    for attr in attrs:
        quote = attr[-1]
        cursor = 0
        chunks: list[str] = []
        while True:
            idx = output.find(attr, cursor)
            if idx == -1:
                chunks.append(output[cursor:])
                break
            chunks.append(output[cursor : idx + len(attr)])
            start = idx + len(attr)
            end = output.find(quote, start)
            if end == -1:
                chunks.append(output[start:])
                break
            original = output[start:end]
            rewritten = _rewrite_link(original, prefix)
            chunks.append(rewritten)
            cursor = end
        output = "".join(chunks)
    return output


def _copy_folder_if_exists(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)


def _clear_output_dir() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def _collect_html_files(base: Path) -> Iterable[Path]:
    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in HTML_EXTENSIONS:
            yield path


def build() -> None:
    client = Client()
    _clear_output_dir()

    routes = _iter_routes()
    for route in routes:
        response = client.get(route)
        if response.status_code != 200:
            raise RuntimeError(f"Failed rendering route {route}: HTTP {response.status_code}")

        out_file = _output_path_for_route(route)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(response.content)

    _copy_folder_if_exists(STATIC_SRC, OUT_DIR / "static")
    _copy_folder_if_exists(MEDIA_SRC, OUT_DIR / "media")

    for html_file in _collect_html_files(OUT_DIR):
        depth = _depth_from_output_path(html_file)
        prefix = _relative_prefix(depth)
        content = html_file.read_text(encoding="utf-8")
        rewritten = _rewrite_html(content, prefix)
        html_file.write_text(rewritten, encoding="utf-8")

    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Static export complete: {OUT_DIR}")
    print("Publish the docs/ folder with GitHub Pages.")


if __name__ == "__main__":
    build()
