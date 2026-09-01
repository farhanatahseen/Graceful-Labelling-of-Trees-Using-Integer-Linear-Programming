import pulp

# --- Define the problem and the tree ---
n = 6
edges = [(0,1),(1,2),(2,3),(3,4),(4,5)]  # example: path P6 — replace with your own tree
m = len(edges)

prob = pulp.LpProblem("GracefulLabelling", pulp.LpMinimize)

# --- Decision variables ---
x = {v: pulp.LpVariable(f"x_{v}", lowBound=0, upBound=n-1, cat="Integer") for v in range(n)}
d = {e: pulp.LpVariable(f"d_{u}_{v}", lowBound=1, upBound=n-1, cat="Integer") for e, (u, v) in enumerate(edges)}
y = {(u, v): pulp.LpVariable(f"y_{u}_{v}", cat="Binary") for u in range(n) for v in range(u+1, n)}
z = {(e1, e2): pulp.LpVariable(f"z_{e1}_{e2}", cat="Binary") for e1 in range(m) for e2 in range(e1+1, m)}
s = {e: pulp.LpVariable(f"s_{e}", cat="Binary") for e in range(m)}

print(f"Created {len(x)} x-vars, {len(d)} d-vars, {len(y)} y-vars, {len(z)} z-vars, {len(s)} s-vars")

# --- Constraints ---
M = n
M_abs = 2*(n-1)

# 1) Vertex-label distinctness
for u in range(n):
    for v in range(u+1, n):
        prob += x[u] - x[v] >= 1 - M*(1 - y[(u, v)])
        prob += x[v] - x[u] >= 1 - M*y[(u, v)]

# 2) Edge-label distinctness
for e1 in range(m):
    for e2 in range(e1+1, m):
        prob += d[e1] - d[e2] >= 1 - M*(1 - z[(e1, e2)])
        prob += d[e2] - d[e1] >= 1 - M*z[(e1, e2)]

# 3) Absolute-difference linearisation
for e, (u, v) in enumerate(edges):
    prob += d[e] >= x[u] - x[v]
    prob += d[e] >= x[v] - x[u]
    prob += d[e] <= x[u] - x[v] + M_abs*(1 - s[e])
    prob += d[e] <= x[v] - x[u] + M_abs*s[e]

print("Constraints added:", len(prob.constraints))

# --- Solve and extract results ---
prob.solve()

print("Status:", pulp.LpStatus[prob.status])

if pulp.LpStatus[prob.status] == "Optimal":
    print("\nVertex labels:")
    for v in range(n):
        print(f"  x_{v} = {int(x[v].varValue)}")

    print("\nEdge labels:")
    edge_labels = []
    for e, (u, v) in enumerate(edges):
        val = int(d[e].varValue)
        edge_labels.append(val)
        print(f"  edge ({u},{v}) -> d = {val}")

    print("\nEdge label set:", sorted(edge_labels))
    print("Expected set {1,...,n-1}:", list(range(1, n)))
    print("Valid graceful labelling:", sorted(edge_labels) == list(range(1, n)))

