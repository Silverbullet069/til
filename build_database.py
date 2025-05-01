#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File         :   build_database.py
@Time         :   2024-12-04 22:31:20
@Author       :   Silverbullet069
@Version      :   1.0
@License      :   MIT License
@Desc         :   Build a SQLite database from README file.
@Cre (if any) :   Simon Willison (content), Claude 3.5 Sonnet (comments and optimization)
'''

from bs4 import BeautifulSoup  # parsing HTML content
from datetime import timezone
import httpx  # make HTTP sync/async req
import git
import os
import pathlib  # handle FS path
import sqlite3
import time
from dotenv import load_dotenv
from utils import setup_logging
from utils import compute_md5

load_dotenv()
github_token = os.environ.get("MARKDOWN_GITHUB_TOKEN")
if not github_token:
    assert (
        False
    ), "GitHub token not found. Please set the MARKDOWN_GITHUB_TOKEN environment variable."

logger = setup_logging(name=pathlib.Path(__file__).name)

# depreciated soon
root = pathlib.Path(__file__).parent.resolve()


def extract_first_paragraph(html):
    soup = BeautifulSoup(html, "html.parser")
    first_paragraph = soup.find("p")
    # in case there is no first paragraph
    clean_first_paragraph = (
        " ".join(first_paragraph.stripped_strings) if first_paragraph else ""
    )

    logger.debug(f"{extract_first_paragraph.__name__} processed! First paragraph: {clean_first_paragraph}")
    return clean_first_paragraph

# In GitHub Actions, file timestamps will reflect the checkout time, not original times
def create_created_changed_times(ref="master"):
    """

    Return a dictionary with the creation and last update times of files in a GitHuy Repository's branch

    This only works for files committed to the git repository. Uncommitted files won't have timestamp data.

    """

    created_changed_times = {}
    repo = git.Repo(search_parent_directories=True, odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref)))

    for commit in commits:
        dt = commit.committed_datetime
        affected_files = list(commit.stats.files.keys())
        for file_path in affected_files:
            if file_path.split(".")[-1] != "md":
                continue

            if file_path not in created_changed_times:
                created_changed_times[file_path] = {
                    "created": dt.isoformat(),
                    "created_utc": dt.astimezone(timezone.utc).isoformat(),
                }

            created_changed_times[file_path].update(
                {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            )
    logger.debug(
        f"{create_created_changed_times.__name__} finished successfully!\nContent: {created_changed_times}"
    )
    return created_changed_times


# build a SQLite database from Markdown files
# - fetching creation and update times
# - extracting title, body, path (sanitized), topic, slug, url
# - rendering Markdown to HTML using GitHub's API (?)
# - enabling Full-text search on database


def build_database(ref="master"):
    all_times = create_created_changed_times()

    repo = git.Repo(search_parent_directories=True, odbt=git.GitDB)
    repo_path = pathlib.Path(repo.working_dir).resolve()

    # This database file will be downloaded from S3 bucket during GitHub Actions workflow
    # If my commit message includes 'REBUILD', download process won't start
    db_path = repo_path / "tils.db"

    with sqlite3.connect(db_path) as conn:  # transaction
        conn.row_factory = (
            sqlite3.Row
        )
        cursor = conn.cursor()

        # batch processing
        records = []
        for file_path in repo_path.glob("*/*.md"):

            # check file content changed or not
            md5 = compute_md5(file_path)
            path = str(file_path.relative_to(repo_path))
            path_sanitized = path.replace("/", "_")

            til_info_row = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='til'"
            ).fetchone()
            if til_info_row is not None:
                row = cursor.execute(
                    "SELECT * FROM til WHERE path = ?", (path_sanitized,)
                ).fetchone()

                logger.debug(f"Existing data inside database for {path}: {dict(row)}")

                prev_md5 = row["md5"] if row is not None else ""  # new TIL

                if md5 == prev_md5:
                    logger.debug(f"File {path} content unchanged! Skipped.")
                    continue

                html = row["html"]
                summary = row["summary"]

            with file_path.open("r", encoding="utf-8") as f:
                title = f.readline().lstrip("#").strip()
                body = f.read().strip()

            slug = str(file_path.stem)
            url = f"https://github.com/Silverbullet069/til/blob/{ref}/{path}"
            topic = path.split("/")[0]

            retries = 0
            response = None
            while retries < 3:
                req_header = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {github_token}",
                    "X-GitHub-Api-Version": "2022-11-28",
                }

                logger.debug(f"Begin rendering HTML for {path}")
                try:
                    response = httpx.post(
                        "https://api.github.com/markdown",
                        json={"mode": "markdown", "text": body},
                        headers=req_header,
                    )
                except httpx.ConnectTimeout:
                    retries += 1
                    logger.error(
                        f"GitHub REST API is being rate-limited. Number of attempt: {retries} ..."
                    )
                    logger.debug("Sleeping in 5s...")
                    time.sleep(5)
                    continue

                if response.status_code == 200:
                    html = response.text
                    summary = extract_first_paragraph(html)
                    logger.debug(f"Rendered HTML for {path} successfully")
                    # do I need to wait here?
                    # https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28#primary-rate-limit-for-github_token-in-github-actions
                    # 1000 requests per hour, good enough for me
                    break

                # can't find in document: https://docs.github.com/en/rest/markdown/markdown?apiVersion=2022-11-28#render-a-markdown-document--status-codes
                elif response.status_code == 401:
                    assert (
                        False
                    ), f"{response.status_code} - Unauthorized error rendering markdown"
                else:
                    logger.error(
                        f"Status code: {response.status_code} - Headers: {response.headers}"
                    )
                    logger.debug("Sleeping in 5s...")
                    time.sleep(5)
                    retries += 1
            else:
                assert (
                    False
                ), f"Could not render {path} - last response was {response.headers}"

            # NOTE: if record structure is changed, remember to change table schema as well
            record = {
                "md5": md5,
                "path": path_sanitized,
                "slug": slug,
                "url": url,
                "topic": topic,
                "title": title,
                "body": body,
                "html": html,
                "summary": summary,
                **all_times[path],
            }

            records.append(record)
            logger.debug(f"Record for {path} created successfully!")

            # TODO: comment after finish testing
            # this ensure only the first file Markdown file it found is processed
            break

        # TODO: comment after finish testing
        # write a dictionary into file, create the file if not exists
        # with open("records.txt", "w") as f:
        #     [f.writelines(str(record)) for record in records]

        if len(records) == 0:
            assert False, "There isn't a single record in TIL!"

        # rebuilt if `tils.db` not existed
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS til (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                md5 TEXT NOT NULL UNIQUE,
                path TEXT NOT NULL UNIQUE,
                slug TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                html TEXT NOT NULL,
                summary TEXT NOT NULL,
                created TEXT NOT NULL,
                created_utc TEXT NOT NULL,
                updated TEXT NOT NULL,
                updated_utc TEXT NOT NULL
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS til_fts USING fts5(
                title,
                body,
                content='til',
                content_rowid='id'
            );

            -- Add triggers to keep FTS in sync
            CREATE TRIGGER IF NOT EXISTS til_after_insert AFTER INSERT ON til BEGIN
                INSERT INTO til_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
            END;

            CREATE TRIGGER IF NOT EXISTS til_after_update AFTER UPDATE ON til BEGIN
                INSERT INTO til_fts(til_fts, rowid, title, body) VALUES('delete', old.id, old.title, old.body);
                INSERT INTO til_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
            END;

            CREATE TRIGGER IF NOT EXISTS til_after_delete AFTER DELETE ON til BEGIN
                INSERT INTO til_fts(til_fts, rowid, title, body) VALUES('delete', old.id, old.title, old.body);
            END;
        """
        )
        conn.commit()  # nested transaction
        logger.debug("Table initialization (if not exists) completed successfully!")

        # bulk insert/update
        cursor.executemany(
            """
            INSERT OR REPLACE INTO til (
                md5, path, slug, url, topic, title, body, html, summary, created, created_utc, updated, updated_utc
            )
            VALUES (
                :md5, :path, :slug, :url, :topic, :title, :body, :html, :summary, :created, :created_utc, :updated, :updated_utc
            )
        """,
            records,
        )
        # triggers have been setup so no need to update FTS table
        conn.commit()  # nested transaction
        logger.debug(f"Updated tils.db with {len(records)} records.")


if __name__ == "__main__":
    build_database(root)
