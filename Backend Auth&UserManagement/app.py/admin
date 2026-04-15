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
  
      # ================= USERS =================
    cur.execute("SELECT * FROM tester")
    testers = cur.fetchall()

    # ================= HR =================
    cur.execute("SELECT * FROM hr")
    hrs = cur.fetchall()

    # ================= PM =================
    cur.execute("""
        SELECT project_manager.*, hr.name 
        FROM project_manager
        JOIN hr ON hr.id = project_manager.hr_id
    """)
    pms = cur.fetchall()

    # ================= TL =================
    cur.execute("""
        SELECT team_leader.*, project_manager.name
        FROM team_leader
        JOIN project_manager ON project_manager.id = team_leader.pm_id
    """)
    tls = cur.fetchall()

    # ================= LOGS =================
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
