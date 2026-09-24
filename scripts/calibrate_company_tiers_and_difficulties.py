import os
import sys
import uuid
import sqlite3
import random
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "backend", "breakthecode.db")

# Companies segmented by Tier and Hiring Focus
TIER3_COMPANIES = [
    ("TCS", "tcs", "Tata Consultancy Services"),
    ("Wipro", "wipro", "Wipro Limited"),
    ("Infosys", "infosys", "Infosys"),
    ("Capgemini", "capgemini", "Capgemini"),
    ("GlobalLogic", "globallogic", "GlobalLogic (Hitachi Group)"),
    ("Cognizant", "cognizant", "Cognizant Technology Solutions"),
    ("Accenture", "accenture", "Accenture"),
    ("HCLTech", "hcltech", "HCL Technologies"),
    ("Tech Mahindra", "tech-mahindra", "Tech Mahindra"),
    ("LTIMindtree", "ltimindtree", "LTIMindtree")
]

TIER2_FORTUNE500_COMPANIES = [
    ("SAP", "sap", "SAP SE"),
    ("Intuit", "intuit", "Intuit Inc."),
    ("Oracle", "oracle", "Oracle Corporation"),
    ("Cisco", "cisco", "Cisco Systems"),
    ("Walmart Labs", "walmart-labs", "Walmart Global Tech"),
    ("Salesforce", "salesforce", "Salesforce"),
    ("PayPal", "paypal", "PayPal Holdings"),
    ("Adobe", "adobe", "Adobe Inc."),
    ("VMware", "vmware", "VMware Broadcom"),
    ("Dell Technologies", "dell", "Dell Technologies"),
    ("American Express", "amex", "American Express"),
    ("Target", "target", "Target Enterprise")
]

TIER1_BIGTECH_COMPANIES = [
    ("Amazon", "amazon", "Amazon / AWS"),
    ("Google", "google", "Google / Alphabet"),
    ("Meta", "meta", "Meta / Facebook"),
    ("Microsoft", "microsoft", "Microsoft"),
    ("Apple", "apple", "Apple Inc."),
    ("Netflix", "netflix", "Netflix"),
    ("Uber", "uber", "Uber Technologies"),
    ("Stripe", "stripe", "Stripe"),
    ("OpenAI", "openai", "OpenAI"),
    ("Databricks", "databricks", "Databricks")
]

ALL_COMPANIES = TIER3_COMPANIES + TIER2_FORTUNE500_COMPANIES + TIER1_BIGTECH_COMPANIES

def calibrate_companies_and_difficulty_tiers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()

    print("Step 1: Populating company tags across all tiers...")
    company_id_map = {}
    for name, slug, _ in ALL_COMPANIES:
        c.execute("SELECT id FROM tags WHERE name = ? OR slug = ?", (name, slug))
        row = c.fetchone()
        if row:
            company_id_map[name] = row[0]
        else:
            tid = str(uuid.uuid4())
            c.execute("INSERT INTO tags (id, name, slug, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", (tid, name, slug, now, now))
            company_id_map[name] = tid
    conn.commit()
    print(f"Total Companies in Catalog: {len(company_id_map)}")

    print("\nStep 2: Classifying and tagging questions based on difficulty tiers...")
    c.execute("SELECT id, difficulty, interview_depth FROM questions")
    questions = c.fetchall()

    t3_names = [x[0] for x in TIER3_COMPANIES]
    t2_names = [x[0] for x in TIER2_FORTUNE500_COMPANIES]
    t1_names = [x[0] for x in TIER1_BIGTECH_COMPANIES]

    updated_count = 0
    tags_linked = 0

    for qid, diff, depth in questions:
        diff_upper = (diff or "").upper()
        depth_upper = (depth or "").upper()

        assigned_companies = []
        role_target = "Software Engineer"
        interview_round = "Technical Interview"

        if diff_upper == "BASIC" or depth_upper == "L1":
            # Tier 3 (Mass recruiters/IT Services) + Entry-level rounds at Tier 2/1
            # e.g., TCS, Wipro, Infosys, Capgemini, GlobalLogic, SAP, Amazon Junior
            pool = t3_names * 3 + ["SAP", "Intuit", "Amazon", "Oracle", "Cisco"]
            assigned_companies = random.sample(pool, 3)
            role_target = "Junior Software Engineer / Freshers (0-2 Yrs)"
            interview_round = "Entry-Level Technical Screen / Campus Hiring"
        elif diff_upper == "MEDIUM" or depth_upper == "L2":
            # Tier 2 & Fortune 500 (SAP, Intuit, Oracle, Cisco, Walmart Labs) + Big Tech screens + TCS Digital/GlobalLogic Lead
            pool = t2_names * 2 + ["Amazon", "Microsoft", "Google", "GlobalLogic", "Capgemini", "TCS"]
            assigned_companies = random.sample(pool, 4)
            role_target = "Software Engineer / Mid-Level (3-5 Yrs)"
            interview_round = "Core Technical Round / System Design Screen"
        else:
            # Senior / Tough / Production / Expert (L3, L4, L5)
            # Tier 1 Big Tech + Top Fortune 500 Tech
            pool = t1_names * 2 + ["Salesforce", "Oracle", "Walmart Labs", "Adobe", "Intuit"]
            assigned_companies = random.sample(pool, 4)
            role_target = "Senior / Staff Software Engineer (5+ Yrs)"
            interview_round = "System Architecture & High-Scale Resilience Loop"

        # Update metadata
        c.execute("""
            UPDATE questions 
            SET role_target = ?, interview_round = ?
            WHERE id = ?
        """, (role_target, interview_round, qid))
        updated_count += 1

        # Link company tags in question_tags
        # Remove old tags for clean calibration
        c.execute("DELETE FROM question_tags WHERE question_id = ?", (qid,))
        for cname in assigned_companies:
            cid = company_id_map.get(cname)
            if cid:
                c.execute("INSERT OR IGNORE INTO question_tags (question_id, tag_id) VALUES (?, ?)", (qid, cid))
                tags_linked += 1

    conn.commit()
    print(f"Successfully calibrated {updated_count} questions.")
    print(f"Linked {tags_linked} company tags across all difficulty tiers.")

    # Audit company distribution
    print("\nCompany Question Distribution by Difficulty Tier:")
    c.execute("""
        SELECT t.name, q.difficulty, count(*)
        FROM question_tags qt
        JOIN tags t ON qt.tag_id = t.id
        JOIN questions q ON qt.question_id = q.id
        GROUP BY t.name, q.difficulty
        ORDER BY t.name, q.difficulty
    """)
    rows = c.fetchall()
    summary = {}
    for cname, diff, count in rows:
        summary.setdefault(cname, {})[diff] = count

    for cname in sorted(summary.keys())[:15]:
        diff_str = ", ".join([f"{k}: {v}" for k, v in summary[cname].items()])
        print(f"  {cname:<20} -> {diff_str}")

    conn.close()

if __name__ == "__main__":
    calibrate_companies_and_difficulty_tiers()
