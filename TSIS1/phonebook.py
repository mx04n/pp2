import csv, json
import psycopg2, psycopg2.extras
from connect import get_connection
from config import PAGE_SIZE
 
 
def get_conn():
    return get_connection()
 
 
def init_db(conn):
    cur = conn.cursor()
    for f in ("schema.sql", "procedures.sql"):
        cur.execute(open(f).read())
    conn.commit()
    cur.close()
 
 
def resolve_group(cur, name):
    cur.execute("SELECT id FROM groups WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (name,))
    return cur.fetchone()[0]
 
 
def add_contact(conn, name, email=None, birthday=None, group=None):
    cur = conn.cursor()
    gid = resolve_group(cur, group) if group else None
    cur.execute(
        "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (name, email, birthday, gid)
    )
    cid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return cid
 
 
def add_phone(conn, contact_name, phone, ptype):
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, ptype))
    conn.commit()
    cur.close()
 
 
def move_to_group(conn, contact_name, group_name):
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
    conn.commit()
    cur.close()
 
 
def delete_contact(conn, name):
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    n = cur.rowcount
    conn.commit()
    cur.close()
    return n
 
 
def search(conn, query):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    cur.close()
    return rows
 
 
def list_contacts(conn, group=None, email=None, sort="name", page=1):
    if sort not in ("name", "birthday", "created_at"):
        sort = "name"
    where, params = [], []
    if group:
        where.append("g.name ILIKE %s"); params.append(group)
    if email:
        where.append("c.email ILIKE %s"); params.append(f"%{email}%")
    w = "WHERE " + " AND ".join(where) if where else ""
 
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(DISTINCT c.id) FROM contacts c LEFT JOIN groups g ON g.id=c.group_id {w}", params)
    total = cur.fetchone()[0]
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, total_pages))
 
    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name AS grp, c.created_at,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ') AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {w}
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY c.{sort} NULLS LAST
        LIMIT %s OFFSET %s
    """, params + [PAGE_SIZE, (page - 1) * PAGE_SIZE])
    rows = cur.fetchall()
    cur.close()
    return rows, total_pages, page
 
 
def export_json(conn, path="contacts.json"):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT c.name, c.email, c.birthday::TEXT, g.name AS grp,
               JSON_AGG(JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type))
               FILTER (WHERE p.id IS NOT NULL) AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
    """)
    data = [dict(r) for r in cur.fetchall()]
    cur.close()
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Exported {len(data)} contacts → {path}")
 
 
def import_json(conn, path="contacts.json"):
    data = json.load(open(path, encoding="utf-8"))
    cur = conn.cursor()
    added = skipped = overwritten = 0
    for item in data:
        name = item.get("name", "").strip()
        if not name:
            continue
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()
        if existing:
            ans = input(f'"{name}" exists. [s]kip/[o]verwrite? ').strip().lower()
            if ans != "o":
                skipped += 1
                continue
            cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
            overwritten += 1
        else:
            added += 1
        gid = resolve_group(cur, item["grp"]) if item.get("grp") else None
        cur.execute(
            "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
            (name, item.get("email"), item.get("birthday"), gid)
        )
        cid = cur.fetchone()[0]
        for ph in item.get("phones") or []:
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                        (cid, ph.get("phone"), ph.get("type")))
    conn.commit()
    cur.close()
    print(f"Done: {added} added, {overwritten} overwritten, {skipped} skipped.")
 
 
def import_csv(conn, path="contacts.csv"):
    cur = conn.cursor()
    added = 0
    for row in csv.DictReader(open(path, encoding="utf-8")):
        name = row.get("name", "").strip()
        if not name:
            continue
        gid = resolve_group(cur, row["group"]) if row.get("group") else None
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()
        if existing:
            cid = existing[0]
            cur.execute("UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                        (row.get("email"), row.get("birthday") or None, gid, cid))
        else:
            cur.execute(
                "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                (name, row.get("email"), row.get("birthday") or None, gid)
            )
            cid = cur.fetchone()[0]
            added += 1
        if row.get("phone"):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                        (cid, row["phone"], row.get("phone_type") or None))
    conn.commit()
    cur.close()
    print(f"CSV import done: {added} new contacts.")
 
 
def print_contact(row):
    r = dict(zip(["id","name","email","birthday","grp","created_at","phones"], row)) \
        if not hasattr(row, "keys") else dict(row)
    print(f"  [{r.get('id','-')}] {r.get('name','?')}")
    for key, label in [("email","Email"), ("birthday","Birthday"), ("grp","Group"), ("phones","Phones")]:
        if r.get(key):
            print(f"       {label}: {r[key]}")
    print()
 
 
def menu_list(conn):
    group = input("Filter by group (blank=all): ").strip() or None
    email = input("Filter by email (blank=all): ").strip() or None
    sort  = {"1":"name","2":"birthday","3":"created_at"}.get(
        input("Sort: (1)name (2)birthday (3)date added [1]: ").strip(), "name")
    page = 1
    while True:
        rows, total_pages, page = list_contacts(conn, group=group, email=email, sort=sort, page=page)
        print(f"\n─── Page {page}/{total_pages} ───")
        for row in rows:
            print_contact(row)
        if not rows:
            print("  (no contacts)")
        nav = input("[n]ext [p]rev [q]uit: ").strip().lower()
        if nav == "n": page = min(page + 1, total_pages)
        elif nav == "p": page = max(page - 1, 1)
        else: break
 
 
def menu_search(conn):
    rows = search(conn, input("Search (name/email/phone): ").strip())
    print(f"\n{len(rows)} result(s):\n")
    for row in rows:
        print_contact(row)
 
 
def menu_add(conn):
    name = input("Name: ").strip()
    cid  = add_contact(conn, name,
                       email=input("Email: ").strip() or None,
                       birthday=input("Birthday YYYY-MM-DD: ").strip() or None,
                       group=input("Group: ").strip() or None)
    print(f"Added (id={cid}).")
    while input("Add phone? [y/n]: ").strip().lower() == "y":
        add_phone(conn, name, input("  Phone: ").strip(), input("  Type [home/work/mobile]: ").strip())
        print("  Phone added.")
 
 
def menu_add_phone(conn):
    try:
        add_phone(conn, input("Contact name: ").strip(),
                  input("Phone: ").strip(), input("Type [home/work/mobile]: ").strip())
        print("Phone added.")
    except Exception as e:
        print(f"Error: {e}")
 
 
def menu_move_group(conn):
    try:
        move_to_group(conn, input("Contact name: ").strip(), input("New group: ").strip())
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
 
 
def menu_delete(conn):
    print(f"Deleted: {delete_contact(conn, input('Name: ').strip())} contact(s).")
 
 
MENU = """
1. List / browse   5. Move to group
2. Search          6. Delete
3. Add contact     7. Export JSON
4. Add phone       8. Import JSON
                   9. Import CSV
0. Exit
"""
 
ACTIONS = {
    "1": menu_list, "2": menu_search, "3": menu_add,
    "4": menu_add_phone, "5": menu_move_group, "6": menu_delete,
    "7": lambda c: export_json(c, input("File [contacts.json]: ").strip() or "contacts.json"),
    "8": lambda c: import_json(c, input("File [contacts.json]: ").strip() or "contacts.json"),
    "9": lambda c: import_csv(c,  input("File [contacts.csv]: ").strip()  or "contacts.csv"),
}
 
 
def main():
    conn = get_conn()
    try:
        init_db(conn)
    except Exception as e:
        print(f"Init warning: {e}")
        conn.rollback()
    while True:
        print(MENU)
        choice = input("> ").strip()
        if choice == "0":
            break
        if choice in ACTIONS:
            try:
                ACTIONS[choice](conn)
            except Exception as e:
                conn.rollback()
                print(f"Error: {e}")
    conn.close()
 
 
if __name__ == "__main__":
    main()