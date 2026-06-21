import os
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "it_operations_center.db"))


TEXT = {
    "en": {
        "app_title": "IT Operations Center",
        "app_caption": "Bilingual helpdesk operations simulator for a small internal IT team.",
        "language": "Language",
        "technician": "Technician name",
        "page": "Page",
        "dashboard": "Dashboard",
        "users": "User Management",
        "assets": "Asset Management",
        "incidents": "Incident Tracker",
        "audit": "Audit Log",
        "ai": "AI Assistant",
        "total_users": "Total users",
        "active_users": "Active users",
        "locked_accounts": "Locked accounts",
        "disabled_accounts": "Disabled accounts",
        "total_devices": "Total devices",
        "devices_assigned": "Devices assigned",
        "devices_repair": "Devices in repair",
        "open_incidents": "Open incidents",
        "high_priority_incidents": "High priority incidents",
        "incident_status": "Incidents by status",
        "incident_priority": "Incidents by priority",
        "recent_activity": "Recent activity",
        "warranty_watch": "Warranty watch",
        "search_users": "Search users",
        "search_users_help": "Search by name, email, department, or username.",
        "select_user": "Select a user",
        "profile": "Profile",
        "actions": "Actions",
        "groups": "Groups",
        "full_name": "Full name",
        "username": "Username",
        "email": "Email",
        "department": "Department",
        "title": "Title",
        "location": "Location",
        "status": "Status",
        "mfa": "MFA enabled",
        "password_reset": "Password last reset",
        "unlock": "Unlock account",
        "reset_password": "Reset password",
        "disable": "Disable account",
        "enable": "Enable account",
        "reset_mfa": "Reset MFA",
        "add_group": "Add user to group",
        "remove_group": "Remove user from group",
        "group_name": "Group name",
        "group_to_remove": "Group to remove",
        "action_success": "Action completed and audit log updated.",
        "search_assets": "Search assets",
        "search_assets_help": "Search by asset tag, hostname, model, serial number, status, or assigned user.",
        "select_asset": "Select an asset",
        "asset_tag": "Asset tag",
        "hostname": "Hostname",
        "device_type": "Device type",
        "model": "Manufacturer / model",
        "serial": "Serial number",
        "assigned_user": "Assigned user",
        "purchase_date": "Purchase date",
        "warranty_expiry": "Warranty expiry",
        "assign_device": "Assign device to user",
        "return_storage": "Return device to storage",
        "mark_repair": "Mark device as in repair",
        "device_history": "Device history",
        "create_incident": "Create incident",
        "search_incidents": "Search incidents",
        "select_incident": "Select an incident",
        "title_field": "Title",
        "description": "Description",
        "priority": "Priority",
        "category": "Category",
        "link_user": "Link user",
        "link_asset": "Link asset",
        "notes": "Technician notes",
        "create": "Create",
        "update": "Update",
        "created": "Incident created.",
        "updated": "Incident updated.",
        "latest_logs": "Latest audit entries",
        "target": "Target",
        "details": "Details",
        "assistant_task": "Assistant task",
        "onboarding": "Generate onboarding checklist",
        "offboarding": "Generate offboarding checklist",
        "incident_checklist": "Generate troubleshooting checklist for incident category",
        "device_checklist": "Generate device troubleshooting checklist",
        "employee_department": "Employee department",
        "generate": "Generate checklist",
        "gemini_missing": "Gemini API key not found. Showing local fallback checklist.",
        "gemini_error": "Gemini is unavailable. Showing local fallback checklist.",
        "local_mode": "Local fallback mode",
        "no_results": "No matching records found.",
        "all": "All",
        "optional": "Optional",
        "none": "None",
        "about": "About",
        "about_text": "This demo uses mock data only. It does not connect to Active Directory, MDM, real ticketing systems, or company credentials.",
        "yes": "Yes",
        "no": "No",
    },
    "ja": {
        "app_title": "IT Operations Center",
        "app_caption": "小規模な社内ITチーム向けの、日英対応ヘルプデスク業務シミュレーターです。",
        "language": "言語",
        "technician": "担当者名",
        "page": "ページ",
        "dashboard": "ダッシュボード",
        "users": "ユーザー管理",
        "assets": "資産管理",
        "incidents": "インシデント管理",
        "audit": "監査ログ",
        "ai": "AIアシスタント",
        "total_users": "ユーザー総数",
        "active_users": "有効ユーザー",
        "locked_accounts": "ロック中アカウント",
        "disabled_accounts": "無効アカウント",
        "total_devices": "端末総数",
        "devices_assigned": "割当済み端末",
        "devices_repair": "修理中端末",
        "open_incidents": "未対応インシデント",
        "high_priority_incidents": "高優先度インシデント",
        "incident_status": "ステータス別インシデント",
        "incident_priority": "優先度別インシデント",
        "recent_activity": "最近の対応履歴",
        "warranty_watch": "保証期限の確認",
        "search_users": "ユーザー検索",
        "search_users_help": "氏名、メール、部署、ユーザー名で検索できます。",
        "select_user": "ユーザーを選択",
        "profile": "プロフィール",
        "actions": "操作",
        "groups": "グループ",
        "full_name": "氏名",
        "username": "ユーザー名",
        "email": "メール",
        "department": "部署",
        "title": "役職",
        "location": "勤務地",
        "status": "ステータス",
        "mfa": "MFA有効",
        "password_reset": "最終パスワードリセット",
        "unlock": "アカウントロック解除",
        "reset_password": "パスワードリセット",
        "disable": "アカウント無効化",
        "enable": "アカウント有効化",
        "reset_mfa": "MFAリセット",
        "add_group": "グループ追加",
        "remove_group": "グループ削除",
        "group_name": "グループ名",
        "group_to_remove": "削除するグループ",
        "action_success": "操作が完了し、監査ログを記録しました。",
        "search_assets": "資産検索",
        "search_assets_help": "資産タグ、ホスト名、モデル、シリアル番号、ステータス、利用者で検索できます。",
        "select_asset": "資産を選択",
        "asset_tag": "資産タグ",
        "hostname": "ホスト名",
        "device_type": "端末種別",
        "model": "メーカー / モデル",
        "serial": "シリアル番号",
        "assigned_user": "利用者",
        "purchase_date": "購入日",
        "warranty_expiry": "保証期限",
        "assign_device": "端末をユーザーへ割り当て",
        "return_storage": "端末を保管状態へ戻す",
        "mark_repair": "修理中として登録",
        "device_history": "端末履歴",
        "create_incident": "インシデント作成",
        "search_incidents": "インシデント検索",
        "select_incident": "インシデントを選択",
        "title_field": "件名",
        "description": "内容",
        "priority": "優先度",
        "category": "カテゴリ",
        "link_user": "関連ユーザー",
        "link_asset": "関連資産",
        "notes": "担当者メモ",
        "create": "作成",
        "update": "更新",
        "created": "インシデントを作成しました。",
        "updated": "インシデントを更新しました。",
        "latest_logs": "最新の監査ログ",
        "target": "対象",
        "details": "詳細",
        "assistant_task": "アシスタント機能",
        "onboarding": "入社対応チェックリストを作成",
        "offboarding": "退職対応チェックリストを作成",
        "incident_checklist": "カテゴリ別トラブルシュート手順を作成",
        "device_checklist": "端末種別別トラブルシュート手順を作成",
        "employee_department": "社員の部署",
        "generate": "チェックリスト作成",
        "gemini_missing": "Gemini APIキーが未設定のため、ローカルの標準チェックリストを表示します。",
        "gemini_error": "Geminiを利用できないため、ローカルの標準チェックリストを表示します。",
        "local_mode": "ローカル代替モード",
        "no_results": "一致するレコードがありません。",
        "all": "すべて",
        "optional": "任意",
        "none": "なし",
        "about": "概要",
        "about_text": "このデモはすべてサンプルデータです。Active Directory、MDM、実際のチケット管理システム、会社の認証情報には接続しません。",
        "yes": "はい",
        "no": "いいえ",
    },
}

STATUS_JA = {
    "Active": "有効",
    "Locked": "ロック中",
    "Disabled": "無効",
    "In Use": "使用中",
    "In Storage": "保管中",
    "In Repair": "修理中",
    "Retired": "廃棄済み",
    "Open": "未対応",
    "In Progress": "対応中",
    "Resolved": "解決済み",
    "Low": "低",
    "Medium": "中",
    "High": "高",
    "Critical": "緊急",
    "Account": "アカウント",
    "Hardware": "ハードウェア",
    "Software": "ソフトウェア",
    "Network": "ネットワーク",
    "Email": "メール",
    "Security": "セキュリティ",
    "Other": "その他",
    "Laptop": "ノートPC",
    "Desktop": "デスクトップPC",
    "Monitor": "モニター",
    "Printer": "プリンター",
    "Mobile": "モバイル端末",
    "Network Device": "ネットワーク機器",
}


def tr(key: str) -> str:
    return TEXT[st.session_state.get("lang", "en")].get(key, key)


def display_value(value):
    if st.session_state.get("lang") == "ja":
        return STATUS_JA.get(str(value), value)
    return value


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def read_df(query: str, params=()):
    with get_conn() as conn:
        return pd.read_sql_query(query, conn, params=params)


def execute(query: str, params=()):
    with get_conn() as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid


def log_audit(technician, action, target_type, target_id, details):
    execute(
        """
        INSERT INTO audit_logs (timestamp, technician, action, target_type, target_id, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (now_text(), technician, action, target_type, str(target_id), details),
    )


def log_device_history(technician, asset_id, action, details):
    execute(
        """
        INSERT INTO device_history (timestamp, technician, asset_id, action, details)
        VALUES (?, ?, ?, ?, ?)
        """,
        (now_text(), technician, asset_id, action, details),
    )


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL,
                mfa_enabled INTEGER NOT NULL DEFAULT 1,
                groups TEXT NOT NULL DEFAULT '',
                password_last_reset TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_tag TEXT NOT NULL UNIQUE,
                hostname TEXT NOT NULL UNIQUE,
                device_type TEXT NOT NULL,
                manufacturer_model TEXT NOT NULL,
                serial_number TEXT NOT NULL UNIQUE,
                assigned_user_id INTEGER,
                status TEXT NOT NULL,
                purchase_date TEXT NOT NULL,
                warranty_expiry TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (assigned_user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                category TEXT NOT NULL,
                user_id INTEGER,
                asset_id INTEGER,
                technician_notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                resolved_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (asset_id) REFERENCES assets(id)
            );

            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                technician TEXT NOT NULL,
                action TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                details TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS device_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                technician TEXT NOT NULL,
                asset_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                FOREIGN KEY (asset_id) REFERENCES assets(id)
            );
            """
        )
        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count == 0:
            seed_data(conn)
        conn.commit()


def seed_data(conn):
    timestamp = now_text()
    users = [
        ("Aiko Tanaka", "atanaka", "aiko.tanaka@example.local", "Sales", "Sales Coordinator", "Tokyo HQ", "Active", 1, "All Staff,Sales"),
        ("Kenji Sato", "ksato", "kenji.sato@example.local", "Finance", "Accountant", "Tokyo HQ", "Locked", 1, "All Staff,Finance"),
        ("Mika Suzuki", "msuzuki", "mika.suzuki@example.local", "HR", "HR Specialist", "Osaka Office", "Active", 1, "All Staff,HR"),
        ("Daniel Kim", "dkim", "daniel.kim@example.local", "Engineering", "Junior Developer", "Tokyo HQ", "Disabled", 0, "All Staff,Engineering"),
        ("Yuki Nakamura", "ynakamura", "yuki.nakamura@example.local", "Operations", "Operations Assistant", "Nagoya Office", "Active", 1, "All Staff,Operations"),
        ("Hana Ito", "hito", "hana.ito@example.local", "Marketing", "Marketing Associate", "Tokyo HQ", "Active", 1, "All Staff,Marketing"),
    ]
    conn.executemany(
        """
        INSERT INTO users (
            full_name, username, email, department, title, location, status, mfa_enabled,
            groups, password_last_reset, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(u + ("2026-06-01 09:00:00", timestamp, timestamp)) for u in users],
    )

    user_ids = {row["username"]: row["id"] for row in conn.execute("SELECT id, username FROM users")}
    assets = [
        ("JP-LT-001", "TKY-LT-001", "Laptop", "Lenovo ThinkPad E14", "LNV-E14-001", user_ids["atanaka"], "In Use", "2024-04-10", "2027-04-09"),
        ("JP-LT-002", "TKY-LT-002", "Laptop", "Dell Latitude 5440", "DLL-5440-002", user_ids["ksato"], "In Use", "2024-06-15", "2027-06-14"),
        ("JP-DT-003", "OSK-DT-003", "Desktop", "HP EliteDesk 800", "HP-800-003", user_ids["msuzuki"], "In Use", "2023-11-20", "2026-11-19"),
        ("JP-MN-004", "TKY-MON-004", "Monitor", "Dell P2422H", "MON-2422-004", None, "In Storage", "2023-07-05", "2026-07-04"),
        ("JP-PR-005", "NGY-PRN-005", "Printer", "Brother MFC-L9570CDW", "BR-MFC-005", None, "In Repair", "2022-09-01", "2025-08-31"),
        ("JP-MB-006", "TKY-IP-006", "Mobile", "Apple iPhone SE", "APL-SE-006", user_ids["hito"], "In Use", "2025-01-12", "2027-01-11"),
    ]
    conn.executemany(
        """
        INSERT INTO assets (
            asset_tag, hostname, device_type, manufacturer_model, serial_number, assigned_user_id,
            status, purchase_date, warranty_expiry, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(a + (timestamp, timestamp)) for a in assets],
    )

    asset_ids = {row["asset_tag"]: row["id"] for row in conn.execute("SELECT id, asset_tag FROM assets")}
    incidents = [
        ("Account locked after password attempts", "User cannot sign in after multiple password attempts.", "Open", "High", "Account", user_ids["ksato"], None, "Verify identity before unlocking account."),
        ("Printer is showing paper jam", "Nagoya office printer reports jam even after removing paper.", "In Progress", "Medium", "Hardware", None, asset_ids["JP-PR-005"], "Asked office admin to confirm error code."),
        ("New hire laptop setup", "Prepare laptop and standard access for incoming Operations employee.", "Open", "Low", "Other", user_ids["ynakamura"], asset_ids["JP-MN-004"], ""),
        ("Suspicious email reported", "User reported a suspicious attachment from an unknown sender.", "Resolved", "Critical", "Security", user_ids["hito"], None, "Confirmed phishing simulation; user completed awareness reminder."),
    ]
    conn.executemany(
        """
        INSERT INTO incidents (
            title, description, status, priority, category, user_id, asset_id,
            technician_notes, created_at, updated_at, resolved_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            i + (timestamp, timestamp, timestamp if i[2] == "Resolved" else None)
            for i in incidents
        ],
    )

    conn.execute(
        """
        INSERT INTO audit_logs (timestamp, technician, action, target_type, target_id, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (timestamp, "System", "Initialize database", "Database", "seed", "Created sample users, assets, incidents, and history."),
    )
    for asset_id, action, details in [
        (asset_ids["JP-LT-001"], "Assigned", "Assigned to Aiko Tanaka during onboarding."),
        (asset_ids["JP-PR-005"], "Repair", "Marked in repair after recurring paper jam errors."),
        (asset_ids["JP-MN-004"], "Storage", "Returned to storage after desk move."),
    ]:
        conn.execute(
            """
            INSERT INTO device_history (timestamp, technician, asset_id, action, details)
            VALUES (?, ?, ?, ?, ?)
            """,
            (timestamp, "System", asset_id, action, details),
        )


def metric_value(query):
    df = read_df(query)
    return int(df.iloc[0, 0])


def render_dashboard():
    st.header(tr("dashboard"))
    col1, col2, col3 = st.columns(3)
    col1.metric(tr("total_users"), metric_value("SELECT COUNT(*) FROM users"))
    col2.metric(tr("active_users"), metric_value("SELECT COUNT(*) FROM users WHERE status = 'Active'"))
    col3.metric(tr("locked_accounts"), metric_value("SELECT COUNT(*) FROM users WHERE status = 'Locked'"))

    col4, col5, col6 = st.columns(3)
    col4.metric(tr("disabled_accounts"), metric_value("SELECT COUNT(*) FROM users WHERE status = 'Disabled'"))
    col5.metric(tr("total_devices"), metric_value("SELECT COUNT(*) FROM assets"))
    col6.metric(tr("devices_assigned"), metric_value("SELECT COUNT(*) FROM assets WHERE assigned_user_id IS NOT NULL"))

    col7, col8, col9 = st.columns(3)
    col7.metric(tr("devices_repair"), metric_value("SELECT COUNT(*) FROM assets WHERE status = 'In Repair'"))
    col8.metric(tr("open_incidents"), metric_value("SELECT COUNT(*) FROM incidents WHERE status != 'Resolved'"))
    col9.metric(tr("high_priority_incidents"), metric_value("SELECT COUNT(*) FROM incidents WHERE priority IN ('High', 'Critical') AND status != 'Resolved'"))

    left, right = st.columns(2)
    with left:
        st.subheader(tr("incident_status"))
        status_df = read_df("SELECT status, COUNT(*) AS count FROM incidents GROUP BY status")
        if not status_df.empty:
            status_df["status"] = status_df["status"].map(display_value)
            st.bar_chart(status_df.set_index("status"))
    with right:
        st.subheader(tr("incident_priority"))
        priority_df = read_df("SELECT priority, COUNT(*) AS count FROM incidents GROUP BY priority")
        if not priority_df.empty:
            priority_df["priority"] = priority_df["priority"].map(display_value)
            st.bar_chart(priority_df.set_index("priority"))

    left, right = st.columns(2)
    with left:
        st.subheader(tr("recent_activity"))
        logs = read_df("SELECT timestamp, technician, action, target_type, details FROM audit_logs ORDER BY id DESC LIMIT 8")
        st.dataframe(logs, use_container_width=True, hide_index=True)
    with right:
        st.subheader(tr("warranty_watch"))
        warranties = read_df(
            """
            SELECT asset_tag, hostname, device_type, warranty_expiry, status
            FROM assets
            ORDER BY warranty_expiry ASC
            LIMIT 8
            """
        )
        warranties["device_type"] = warranties["device_type"].map(display_value)
        warranties["status"] = warranties["status"].map(display_value)
        st.dataframe(warranties, use_container_width=True, hide_index=True)


def get_user_options(include_none=False):
    users = read_df("SELECT id, full_name, username, department FROM users ORDER BY full_name")
    options = {}
    if include_none:
        options[tr("none")] = None
    for _, row in users.iterrows():
        options[f"{row['full_name']} ({row['username']}) - {row['department']}"] = int(row["id"])
    return options


def get_asset_options(include_none=False):
    assets = read_df("SELECT id, asset_tag, hostname, device_type, status FROM assets ORDER BY asset_tag")
    options = {}
    if include_none:
        options[tr("none")] = None
    for _, row in assets.iterrows():
        options[f"{row['asset_tag']} / {row['hostname']} - {display_value(row['device_type'])} ({display_value(row['status'])})"] = int(row["id"])
    return options


def render_user_management(technician):
    st.header(tr("users"))
    search = st.text_input(tr("search_users"), help=tr("search_users_help"))
    pattern = f"%{search.strip()}%"
    users = read_df(
        """
        SELECT * FROM users
        WHERE full_name LIKE ? OR email LIKE ? OR department LIKE ? OR username LIKE ?
        ORDER BY full_name
        """,
        (pattern, pattern, pattern, pattern),
    )
    if users.empty:
        st.info(tr("no_results"))
        return

    user_map = {
        f"{row['full_name']} ({row['username']}) - {display_value(row['status'])}": int(row["id"])
        for _, row in users.iterrows()
    }
    selected_label = st.selectbox(tr("select_user"), list(user_map.keys()))
    user_id = user_map[selected_label]
    user = read_df("SELECT * FROM users WHERE id = ?", (user_id,)).iloc[0]

    tab_profile, tab_actions, tab_groups = st.tabs([tr("profile"), tr("actions"), tr("groups")])
    with tab_profile:
        col1, col2 = st.columns(2)
        col1.write(f"**{tr('full_name')}:** {user['full_name']}")
        col1.write(f"**{tr('username')}:** {user['username']}")
        col1.write(f"**{tr('email')}:** {user['email']}")
        col2.write(f"**{tr('department')}:** {user['department']}")
        col2.write(f"**{tr('title')}:** {user['title']}")
        col2.write(f"**{tr('location')}:** {user['location']}")
        st.write(f"**{tr('status')}:** {display_value(user['status'])}")
        st.write(f"**{tr('mfa')}:** {tr('yes') if user['mfa_enabled'] else tr('no')}")
        st.write(f"**{tr('password_reset')}:** {user['password_last_reset']}")

    with tab_actions:
        cols = st.columns(3)
        if cols[0].button(tr("unlock"), disabled=user["status"] != "Locked", use_container_width=True):
            update_user_status(user_id, "Active", technician, "Unlock account", f"Unlocked {user['username']}.")
        if cols[1].button(tr("reset_password"), use_container_width=True):
            execute("UPDATE users SET password_last_reset = ?, updated_at = ? WHERE id = ?", (now_text(), now_text(), user_id))
            log_audit(technician, "Reset password", "User", user_id, f"Simulated password reset for {user['username']}.")
            st.success(tr("action_success"))
            st.rerun()
        if cols[2].button(tr("reset_mfa"), use_container_width=True):
            execute("UPDATE users SET mfa_enabled = 1, updated_at = ? WHERE id = ?", (now_text(), user_id))
            log_audit(technician, "Reset MFA", "User", user_id, f"Reset MFA registration for {user['username']}.")
            st.success(tr("action_success"))
            st.rerun()

        cols = st.columns(2)
        if cols[0].button(tr("disable"), disabled=user["status"] == "Disabled", use_container_width=True):
            update_user_status(user_id, "Disabled", technician, "Disable account", f"Disabled {user['username']}.")
        if cols[1].button(tr("enable"), disabled=user["status"] == "Active", use_container_width=True):
            update_user_status(user_id, "Active", technician, "Enable account", f"Enabled {user['username']}.")

    with tab_groups:
        groups = [g.strip() for g in str(user["groups"]).split(",") if g.strip()]
        st.write(", ".join(groups) if groups else tr("none"))

        with st.form("add_group_form"):
            group_name = st.text_input(tr("group_name"), placeholder="VPN Users")
            submitted = st.form_submit_button(tr("add_group"))
            if submitted and group_name.strip():
                new_groups = sorted(set(groups + [group_name.strip()]))
                execute("UPDATE users SET groups = ?, updated_at = ? WHERE id = ?", (",".join(new_groups), now_text(), user_id))
                log_audit(technician, "Add group", "User", user_id, f"Added {user['username']} to group {group_name.strip()}.")
                st.success(tr("action_success"))
                st.rerun()

        if groups:
            with st.form("remove_group_form"):
                group_to_remove = st.selectbox(tr("group_to_remove"), groups)
                submitted = st.form_submit_button(tr("remove_group"))
                if submitted:
                    new_groups = [g for g in groups if g != group_to_remove]
                    execute("UPDATE users SET groups = ?, updated_at = ? WHERE id = ?", (",".join(new_groups), now_text(), user_id))
                    log_audit(technician, "Remove group", "User", user_id, f"Removed {user['username']} from group {group_to_remove}.")
                    st.success(tr("action_success"))
                    st.rerun()


def update_user_status(user_id, status, technician, action, details):
    execute("UPDATE users SET status = ?, updated_at = ? WHERE id = ?", (status, now_text(), user_id))
    log_audit(technician, action, "User", user_id, details)
    st.success(tr("action_success"))
    st.rerun()


def render_asset_management(technician):
    st.header(tr("assets"))
    search = st.text_input(tr("search_assets"), help=tr("search_assets_help"))
    pattern = f"%{search.strip()}%"
    assets = read_df(
        """
        SELECT a.*, u.full_name AS assigned_user
        FROM assets a
        LEFT JOIN users u ON a.assigned_user_id = u.id
        WHERE a.asset_tag LIKE ? OR a.hostname LIKE ? OR a.manufacturer_model LIKE ?
           OR a.serial_number LIKE ? OR a.status LIKE ? OR COALESCE(u.full_name, '') LIKE ?
        ORDER BY a.asset_tag
        """,
        (pattern, pattern, pattern, pattern, pattern, pattern),
    )
    if assets.empty:
        st.info(tr("no_results"))
        return

    asset_map = {
        f"{row['asset_tag']} / {row['hostname']} - {display_value(row['status'])}": int(row["id"])
        for _, row in assets.iterrows()
    }
    selected_label = st.selectbox(tr("select_asset"), list(asset_map.keys()))
    asset_id = asset_map[selected_label]
    asset = read_df(
        """
        SELECT a.*, u.full_name AS assigned_user
        FROM assets a
        LEFT JOIN users u ON a.assigned_user_id = u.id
        WHERE a.id = ?
        """,
        (asset_id,),
    ).iloc[0]

    tab_profile, tab_actions, tab_history = st.tabs([tr("profile"), tr("actions"), tr("device_history")])
    with tab_profile:
        col1, col2 = st.columns(2)
        col1.write(f"**{tr('asset_tag')}:** {asset['asset_tag']}")
        col1.write(f"**{tr('hostname')}:** {asset['hostname']}")
        col1.write(f"**{tr('device_type')}:** {display_value(asset['device_type'])}")
        col1.write(f"**{tr('model')}:** {asset['manufacturer_model']}")
        col2.write(f"**{tr('serial')}:** {asset['serial_number']}")
        col2.write(f"**{tr('assigned_user')}:** {asset['assigned_user'] or tr('none')}")
        col2.write(f"**{tr('status')}:** {display_value(asset['status'])}")
        col2.write(f"**{tr('warranty_expiry')}:** {asset['warranty_expiry']}")

    with tab_actions:
        user_options = get_user_options()
        with st.form("assign_asset_form"):
            selected_user = st.selectbox(tr("assign_device"), list(user_options.keys()))
            submitted = st.form_submit_button(tr("assign_device"))
            if submitted:
                assigned_user_id = user_options[selected_user]
                execute(
                    "UPDATE assets SET assigned_user_id = ?, status = 'In Use', updated_at = ? WHERE id = ?",
                    (assigned_user_id, now_text(), asset_id),
                )
                details = f"Assigned {asset['asset_tag']} to {selected_user}."
                log_audit(technician, "Assign device", "Asset", asset_id, details)
                log_device_history(technician, asset_id, "Assigned", details)
                st.success(tr("action_success"))
                st.rerun()

        col1, col2 = st.columns(2)
        if col1.button(tr("return_storage"), use_container_width=True):
            execute("UPDATE assets SET assigned_user_id = NULL, status = 'In Storage', updated_at = ? WHERE id = ?", (now_text(), asset_id))
            details = f"Returned {asset['asset_tag']} to storage."
            log_audit(technician, "Return device", "Asset", asset_id, details)
            log_device_history(technician, asset_id, "Returned", details)
            st.success(tr("action_success"))
            st.rerun()
        if col2.button(tr("mark_repair"), use_container_width=True):
            execute("UPDATE assets SET status = 'In Repair', updated_at = ? WHERE id = ?", (now_text(), asset_id))
            details = f"Marked {asset['asset_tag']} as in repair."
            log_audit(technician, "Mark repair", "Asset", asset_id, details)
            log_device_history(technician, asset_id, "Repair", details)
            st.success(tr("action_success"))
            st.rerun()

    with tab_history:
        history = read_df(
            """
            SELECT timestamp, technician, action, details
            FROM device_history
            WHERE asset_id = ?
            ORDER BY id DESC
            """,
            (asset_id,),
        )
        st.dataframe(history, use_container_width=True, hide_index=True)


def render_incident_tracker(technician):
    st.header(tr("incidents"))
    tab_create, tab_search = st.tabs([tr("create_incident"), tr("search_incidents")])

    user_options = get_user_options(include_none=True)
    asset_options = get_asset_options(include_none=True)
    priorities = ["Low", "Medium", "High", "Critical"]
    categories = ["Account", "Hardware", "Software", "Network", "Email", "Security", "Other"]
    statuses = ["Open", "In Progress", "Resolved"]

    with tab_create:
        with st.form("create_incident_form"):
            title = st.text_input(tr("title_field"))
            description = st.text_area(tr("description"))
            col1, col2 = st.columns(2)
            priority = col1.selectbox(tr("priority"), priorities, format_func=display_value, index=1)
            category = col2.selectbox(tr("category"), categories, format_func=display_value)
            linked_user = st.selectbox(tr("link_user"), list(user_options.keys()))
            linked_asset = st.selectbox(tr("link_asset"), list(asset_options.keys()))
            notes = st.text_area(tr("notes"))
            submitted = st.form_submit_button(tr("create"))
            if submitted and title.strip() and description.strip():
                incident_id = execute(
                    """
                    INSERT INTO incidents (
                        title, description, status, priority, category, user_id, asset_id,
                        technician_notes, created_at, updated_at
                    )
                    VALUES (?, ?, 'Open', ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        title.strip(),
                        description.strip(),
                        priority,
                        category,
                        user_options[linked_user],
                        asset_options[linked_asset],
                        notes.strip(),
                        now_text(),
                        now_text(),
                    ),
                )
                log_audit(technician, "Create incident", "Incident", incident_id, f"Created incident: {title.strip()}.")
                st.success(tr("created"))
                st.rerun()

    with tab_search:
        search = st.text_input(tr("search_incidents"))
        pattern = f"%{search.strip()}%"
        incidents = read_df(
            """
            SELECT i.*, u.full_name AS user_name, a.asset_tag AS asset_tag
            FROM incidents i
            LEFT JOIN users u ON i.user_id = u.id
            LEFT JOIN assets a ON i.asset_id = a.id
            WHERE i.title LIKE ? OR i.description LIKE ? OR i.status LIKE ?
               OR i.priority LIKE ? OR i.category LIKE ? OR COALESCE(u.full_name, '') LIKE ?
               OR COALESCE(a.asset_tag, '') LIKE ?
            ORDER BY i.updated_at DESC
            """,
            (pattern, pattern, pattern, pattern, pattern, pattern, pattern),
        )
        if incidents.empty:
            st.info(tr("no_results"))
            return

        incident_map = {
            f"#{row['id']} {row['title']} - {display_value(row['status'])} / {display_value(row['priority'])}": int(row["id"])
            for _, row in incidents.iterrows()
        }
        selected_incident = st.selectbox(tr("select_incident"), list(incident_map.keys()))
        incident_id = incident_map[selected_incident]
        incident = incidents[incidents["id"] == incident_id].iloc[0]

        st.write(f"**{tr('description')}:** {incident['description']}")
        st.write(f"**{tr('link_user')}:** {incident['user_name'] or tr('none')}")
        st.write(f"**{tr('link_asset')}:** {incident['asset_tag'] or tr('none')}")

        with st.form("update_incident_form"):
            new_status = st.selectbox(tr("status"), statuses, index=statuses.index(incident["status"]), format_func=display_value)
            new_priority = st.selectbox(tr("priority"), priorities, index=priorities.index(incident["priority"]), format_func=display_value)
            new_notes = st.text_area(tr("notes"), value=incident["technician_notes"] or "")
            submitted = st.form_submit_button(tr("update"))
            if submitted:
                resolved_at = now_text() if new_status == "Resolved" else None
                execute(
                    """
                    UPDATE incidents
                    SET status = ?, priority = ?, technician_notes = ?, updated_at = ?, resolved_at = ?
                    WHERE id = ?
                    """,
                    (new_status, new_priority, new_notes, now_text(), resolved_at, incident_id),
                )
                log_audit(
                    technician,
                    "Update incident",
                    "Incident",
                    incident_id,
                    f"Updated status to {new_status}, priority to {new_priority}.",
                )
                st.success(tr("updated"))
                st.rerun()


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def fallback_checklist(task, language, category=None, device_type=None, department=None):
    ja = language == "ja"
    if task == "onboarding":
        if ja:
            return [
                f"{department or '配属部署'}の上長に開始日と必要な権限を確認する。",
                "標準PC、ACアダプター、周辺機器を準備し、資産タグを確認する。",
                "メール、MFA、VPN、チャット、業務アプリの初期設定を確認する。",
                "初回ログイン、パスワード変更、MFA登録をユーザーと一緒に確認する。",
                "完了した作業をチケットと監査ログに記録する。",
            ]
        return [
            f"Confirm start date and required access with the {department or 'employee'} manager.",
            "Prepare standard laptop, charger, peripherals, and verify the asset tag.",
            "Confirm email, MFA, VPN, chat, and required business apps are ready.",
            "Walk through first login, password change, and MFA registration with the user.",
            "Record completed steps in the ticket and audit trail.",
        ]
    if task == "offboarding":
        if ja:
            return [
                "退職日時とアカウント停止タイミングを人事または上長に確認する。",
                "アカウントを無効化し、MFA、VPN、メール、業務アプリのアクセスを停止する。",
                "貸与端末、充電器、入館証、モバイル端末の返却状況を確認する。",
                "必要に応じてメール転送、共有メールボックス、データ引き継ぎを確認する。",
                "実施内容をインシデントまたは作業記録へ残す。",
            ]
        return [
            "Confirm departure date and account disable timing with HR or the manager.",
            "Disable account access for MFA, VPN, email, and business applications.",
            "Confirm return of laptop, charger, badge, and mobile devices.",
            "Verify mailbox forwarding, shared mailbox access, or data handover if required.",
            "Document completed actions in the ticket or work log.",
        ]
    if task == "incident":
        if ja:
            return [
                f"{display_value(category)}の影響範囲、発生時刻、再現手順を確認する。",
                "ユーザー本人確認を行い、エラーメッセージやスクリーンショットを取得する。",
                "基本切り分けを実施し、アカウント、端末、ネットワーク、アプリのどこに原因が近いか整理する。",
                "既知の手順で復旧できない場合は、影響度と実施済み対応を添えてエスカレーションする。",
                "対応内容、結果、次回アクションをチケットに記録する。",
            ]
        return [
            f"Confirm impact, start time, and reproduction steps for the {category} issue.",
            "Verify the user and collect the exact error message or screenshots.",
            "Run basic isolation to identify whether the issue is account, device, network, or application related.",
            "Escalate with impact and completed steps if standard procedures do not resolve it.",
            "Record actions, outcome, and next steps in the ticket.",
        ]
    if ja:
        return [
            f"{display_value(device_type)}の利用者、設置場所、資産タグ、保証期限を確認する。",
            "電源、ケーブル、ネットワーク接続、最近の変更点を確認する。",
            "再起動、アップデート、ドライバー、空き容量、エラーログなど基本項目を確認する。",
            "必要に応じて代替機を手配し、業務影響を最小化する。",
            "修理、交換、返却などの対応履歴を資産管理に記録する。",
        ]
    return [
        f"Confirm assigned user, location, asset tag, and warranty status for the {device_type}.",
        "Check power, cables, network connection, and recent changes.",
        "Review restart status, updates, drivers, free disk space, and error logs.",
        "Arrange a loaner device if needed to reduce business impact.",
        "Record repair, replacement, or return history in asset management.",
    ]


def generate_with_gemini(prompt):
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        return None, "missing"
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text, None
    except Exception:
        return None, "error"


def render_ai_assistant():
    st.header(tr("ai"))
    task_labels = {
        tr("onboarding"): "onboarding",
        tr("offboarding"): "offboarding",
        tr("incident_checklist"): "incident",
        tr("device_checklist"): "device",
    }
    task_label = st.selectbox(tr("assistant_task"), list(task_labels.keys()))
    task = task_labels[task_label]

    department = None
    category = None
    device_type = None
    if task in {"onboarding", "offboarding"}:
        department = st.text_input(tr("employee_department"), value="Sales")
    if task == "incident":
        category = st.selectbox(tr("category"), ["Account", "Hardware", "Software", "Network", "Email", "Security", "Other"], format_func=display_value)
    if task == "device":
        device_type = st.selectbox(tr("device_type"), ["Laptop", "Desktop", "Monitor", "Printer", "Mobile", "Network Device"], format_func=display_value)

    if st.button(tr("generate")):
        language_name = "Japanese" if st.session_state.get("lang") == "ja" else "English"
        prompt = (
            f"Create a concise, realistic IT helpdesk checklist in {language_name}. "
            "Use professional language suitable for an entry-level IT Support portfolio demo. "
            "Do not mention real credentials, real Active Directory changes, or private company data. "
            f"Task: {task}. Department: {department or 'N/A'}. "
            f"Incident category: {category or 'N/A'}. Device type: {device_type or 'N/A'}. "
            "Return 5-7 checklist bullets only."
        )
        text, error = generate_with_gemini(prompt)
        if text:
            st.markdown(text)
        else:
            st.info(tr("gemini_missing") if error == "missing" else tr("gemini_error"))
            st.caption(tr("local_mode"))
            checklist = fallback_checklist(task, st.session_state.get("lang"), category, device_type, department)
            for item in checklist:
                st.checkbox(item, value=False)


def render_audit_log():
    st.header(tr("audit"))
    logs = read_df(
        """
        SELECT timestamp, technician, action, target_type, target_id, details
        FROM audit_logs
        ORDER BY id DESC
        LIMIT 200
        """
    )
    st.dataframe(logs, use_container_width=True, hide_index=True)


def main():
    st.set_page_config(page_title="IT Operations Center", page_icon=":computer:", layout="wide")
    init_db()

    if "lang" not in st.session_state:
        st.session_state.lang = "en"

    language_label = st.sidebar.selectbox(
        TEXT[st.session_state.lang]["language"],
        ["English", "日本語"],
        index=0 if st.session_state.lang == "en" else 1,
    )
    st.session_state.lang = "ja" if language_label == "日本語" else "en"

    technician = st.sidebar.text_input(tr("technician"), value="Helpdesk Technician")
    pages = {
        tr("dashboard"): render_dashboard,
        tr("users"): lambda: render_user_management(technician),
        tr("assets"): lambda: render_asset_management(technician),
        tr("incidents"): lambda: render_incident_tracker(technician),
        tr("audit"): render_audit_log,
        tr("ai"): render_ai_assistant,
    }
    page = st.sidebar.radio(tr("page"), list(pages.keys()))

    with st.sidebar.expander(tr("about")):
        st.write(tr("about_text"))

    st.title(tr("app_title"))
    st.caption(tr("app_caption"))
    pages[page]()


if __name__ == "__main__":
    main()
