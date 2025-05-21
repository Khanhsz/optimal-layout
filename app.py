import itertools
import numpy as np
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain

# --- Page Config ---
st.set_page_config(page_title="Facility Layout Optimizer", layout="centered")

# --- Header ---
colored_header(
    label="🔧 Facility Layout Optimizer",
    description="Calculate the optimal layout with minimum total cost based on FLOW and DISTANCE matrices.",
    color_name="blue-70",
)

# --- Rain Effect ---
rain(emoji="📦", font_size=30, falling_speed=5, animation_length="infinite")

# --- Sample Input ---
sample_flow = """- 15 20 25
0 - 15 10
0 0 - 10
0 0 0 -"""
sample_dist = """- 4 6 3
4 - 3 5
6 3 - 4
3 5 4 -"""

# --- Input Section ---
st.subheader("📥 Input Matrices")
st.markdown("Please input **FLOW** and **DISTANCE** matrices. Use '-' or '0' to indicate no flow/distance.")

flow_input = st.text_area("FLOW Matrix", sample_flow, height=150, help="Square matrix representing the flow between departments")
dist_input = st.text_area("DISTANCE Matrix", sample_dist, height=150, help="Square matrix representing distances between locations")

# --- Helper Functions ---
def parse_matrix(input_str):
    lines = input_str.strip().split("\n")
    matrix = []
    for line in lines:
        row = [int(x) if x != '-' else 0 for x in line.strip().split()]
        matrix.append(row)
    return np.array(matrix)

def calculate_cost(flow, dist, layout):
    n = len(layout)
    cost = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                cost += flow[i][j] * dist[layout[i]][layout[j]]
    return cost

def find_optimal_layout(flow_matrix, distance_matrix):
    n = len(flow_matrix)
    min_cost = float('inf')
    best_layout = None

    for perm in itertools.permutations(range(n)):
        cost = calculate_cost(flow_matrix, distance_matrix, perm)
        if cost < min_cost:
            min_cost = cost
            best_layout = perm

    return best_layout, min_cost

# --- Run Calculation ---
if st.button("🚀 Calculate Optimal Layout"):
    try:
        flow = parse_matrix(flow_input)
        dist = parse_matrix(dist_input)
        best_layout, min_cost = find_optimal_layout(flow, dist)

        st.success(f"✅ Optimal Layout (Position → Area): {best_layout}")
        st.success(f"💰 Minimum Total Cost: {min_cost}")

        st.markdown("### 🔍 Details")
        st.write("FLOW Matrix:")
        st.dataframe(flow)
        st.write("DISTANCE Matrix:")
        st.dataframe(dist)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# --- Footer ---
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit")
