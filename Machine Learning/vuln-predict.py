@app.route("/predict", methods=["POST"])
def predict():
    import networkx as nx
    import matplotlib.pyplot as plt
    import uuid

    # CHECK LOGIN (TESTER)

    if "tester" not in session:
        return redirect("/login")

    tester_id = session.get("tester")
    project_id = request.form.get("project_id")

    file = request.files.get("file")

    if not file or file.filename == "":
        return "No file selected"

    # SETUP

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs("static", exist_ok=True)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    packages = set()

    # READ FILE

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

    # CHARTS

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
