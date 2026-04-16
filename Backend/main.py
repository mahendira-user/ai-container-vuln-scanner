from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
import json
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)
app.secret_key = "secret"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# DB CONNECTION
def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sbom_project",
        charset='utf8'
    )
# LOAD DATASET
with open("packages.json") as f:
    vuln_data = json.load(f)
# HELPER FUNCTIONS
def get_severity(pkg, version):
    # exact match
    for item in vuln_data:
        if item["name"] == pkg and item["version"] == version:
            return item["severity"]
    # fallback (package only)
    for item in vuln_data:
        if item["name"] == pkg:
            return item["severity"]
    return "Low"

def generate_recommendation(pkg, severity):
    if severity == "Low":
        return None

    return f"""Update {pkg} to the latest secure version.
The package "{pkg}" has {severity} severity vulnerabilities which may impact system security. It is recommended to update and monitor this dependency regularly."""

# HOME
@app.route("/")
def index():
    return render_template("index.html")
# ADMIN LOGIN
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u == "admin" and p == "admin":
            session["admin"] = u
            return redirect("/admin_dashboard")

    return render_template("admin_login.html")
# ADMIN DASHBOARD
@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    con = db()
    cur = con.cursor()

    # USERS
    cur.execute("SELECT * FROM tester")
    testers = cur.fetchall()

    #HR
    cur.execute("SELECT * FROM hr")
    hrs = cur.fetchall()

    #PM
    cur.execute("""
        SELECT project_manager.*, hr.name 
        FROM project_manager
        JOIN hr ON hr.id = project_manager.hr_id
    """)
    pms = cur.fetchall()

    #TL 
    cur.execute("""
        SELECT team_leader.*, project_manager.name
        FROM team_leader
        JOIN project_manager ON project_manager.id = team_leader.pm_id
    """)
    tls = cur.fetchall()

    #LOGS
    cur.execute("SELECT * FROM logs")
    logs = cur.fetchall()

    return render_template(
        "admin_dashboard.html",
        testers=testers,
        hrs=hrs,
        pms=pms,
        tls=tls,
        logs=logs
    )

@app.route("/hr_register", methods=["GET","POST"])
def hr_register():
    if request.method == "POST":
        data = (
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["company"],
            request.form["location"],
            request.form["username"],
            request.form["password"]
        )

        con = db()
        cur = con.cursor()
        cur.execute("""INSERT INTO hr 
        (name,email,mobile,company,location,username,password)
        VALUES(%s,%s,%s,%s,%s,%s,%s)""", data)
        con.commit()

        return redirect("/hr_login")

    return render_template("hr_register.html")

@app.route("/hr_login", methods=["GET","POST"])
def hr_login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM hr WHERE username=%s AND password=%s",(u,p))
        user = cur.fetchone()

        if user:
            session["hr"] = user[0]
            return redirect("/hr_dashboard")

    return render_template("hr_login.html")

@app.route("/hr_dashboard")
def hr_dashboard():
    return render_template("hr_dashboard.html")

@app.route("/add_pm", methods=["GET","POST"])
def add_pm():
    if request.method == "POST":
        data = (
            session["hr"],
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["username"],
            request.form["password"]
        )

        con = db()
        cur = con.cursor()
        cur.execute("""INSERT INTO project_manager
        (hr_id,name,email,mobile,username,password)
        VALUES(%s,%s,%s,%s,%s,%s)""", data)
        con.commit()

        return redirect("/hr_dashboard")

    return render_template("add_pm.html")

@app.route("/pm_login", methods=["GET","POST"])
def pm_login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM project_manager WHERE username=%s AND password=%s",(u,p))
        user = cur.fetchone()

        if user:
            session["pm"] = user[0]
            return redirect("/pm_dashboard")

    return render_template("pm_login.html")

@app.route("/pm_dashboard")
def pm_dashboard():
    return render_template("pm_dashboard.html")
@app.route("/add_tl", methods=["GET","POST"])
def add_tl():
    if request.method == "POST":
        data = (
            session["pm"],
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["username"],
            request.form["password"]
        )

        con = db()
        cur = con.cursor()
        cur.execute("""INSERT INTO team_leader
        (pm_id,name,email,mobile,username,password)
        VALUES(%s,%s,%s,%s,%s,%s)""", data)
        con.commit()

        return redirect("/pm_dashboard")

    return render_template("add_tl.html")

@app.route("/assign_project", methods=["GET","POST"])
def assign_project():

    if "pm" not in session:
        return redirect("/pm_login")

    con = db()
    cur = con.cursor()

    pm_id = session["pm"]

    # ✅ Fetch TL
    cur.execute("SELECT id, name FROM team_leader WHERE pm_id=%s", (pm_id,))
    tls = cur.fetchall()

    if request.method == "POST":

        # ✅ USE ID (NOT NAME)
        tl_id = request.form["tl_id"]

        data = (
            pm_id,
            tl_id,
            request.form["title"],
            request.form["module"],
            request.form["workflow"],
            request.form["requirements"],
            "Assigned"
        )

        cur.execute("""
            INSERT INTO projects
            (pm_id, tl_id, title, module, workflow, requirements, status)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, data)

        con.commit()

        return redirect("/pm_dashboard")

    return render_template("assign_project.html", tls=tls)

@app.route("/tl_login", methods=["GET","POST"])
def tl_login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM team_leader WHERE username=%s AND password=%s",(u,p))
        user = cur.fetchone()

        if user:
            session["tl"] = user[0]
            return redirect("/tl_dashboard")

    return render_template("tl_login.html")

@app.route("/tl_dashboard")
def tl_dashboard():
    if "tl" not in session:
        return redirect("/tl_login")

    tl_id = session["tl"]

    con = db()
    cur = con.cursor()

    # Get projects under this TL
    cur.execute("""
        SELECT id, title, module, status
        FROM projects
        WHERE tl_id=%s
    """, (tl_id,))
    projects = cur.fetchall()

    # Get testers under this TL
    cur.execute("""
        SELECT id, name, email, mobile
        FROM tester
        WHERE tl_id=%s
    """, (tl_id,))
    testers = cur.fetchall()

    return render_template("tl_dashboard.html", projects=projects, testers=testers)

@app.route("/add_tester", methods=["GET","POST"])
def add_tester():

    if "tl" not in session:
        return redirect("/tl_login")

    if request.method == "POST":
        data = (
            session["tl"],
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["username"],
            request.form["password"]
        )

        con = db()
        cur = con.cursor()
        cur.execute("""INSERT INTO tester
        (tl_id,name,email,mobile,username,password)
        VALUES(%s,%s,%s,%s,%s,%s)""", data)
        con.commit()

        return redirect("/tl_dashboard")

    return render_template("add_tester.html")

@app.route("/assign_to_tester", methods=["GET","POST"])
def assign_to_tester():

    # ✅ SESSION CHECK
    if "tl" not in session:
        return redirect("/tl_login")

    tl_id = session["tl"]

    con = db()
    cur = con.cursor()

    # ✅ GET TESTERS (ONLY THIS TL)
    cur.execute("SELECT id, name FROM tester WHERE tl_id=%s", (tl_id,))
    testers = cur.fetchall()

    # ✅ GET PROJECTS (ONLY THIS TL)
    cur.execute("SELECT id, title FROM projects WHERE tl_id=%s", (tl_id,))
    projects = cur.fetchall()

    if request.method == "POST":

        tester_name = request.form["tester_name"]
        project_title = request.form["project_title"]

        # 🔥 GET TESTER ID FROM NAME
        cur.execute(
            "SELECT id FROM tester WHERE name=%s AND tl_id=%s",
            (tester_name, tl_id)
        )
        tester_row = cur.fetchone()

        # 🔥 GET PROJECT ID FROM TITLE
        cur.execute(
            "SELECT id FROM projects WHERE title=%s AND tl_id=%s",
            (project_title, tl_id)
        )
        project_row = cur.fetchone()

        # ✅ SAFETY CHECK
        if tester_row and project_row:
            tester_id = tester_row[0]
            project_id = project_row[0]

            # 🔥 UPDATE PROJECT
            cur.execute("""
                UPDATE projects 
                SET tester_id=%s, status='In Progress'
                WHERE id=%s
            """, (tester_id, project_id))

            con.commit()

        return redirect("/tl_dashboard")

    return render_template(
        "assign_tester.html",
        testers=testers,
        projects=projects
    )


# =========================
# TESTER REGISTER
# =========================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = (
            request.form["name"],
            request.form["email"],
            request.form["mobile"],
            request.form["username"],
            request.form["password"]
        )

        con = db()
        cur = con.cursor()
        cur.execute("INSERT INTO testers(name,email,mobile,username,password) VALUES(%s,%s,%s,%s,%s)", data)
        con.commit()

        return redirect("/login")

    return render_template("tester_register.html")

# =========================
# TESTER LOGIN
# =========================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        con = db()
        cur = con.cursor()

        # ✅ CHANGE TABLE HERE
        cur.execute("SELECT * FROM tester WHERE username=%s AND password=%s",(u,p))
        user = cur.fetchone()

        if user:
            session["tester"] = user[0]   # store tester_id
            return redirect("/dashboard")

    return render_template("tester_login.html")

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "tester" not in session:
        return redirect("/login")

    tester_id = session["tester"]

    con = db()
    cur = con.cursor()

    cur.execute("""
        SELECT 
            projects.id,
            projects.title,
            projects.module,
            projects.status,
            results.risk,
            results.recommendation
        FROM projects
        LEFT JOIN results 
            ON results.project_id = projects.id 
            AND results.tester_id = %s
        WHERE projects.tester_id=%s
    """, (tester_id, tester_id))

    projects = cur.fetchall()

    return render_template("tester_dashboard.html", projects=projects)

@app.route("/predict", methods=["POST"])
def predict():
    import networkx as nx
    import matplotlib.pyplot as plt
    import uuid

    # =========================
    # CHECK LOGIN (TESTER)
    # =========================
    if "tester" not in session:
        return redirect("/login")

    tester_id = session.get("tester")
    project_id = request.form.get("project_id")

    file = request.files.get("file")

    if not file or file.filename == "":
        return "No file selected"

    # =========================
    # SETUP
    # =========================
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs("static", exist_ok=True)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    packages = set()

    # =========================
    # READ FILE
    # =========================
    if file.filename.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if "==" in line:
                    try:
                        pkg, ver = line.split("==")
                        packages.add((pkg.lower().strip(), ver.strip()))
                    except:
                        continue

    elif file.filename.endswith(".py"):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()

                if line.startswith("import"):
                    parts = line.replace(",", " ").split()
                    for p in parts[1:]:
                        packages.add((p.lower().strip(), "unknown"))

                elif line.startswith("from"):
                    parts = line.split()
                    if len(parts) > 1:
                        packages.add((parts[1].lower().strip(), "unknown"))

    packages = list(packages)

    # PROCESS PACKAGES
 
    results = []
    recommendations = []

    for pkg, ver in packages:
        severity = get_severity(pkg, ver)

        results.append({
            "name": pkg,
            "version": ver,
            "severity": severity
        })

        rec = generate_recommendation(pkg, severity)
        if rec:
            recommendations.append(rec)

    # RISK CALCULATION

    score_map = {"Low":1, "Medium":2, "High":3, "Critical":4}

    counts = {"Low":0, "Medium":0, "High":0, "Critical":0}
    total_score = 0

    for r in results:
        sev = r["severity"]
        counts[sev] += 1
        total_score += score_map[sev]

    avg_score = total_score / len(results) if results else 1

    if counts["Critical"] >= 1:
        final_risk = "Critical"
    elif avg_score >= 3:
        final_risk = "High"
    elif avg_score >= 2:
        final_risk = "Medium"
    else:
        final_risk = "Low"

    # GRAPH

    G = nx.DiGraph()

    for r in results:
        G.add_node(r["name"], severity=r["severity"])

    for i in range(len(results)-1):
        G.add_edge(results[i]["name"], results[i+1]["name"])

    color_map = []
    for node in G:
        sev = G.nodes[node]["severity"]
        color_map.append(
            "#ff0000" if sev == "Critical" else
            "#ff6600" if sev == "High" else
            "#ffcc00" if sev == "Medium" else
            "#00cc66"
        )

    plt.figure(figsize=(8,6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=2500, font_size=8)

    graph_file = f"graph_{uuid.uuid4().hex}.png"
    plt.savefig(os.path.join("static", graph_file))
    plt.close()

    # =========================
    # CHARTS
    # =========================
    bar_file = f"bar_{uuid.uuid4().hex}.png"
    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title("Risk Distribution")
    plt.xlabel("Severity")
    plt.ylabel("Count")
    plt.savefig(os.path.join("static", bar_file))
    plt.close()

    pie_file = f"pie_{uuid.uuid4().hex}.png"
    plt.figure()
    plt.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%')
    plt.title("Severity Breakdown")
    plt.savefig(os.path.join("static", pie_file))
    plt.close()

    # SAVE RESULT (UPDATED)

    con = db()
    cur = con.cursor()

    # Save in results table
    cur.execute("""
        INSERT INTO results (tester_id, project_id, filename, risk)
        VALUES (%s, %s, %s, %s)
    """, (tester_id, project_id, file.filename, final_risk))

    # Update project status
    if project_id:
        cur.execute("""
            UPDATE projects SET status='Completed'
            WHERE id=%s
        """, (project_id,))

    # Keep your old logs also
    cur.execute(
        "INSERT INTO logs(username, filename, result) VALUES(%s, %s, %s)",
        (session.get("user"), file.filename, final_risk)
    )

    con.commit()
    # RETURN
    return render_template(
        "result.html",
        results=results,
        risk=final_risk,
        recs=recommendations,
        filename=file.filename,
        graph=graph_file,
        bar=bar_file,
        pie=pie_file,
        counts=counts
    )

@app.route("/view_results", methods=["GET", "POST"])
def view_results():

    con = db()
    cur = con.cursor()

    #SAVE RECOMMENDATION
    if request.method == "POST":
        result_id = request.form.get("result_id")
        recommendation = request.form.get("recommendation")

        cur.execute("""
            UPDATE results 
            SET recommendation=%s 
            WHERE id=%s
        """, (recommendation, result_id))
        con.commit()

    # FETCH 
    cur.execute("""
    SELECT 
        results.id,
        tester.name,
        projects.title,
        projects.module,
        projects.workflow,
        projects.status,
        results.filename,
        results.risk,
        results.recommendation,
        results.created_at
    FROM results
    JOIN tester ON tester.id = results.tester_id
    JOIN projects ON projects.id = results.project_id
    ORDER BY results.created_at DESC
    """)

    data = cur.fetchall()

    return render_template("view_results.html", data=data)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
# RUN
if __name__ == "__main__":
    app.run(debug=True)
