import os
import sqlite3
from datetime import date
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

# Render's normal filesystem may reset on redeploy/restart.
# Set DATABASE_PATH to a persistent disk path if one is configured.
DB_PATH = os.environ.get("DATABASE_PATH", str(Path("instance") / "study.db"))

def get_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS study_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_date TEXT NOT NULL,
                subject TEXT NOT NULL,
                minutes INTEGER NOT NULL,
                note TEXT DEFAULT ''
            )
        """)

@app.route("/", methods=["GET"])
def index():
    init_db()
    today = date.today().isoformat()
    with get_db() as conn:
        records = conn.execute(
            "SELECT * FROM study_records ORDER BY study_date DESC, id DESC"
        ).fetchall()
        today_total = conn.execute(
            "SELECT COALESCE(SUM(minutes), 0) FROM study_records WHERE study_date = ?",
            (today,)
        ).fetchone()[0]
        all_total = conn.execute(
            "SELECT COALESCE(SUM(minutes), 0) FROM study_records"
        ).fetchone()[0]
        subject_count = conn.execute(
            "SELECT COUNT(DISTINCT subject) FROM study_records WHERE study_date = ?",
            (today,)
        ).fetchone()[0]
    return render_template(
        "index.html",
        records=records,
        today=today,
        today_total=today_total,
        all_total=all_total,
        subject_count=subject_count
    )

@app.route("/add", methods=["POST"])
def add_record():
    study_date = request.form.get("study_date", "").strip()
    subject = request.form.get("subject", "").strip()
    note = request.form.get("note", "").strip()
    try:
        minutes = int(request.form.get("minutes", "0"))
        date.fromisoformat(study_date)
    except (ValueError, TypeError):
        flash("日付と勉強時間を正しく入力してください。", "error")
        return redirect(url_for("index"))

    if not subject or minutes < 1 or minutes > 1440:
        flash("科目名と1〜1440分の勉強時間を入力してください。", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO study_records (study_date, subject, minutes, note) VALUES (?, ?, ?, ?)",
            (study_date, subject, minutes, note)
        )
    flash("勉強記録を追加しました！", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    with get_db() as conn:
        conn.execute("DELETE FROM study_records WHERE id = ?", (record_id,))
    flash("記録を削除しました。", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
