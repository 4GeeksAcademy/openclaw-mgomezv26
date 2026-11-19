#!/usr/bin/env python3
"""Read-only 4Geeks student API client for future MØLI/OpenClaw skills.

The credential is read only from TOKEN_4GEEKS in the process environment.
Only documented GET endpoints on the documented production host are allowed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://breathecode.herokuapp.com"
MAX_RESPONSE_BYTES = 5 * 1024 * 1024


class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old = urllib.parse.urlsplit(req.full_url)
        new = urllib.parse.urlsplit(newurl)
        if new.scheme != "https" or new.hostname != old.hostname:
            raise urllib.error.HTTPError(req.full_url, code, "cross-host redirect blocked", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def parser_for_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Use the read-only 4Geeks student API client.")
    parser.add_argument("resource", choices=("verify-auth", "me", "cohorts", "tasks", "projects", "pending-work", "progress-summary", "content-search", "project-search", "project-assignment", "content-detail", "project-detail", "project-assignment-detail", "activity", "task-detail"))
    parser.add_argument("task_id", nargs="?", help="Numeric task id (required for task-detail or project-assignment-detail).")
    parser.add_argument("--task-status", choices=("PENDING", "DONE", "APPROVED", "REJECTED"))
    parser.add_argument("--task-type", choices=("PROJECT", "EXERCISE", "LESSON", "QUIZ"))
    parser.add_argument("--cohort", help="Cohort id or slug, when supported by the endpoint.")
    parser.add_argument("--academy", help="Academy id (used to filter cohort enrollments).")
    parser.add_argument("--educational-status", choices=("ACTIVE", "GRADUATED", "SUSPENDED", "DROPPED"))
    parser.add_argument("--date-start", help="Activity start date (YYYY-MM-DD).")
    parser.add_argument("--date-end", help="Activity end date (YYYY-MM-DD).")
    parser.add_argument("--query", help="Text to search in registry assets.")
    parser.add_argument("--asset-type", choices=("LESSON", "EXERCISE", "PROJECT"), help="Registry content type.")
    parser.add_argument("--asset-slug", help="Registry asset slug (for content-detail or project-detail).")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offset", type=int)
    return parser


def build_url(args: argparse.Namespace) -> str:
    paths = {
        "verify-auth": "/v1/admissions/user/me",
        "me": "/v1/admissions/user/me",
        "cohorts": "/v1/admissions/academy/cohort/me",
        "tasks": "/v1/assignment/user/me/task",
        "projects": "/v1/assignment/user/me/task",
        "pending-work": "/v1/assignment/user/me/task",
        "progress-summary": "/v1/assignment/user/me/task",
        "content-search": "/v1/registry/asset",
        "project-search": "/v1/registry/asset",
        "project-assignment": "/v1/assignment/user/me/task",
        "activity": "/v1/activity/me",
    }
    if args.resource in ("task-detail", "project-assignment-detail"):
        if not args.task_id or not re.fullmatch(r"[0-9]+", args.task_id):
            raise ValueError(f"{args.resource} requires a numeric task_id")
        path = f"/v1/assignment/task/{args.task_id}"
    elif args.resource in ("content-detail", "project-detail"):
        if not args.asset_slug or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", args.asset_slug):
            raise ValueError(f"{args.resource} requires an asset slug containing only letters, digits, hyphens, or underscores")
        path = f"/v1/registry/asset/{urllib.parse.quote(args.asset_slug, safe='')}"
    else:
        if args.task_id:
            raise ValueError("task_id is only accepted for task-detail or project-assignment-detail")
        path = paths[args.resource]

    query: dict[str, str] = {}
    if args.resource == "tasks":
        for name, value in (("task_status", args.task_status), ("task_type", args.task_type), ("cohort", args.cohort)):
            if value is not None:
                query[name] = value
    elif args.resource == "projects":
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end)):
            raise ValueError("projects always filters task_type=PROJECT and accepts no additional filters")
        query["task_type"] = "PROJECT"
    elif args.resource == "project-assignment":
        if not args.query or not args.query.strip():
            raise ValueError("project-assignment requires --query")
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end, args.asset_type, args.asset_slug)):
            raise ValueError("project-assignment accepts only --query, --limit, and --offset")
        query["task_type"] = "PROJECT"
    elif args.resource == "pending-work":
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end)):
            raise ValueError("pending-work fetches all assignments and filters statuses locally")
    elif args.resource == "progress-summary":
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end)):
            raise ValueError("progress-summary fetches all assignments and summarizes statuses locally")
    elif args.resource == "cohorts":
        for name, value in (("educational_status", args.educational_status),):
            if value is not None:
                query[name] = value
        if args.academy is not None:
            query["academy"] = args.academy
    elif args.resource == "activity":
        for name, value in (("cohort", args.cohort), ("date_start", args.date_start), ("date_end", args.date_end)):
            if value is not None:
                query[name] = value
    elif args.resource in ("content-search", "project-search"):
        if not args.query or not args.query.strip():
            raise ValueError(f"{args.resource} requires --query")
        if args.resource == "project-search":
            if args.asset_type not in (None, "PROJECT"):
                raise ValueError("project-search searches PROJECT assets only")
            args.asset_type = "PROJECT"
        elif not args.asset_type:
            raise ValueError("content-search requires --asset-type")
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end, args.asset_slug)):
            raise ValueError(f"{args.resource} accepts only --query, --asset-type, --limit, and --offset")
        query["asset_type"] = args.asset_type
        query["like"] = args.query.strip()
    elif args.resource in ("content-detail", "project-detail"):
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end, args.query, args.asset_type)):
            raise ValueError(f"{args.resource} accepts only --asset-slug")
    elif args.resource == "project-assignment-detail":
        if any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end, args.query, args.asset_type, args.asset_slug)):
            raise ValueError("project-assignment-detail accepts only a numeric task_id")
    elif any((args.task_status, args.task_type, args.cohort, args.academy, args.educational_status, args.date_start, args.date_end, args.query, args.asset_type, args.asset_slug)):
        raise ValueError("filters are not supported for this resource")

    if args.limit is not None:
        if args.resource not in ("tasks", "projects", "pending-work", "progress-summary", "content-search", "project-search", "project-assignment"):
            raise ValueError("limit is only enabled for task, project, and content lists")
        if not 1 <= args.limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        query["limit"] = str(args.limit)
    if args.offset is not None:
        if args.resource not in ("tasks", "projects", "pending-work", "progress-summary", "content-search", "project-search", "project-assignment"):
            raise ValueError("offset is only enabled for task, project, and content lists")
        if args.offset < 0:
            raise ValueError("offset must not be negative")
        query["offset"] = str(args.offset)
    suffix = "?" + urllib.parse.urlencode(query) if query else ""
    return BASE_URL + path + suffix


def summarize_assignments(rows: list[dict]) -> dict:
    """Count unique assignments by their API id, failing closed on conflicts."""
    by_id: dict[object, dict] = {}
    duplicates = 0
    for row in rows:
        assignment_id = row.get("id")
        if assignment_id is None:
            raise ValueError("assignment is missing its id; cannot safely deduplicate")
        if assignment_id in by_id:
            if row.get("task_status") != by_id[assignment_id].get("task_status"):
                raise ValueError("duplicate assignment id has conflicting statuses")
            duplicates += 1
            continue
        by_id[assignment_id] = row

    total = len(by_id)
    counts = {status: 0 for status in ("PENDING", "DONE", "APPROVED", "REJECTED")}
    for row in by_id.values():
        status = row.get("task_status", "UNKNOWN")
        if status in counts:
            counts[status] += 1
    counts["UNKNOWN"] = total - sum(counts.values())

    def percent(count: int) -> float:
        return round((count / total * 100) if total else 0.0, 1)

    submitted_or_approved = counts["DONE"] + counts["APPROVED"]
    return {
        "total": total,
        "duplicate_records_ignored": duplicates,
        "counts": counts,
        "percentages": {status: percent(count) for status, count in counts.items()},
        "done_or_approved": submitted_or_approved,
        "done_or_approved_percent": percent(submitted_or_approved),
    }


def main() -> int:
    parser = parser_for_cli()
    args = parser.parse_args()
    try:
        if args.resource == "progress-summary" and args.offset is not None:
            parser.error("progress-summary always starts at offset 0; use --limit only to change page size")
        url = build_url(args)
    except ValueError as exc:
        parser.error(str(exc))

    token = os.environ.get("TOKEN_4GEEKS", "").strip()
    if not token:
        if args.resource == "verify-auth":
            print("AUTH_STATUS=TOKEN_MISSING")
        else:
            print("Error: TOKEN_4GEEKS is missing from this process environment.", file=sys.stderr)
        return 2

    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Token {token}", "Accept": "application/json"},
        method="GET",
    )
    opener = urllib.request.build_opener(SameHostRedirect())
    try:
        if args.resource in ("content-search", "project-search"):
            page_size = args.limit or 20
            offset = args.offset or 0
            max_pages = 50
            pages = 0
            known_total: int | None = None
            assets: list[dict] = []
            while pages < max_pages:
                args.limit = page_size
                args.offset = offset
                page_url = build_url(args)
                page_request = urllib.request.Request(
                    page_url,
                    headers={"Authorization": f"Token {token}", "Accept": "application/json"},
                    method="GET",
                )
                with opener.open(page_request, timeout=20) as response:
                    body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                    return 3
                try:
                    page = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                    return 4
                if isinstance(page, list):
                    rows = page
                elif isinstance(page, dict) and isinstance(page.get("results"), list):
                    rows = page["results"]
                    count = page.get("count")
                    if isinstance(count, int) and count >= 0:
                        known_total = count
                else:
                    print("Error: API returned an unexpected registry-list format.", file=sys.stderr)
                    return 4
                assets.extend(row for row in rows if isinstance(row, dict))
                pages += 1
                if not rows or len(rows) < page_size:
                    break
                offset += len(rows)
                if known_total is not None and offset >= known_total:
                    break
            else:
                print("Error: registry pagination exceeded the 50-page safety limit.", file=sys.stderr)
                return 5

            # Keep discovery output compact and avoid exposing owner/private metadata.
            results = []
            seen: set[object] = set()
            for row in assets:
                slug = row.get("slug")
                if not isinstance(slug, str) or not slug or slug in seen:
                    continue
                seen.add(slug)
                category = row.get("category")
                results.append({
                    "title": row.get("title") or "(sin título)",
                    "slug": slug,
                    "asset_type": row.get("asset_type", args.asset_type),
                    "description": row.get("description") or "",
                    "category": category.get("title") if isinstance(category, dict) else None,
                    "technologies": [t.get("name") for t in row.get("technologies", []) if isinstance(t, dict) and t.get("name")],
                    **({"readme_url": row.get("readme_url")} if args.resource == "project-search" else {}),
                })
            print(json.dumps({"count": len(results), "api_total": known_total, "pages": pages, "results": results}, ensure_ascii=False))
            return 0

        if args.resource in ("content-detail", "project-detail", "project-assignment-detail"):
            with opener.open(request, timeout=20) as response:
                body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                return 3
            try:
                asset = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                return 4
            if not isinstance(asset, dict):
                detail_kind = "assignment" if args.resource == "project-assignment-detail" else "registry"
                print(f"Error: API returned an unexpected {detail_kind}-detail format.", file=sys.stderr)
                return 4
            category = asset.get("category")
            safe = {
                "title": asset.get("title"),
                "slug": asset.get("slug"),
                "asset_type": asset.get("asset_type"),
                "description": asset.get("description") or "",
                "readme_url": asset.get("readme_url"),
                "category": category.get("title") if isinstance(category, dict) else None,
                "technologies": [t.get("name") for t in asset.get("technologies", []) if isinstance(t, dict) and t.get("name")],
                "related_assets": [
                    {"title": r.get("title"), "slug": r.get("slug"), "asset_type": r.get("asset_type")}
                    for r in asset.get("assets_related", []) if isinstance(r, dict)
                ],
            }
            if args.resource == "project-assignment-detail":
                if asset.get("task_type") != "PROJECT":
                    print("Error: assignment is not a PROJECT.", file=sys.stderr)
                    return 4
                safe = {
                    "title": asset.get("title"),
                    "task_type": asset.get("task_type"),
                    "status": asset.get("task_status"),
                    "description": asset.get("description") or "",
                    "score": asset.get("score"),
                    "feedback": asset.get("feedback"),
                    "revision_status": asset.get("revision_status"),
                    "associated_slug": asset.get("associated_slug"),
                }
            elif args.resource == "project-detail":
                if asset.get("asset_type") != "PROJECT":
                    print("Error: registry asset is not a PROJECT.", file=sys.stderr)
                    return 4
                safe = {
                    "title": asset.get("title"),
                    "slug": asset.get("slug"),
                    "asset_type": asset.get("asset_type"),
                    "description": asset.get("description") or "",
                    "readme_url": asset.get("readme_url"),
                    "url": asset.get("url"),
                    "assessment": asset.get("assessment"),
                    "delivery_instructions": asset.get("delivery_instructions"),
                    "graded": asset.get("graded"),
                    "difficulty": asset.get("difficulty"),
                    "duration": asset.get("duration"),
                    "technologies": [t.get("name") or t.get("title") for t in asset.get("technologies", []) if isinstance(t, dict) and (t.get("name") or t.get("title"))],
                    "related_assets": [
                        {"title": r.get("title"), "slug": r.get("slug"), "asset_type": r.get("asset_type")}
                        for r in asset.get("assets_related", []) if isinstance(r, dict)
                    ],
                }
            print(json.dumps(safe, ensure_ascii=False))
            return 0

        if args.resource == "project-assignment":
            page_size = args.limit or 100
            offset = args.offset or 0
            assignments: list[dict] = []
            known_total: int | None = None
            max_pages = 50
            pages = 0
            while pages < max_pages:
                args.limit = page_size
                args.offset = offset
                page_url = build_url(args)
                page_request = urllib.request.Request(page_url, headers={"Authorization": f"Token {token}", "Accept": "application/json"}, method="GET")
                with opener.open(page_request, timeout=20) as response:
                    body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                    return 3
                try:
                    page = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                    return 4
                if isinstance(page, list):
                    rows = page
                elif isinstance(page, dict) and isinstance(page.get("results"), list):
                    rows = page["results"]
                    count = page.get("count")
                    if isinstance(count, int) and count >= 0:
                        known_total = count
                else:
                    print("Error: API returned an unexpected assignment-list format.", file=sys.stderr)
                    return 4
                assignments.extend(row for row in rows if isinstance(row, dict))
                pages += 1
                if not rows or len(rows) < page_size:
                    break
                offset += len(rows)
                if known_total is not None and offset >= known_total:
                    break
            else:
                print("Error: project assignment pagination exceeded the 50-page safety limit.", file=sys.stderr)
                return 5
            needle = args.query.strip().casefold()
            matches = []
            for row in assignments:
                title = str(row.get("title") or "")
                if row.get("task_type") != "PROJECT" or needle not in title.casefold():
                    continue
                matches.append({
                    "assignment_id": row.get("id"),
                    "title": title,
                    "status": row.get("task_status", "UNKNOWN"),
                    "description": row.get("description") or "",
                    "associated_slug": row.get("associated_slug"),
                })
            print(json.dumps({"count": len(matches), "pages": pages, "api_total": known_total, "assignments": matches}, ensure_ascii=False))
            return 0

        if args.resource == "projects":
            page_size = args.limit or 100
            offset = args.offset or 0
            all_projects: list[dict] = []
            known_total: int | None = None
            max_pages = 50
            pages = 0
            while pages < max_pages:
                args.limit = page_size
                args.offset = offset
                page_url = build_url(args)
                page_request = urllib.request.Request(
                    page_url,
                    headers={"Authorization": f"Token {token}", "Accept": "application/json"},
                    method="GET",
                )
                with opener.open(page_request, timeout=20) as response:
                    body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                    return 3
                try:
                    page = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                    return 4
                if isinstance(page, list):
                    rows = page
                elif isinstance(page, dict) and isinstance(page.get("results"), list):
                    rows = page["results"]
                    count = page.get("count")
                    if isinstance(count, int) and count >= 0:
                        known_total = count
                else:
                    print("Error: API returned an unexpected project-list format.", file=sys.stderr)
                    return 4

                all_projects.extend(row for row in rows if isinstance(row, dict))
                pages += 1
                if not rows or len(rows) < page_size:
                    break
                offset += len(rows)
                if known_total is not None and offset >= known_total:
                    break
            else:
                print("Error: project pagination exceeded the 50-page safety limit.", file=sys.stderr)
                return 5

            # Return only fields needed to identify an assigned project and its state.
            # Omit descriptions, feedback, URLs, and unrelated personal metadata.
            projects = [
                {
                    "title": row.get("title") or "(sin título)",
                    "status": row.get("task_status", "UNKNOWN"),
                }
                for row in all_projects
                if row.get("task_type") == "PROJECT"
            ]
            print(json.dumps({"count": len(projects), "pages": pages, "projects": projects}, ensure_ascii=False))
            return 0

        if args.resource == "pending-work":
            page_size = args.limit or 100
            offset = args.offset or 0
            assignments: list[dict] = []
            known_total: int | None = None
            max_pages = 50
            pages = 0
            while pages < max_pages:
                args.limit = page_size
                args.offset = offset
                page_url = build_url(args)
                page_request = urllib.request.Request(
                    page_url,
                    headers={"Authorization": f"Token {token}", "Accept": "application/json"},
                    method="GET",
                )
                with opener.open(page_request, timeout=20) as response:
                    body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                    return 3
                try:
                    page = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                    return 4
                if isinstance(page, list):
                    rows = page
                elif isinstance(page, dict) and isinstance(page.get("results"), list):
                    rows = page["results"]
                    count = page.get("count")
                    if isinstance(count, int) and count >= 0:
                        known_total = count
                else:
                    print("Error: API returned an unexpected assignment-list format.", file=sys.stderr)
                    return 4

                assignments.extend(row for row in rows if isinstance(row, dict))
                pages += 1
                if not rows or len(rows) < page_size:
                    break
                offset += len(rows)
                if known_total is not None and offset >= known_total:
                    break
            else:
                print("Error: assignment pagination exceeded the 50-page safety limit.", file=sys.stderr)
                return 5

            relevant_statuses = {"PENDING", "REJECTED", "DONE"}
            work_items = [
                {
                    "title": row.get("title") or "(sin título)",
                    "task_type": row.get("task_type", "UNKNOWN"),
                    "status": row.get("task_status", "UNKNOWN"),
                }
                for row in assignments
                if row.get("task_status") in relevant_statuses
            ]
            print(json.dumps({"count": len(work_items), "pages": pages, "items": work_items}, ensure_ascii=False))
            return 0

        if args.resource == "progress-summary":
            page_size = args.limit or 100
            offset = 0
            assignments: list[dict] = []
            known_total: int | None = None
            max_pages = 50
            pages = 0
            while pages < max_pages:
                args.limit = page_size
                args.offset = offset
                page_url = build_url(args)
                page_request = urllib.request.Request(
                    page_url,
                    headers={"Authorization": f"Token {token}", "Accept": "application/json"},
                    method="GET",
                )
                with opener.open(page_request, timeout=20) as response:
                    body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                    return 3
                try:
                    page = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                    return 4
                if isinstance(page, list):
                    rows = page
                elif isinstance(page, dict) and isinstance(page.get("results"), list):
                    rows = page["results"]
                    count = page.get("count")
                    if isinstance(count, int) and count >= 0:
                        known_total = count
                else:
                    print("Error: API returned an unexpected assignment-list format.", file=sys.stderr)
                    return 4

                assignments.extend(row for row in rows if isinstance(row, dict))
                pages += 1
                if not rows or len(rows) < page_size:
                    break
                offset += len(rows)
                if known_total is not None and offset >= known_total:
                    break
            else:
                print("Error: progress summary pagination exceeded the 50-page safety limit.", file=sys.stderr)
                return 5

            try:
                summary = summarize_assignments(assignments)
            except ValueError as exc:
                print(f"Error: cannot safely summarize assignments: {exc}.", file=sys.stderr)
                return 4
            summary["pages"] = pages
            summary["api_total"] = known_total
            print(json.dumps(summary, ensure_ascii=False))
            return 0

        with opener.open(request, timeout=20) as response:
            if args.resource == "verify-auth":
                # This branch deliberately discards the user profile response.
                print(f"AUTH_STATUS=VALID HTTP_STATUS={response.status}")
                return 0
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                print("Error: API response exceeded the 5 MiB safety limit.", file=sys.stderr)
                return 3
            text = body.decode("utf-8")
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                print("Error: API returned a successful response that was not JSON.", file=sys.stderr)
                return 4
            print(json.dumps(result, ensure_ascii=False))
            return 0
    except urllib.error.HTTPError as exc:
        # Do not print response bodies: they may contain personal data or diagnostics.
        if args.resource == "verify-auth" and exc.code in (401, 403):
            print(f"AUTH_STATUS=TOKEN_REJECTED HTTP_STATUS={exc.code}")
            return 12
        if args.resource == "verify-auth":
            print(f"AUTH_STATUS=API_ERROR HTTP_STATUS={exc.code}")
            return 13
        print(f"API request failed with HTTP {exc.code}.", file=sys.stderr)
        return 10
    except (urllib.error.URLError, TimeoutError, OSError):
        print("API request failed due to a connection or timeout error.", file=sys.stderr)
        return 11


if __name__ == "__main__":
    raise SystemExit(main())
