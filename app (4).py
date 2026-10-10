import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Smart Digital Evidence Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
    .stApp { background: #061426; color: #e8f1ff; }
    [data-testid="stSidebar"] { background: #07182b; border-right: 1px solid #18324e; }
    [data-testid="stSidebar"] * { color: #dbe9ff; }
    .top-title {font-size: 29px; font-weight: 800; color:#eaf2ff; margin-bottom:0;}
    .sub-title {color:#9fb5d2; font-size:14px; margin-top:0;}
    .panel {background:#081a2d; border:1px solid #183650; border-radius:12px; padding:16px 18px; margin-bottom:12px;}
    .panel-title {font-size:18px; font-weight:750; color:#eaf2ff; margin-bottom:10px;}
    .metric-label {color:#9fb5d2; font-size:13px;}
    .metric-value {font-size:27px; font-weight:800; color:#f0f6ff;}
    .pill {display:inline-block; padding:5px 12px; border-radius:16px; background:#8e2039; color:white; font-weight:800;}
    div[data-testid="stMetric"] {background:#0b2036; border:1px solid #1b3a56; padding:12px; border-radius:10px;}
    div[data-testid="stMetricLabel"] {color:#9fb5d2;}
    div[data-testid="stMetricValue"] {color:#edf5ff;}
    .small-muted {color:#9fb5d2; font-size:12px;}
    h1,h2,h3 {color:#eaf2ff;}
    .stButton>button {border-radius:8px; border:1px solid #285078; background:#102b48; color:#eaf2ff;}
    .stButton>button:hover {border-color:#36a3ff; color:white;}
    [data-testid="stDataFrame"] {border:1px solid #1b3a56; border-radius:8px;}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🛡️ Smart Digital")
    st.markdown("### Evidence Analyzer")
    st.caption("Investigate • Connect • Find the Truth")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Upload Evidence", "Visual Map", "Timeline", "Analysis Report", "Settings"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### 🫆")
    st.caption("Digital Forensics\n\nfor a Safer Tomorrow")

# ---------- Sample evidence data ----------
if "evidence_rows" not in st.session_state:
    st.session_state.evidence_rows = [
        {"Time":"23:45", "Type":"Login", "User":"admin", "Details":"IP: 45.67.89.10 (External)", "Risk":"Medium (20)", "Status":"Suspicious"},
        {"Time":"23:50", "Type":"Web", "User":"admin", "Details":"URL: http://phishing-site.com", "Risk":"High (30)", "Status":"Malicious"},
        {"Time":"23:55", "Type":"File", "User":"admin", "Details":"File: confidential_password.txt", "Risk":"High (30)", "Status":"Sensitive"},
        {"Time":"00:10", "Type":"Device", "User":"admin", "Details":"Android Phone (Unknown Location)", "Risk":"Medium (20)", "Status":"Unusual"},
    ]

st.markdown('<div class="top-title">🛡️ Smart Digital Evidence Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Investigate　 •　 Connect　 •　 Find the Truth</div>', unsafe_allow_html=True)
st.markdown("---")

if page == "Upload Evidence":
    st.markdown("## 📤 Upload Evidence")
    st.write("Upload a sample evidence file (CSV, TXT, JSON, or log file) to add it to this demo dashboard.")
    uploaded = st.file_uploader("Choose an evidence file", type=["csv", "txt", "json", "log"])
    if uploaded:
        st.success(f"Uploaded: {uploaded.name}")
        if uploaded.name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(uploaded)
                st.dataframe(df, use_container_width=True)
                st.info("CSV preview shown. This starter version does not automatically classify every uploaded format.")
            except Exception as e:
                st.error(f"Could not read CSV: {e}")
        else:
            raw = uploaded.getvalue().decode("utf-8", errors="replace")
            st.text_area("File preview", raw[:12000], height=260)
    st.stop()

if page == "Timeline":
    st.markdown("## 🕒 Evidence Timeline")
    for row in st.session_state.evidence_rows:
        st.markdown(f"**🔴 {row['Time']} — {row['Type']}**  \n{row['Details']}")
        st.markdown("---")
    st.stop()

if page == "Analysis Report":
    st.markdown("## 📑 Analysis Report")
    st.write("Demo report generated from the sample events shown on this page.")
    st.metric("Overall risk score", "70 / 100", "HIGH")
    st.write("### Key findings")
    st.write("- Suspicious website detected (possible phishing indicator).")
    st.write("- Sensitive file accessed (password/secret keyword indicator).")
    st.write("- External IP address recorded.")
    st.write("- Login occurred at an unusual time.")
    st.warning("These are illustrative sample findings, not a validated forensic conclusion.")
    st.download_button(
        "Download evidence report (CSV)",
        data=pd.DataFrame(st.session_state.evidence_rows).to_csv(index=False).encode("utf-8"),
        file_name="evidence_report.csv",
        mime="text/csv",
    )
    st.stop()

if page == "Settings":
    st.markdown("## ⚙️ Settings")
    st.info("This starter app uses demonstration data. Replace it with your authorized case evidence before relying on the results.")
    st.checkbox("Show sample evidence", value=True, disabled=True)
    st.stop()

if page == "Visual Map":
    st.markdown("## 🕸️ Investigation Map")
    st.caption("Visual connections between the selected user and evidence categories.")
elif page == "Dashboard":
    st.markdown("## 🕸️ Investigation Map")
    st.caption("Visual connections between events, files, URLs and users.")
else:
    st.markdown("## 🕸️ Investigation Map")
    st.caption("Visual connections between events, files, URLs and users.")

left, right = st.columns([1.85, 1], gap="medium")

# ---------- User-centred investigation graph ----------
with left:
    st.markdown('<div class="panel"><div class="panel-title">🕸️ Investigation Map</div><span class="small-muted">User-centred relationship view</span></div>', unsafe_allow_html=True)
    filter_choice = st.radio(
        "Filter evidence",
        ["All", "Login", "Web", "File", "Device"],
        horizontal=True,
        label_visibility="collapsed",
    )

    # x/y coordinates are fixed so the user stays in the centre.
    nodes = {
        "User: admin": (0.0, 0.0, "#ff4f86", "👤"),
        "Device": (-0.9, 1.15, "#24d6ad", "▣"),
        "Suspicious URL": (1.05, 1.12, "#299cff", "◎"),
        "File Access": (1.35, -0.05, "#a56bff", "▤"),
        "Login Event": (-1.45, 0.0, "#ff5a91", "◷"),
        "IP Address": (-0.85, -1.05, "#16c7ee", "⌖"),
        "Keyword Match": (0.95, -1.05, "#ffbd3f", "⚠"),
    }
    edges = [
        ("Device", "User: admin", "logged in from", "#24d6ad"),
        ("User: admin", "Suspicious URL", "visited", "#299cff"),
        ("User: admin", "File Access", "accessed", "#a56bff"),
        ("User: admin", "Login Event", "login", "#ff5a91"),
        ("User: admin", "IP Address", "from", "#16c7ee"),
        ("File Access", "Keyword Match", "contains", "#ffbd3f"),
    ]
    visible_categories = {
        "All": set(nodes.keys()),
        "Login": {"User: admin", "Login Event", "IP Address"},
        "Web": {"User: admin", "Suspicious URL", "IP Address"},
        "File": {"User: admin", "File Access", "Keyword Match"},
        "Device": {"User: admin", "Device", "IP Address"},
    }[filter_choice]

    fig = go.Figure()
    for a, b, label, color in edges:
        if a not in visible_categories or b not in visible_categories:
            continue
        x1, y1, _, _ = nodes[a]
        x2, y2, _, _ = nodes[b]
        fig.add_trace(go.Scatter(
            x=[x1, x2], y=[y1, y2], mode="lines",
            line=dict(color=color, width=2.4), hoverinfo="skip", showlegend=False
        ))
        # Relationship labels are placed near the middle of each line.
        fig.add_annotation(
            x=(x1+x2)/2, y=(y1+y2)/2, text=label, showarrow=False,
            font=dict(size=10, color=color), bgcolor="rgba(6,20,38,0.96)",
            borderpad=2
        )

    # Draw node circles first, then put labels in dedicated positions outside them.
    # This prevents labels from being hidden underneath the circle markers.
    for name, (x, y, color, icon) in nodes.items():
        if name not in visible_categories:
            continue
        is_user = name == "User: admin"
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers",
            marker=dict(
                size=42 if is_user else 32,
                color="#081a2d",
                line=dict(color=color, width=3),
            ),
            hovertemplate=f"<b>{name}</b><extra></extra>",
            showlegend=False,
        ))
        fig.add_annotation(
            x=x, y=y,
            text=icon,
            showarrow=False,
            font=dict(size=19 if is_user else 16, color=color),
            xanchor="center", yanchor="middle",
        )
        # Put node title above/below the circle, not inside it.
        if name == "User: admin":
            label_y, label_text = y - 0.28, "<b>User: admin</b>"
        elif name in ("Device", "Suspicious URL"):
            label_y, label_text = y + 0.29, f"<b>{name}</b>"
        elif name in ("Login Event", "File Access"):
            label_y, label_text = y + 0.30, f"<b>{name}</b>"
        else:
            label_y, label_text = y - 0.30, f"<b>{name}</b>"
        fig.add_annotation(
            x=x, y=label_y,
            text=label_text,
            showarrow=False,
            font=dict(size=11, color="#edf5ff"),
            xanchor="center", yanchor="middle",
            bgcolor="rgba(6,20,38,0.92)",
            borderpad=3,
        )

    fig.update_layout(
        height=560,
        margin=dict(l=22, r=22, t=28, b=28),
        paper_bgcolor="#081a2d",
        plot_bgcolor="#081a2d",
        xaxis=dict(visible=False, range=[-2.15, 2.15], fixedrange=True),
        yaxis=dict(visible=False, range=[-1.65, 1.75], fixedrange=True, scaleanchor="x", scaleratio=1),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="panel"><div class="panel-title">📄 Evidence Details</div></div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.evidence_rows), use_container_width=True, hide_index=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">🛡️ Risk Overview</div></div>', unsafe_allow_html=True)
    risk_col1, risk_col2 = st.columns(2)
    with risk_col1:
        st.metric("Risk score", "70 / 100")
    with risk_col2:
        st.markdown("### 🔴 HIGH")
        st.caption("Overall risk level")
    st.progress(0.70, text="Overall risk level: HIGH")
    st.markdown("🔴 High-risk events: **2**")
    st.markdown("🟠 Medium-risk events: **2**")
    st.markdown("🟢 Low-risk events: **0**")

    st.markdown('<div class="panel"><div class="panel-title">🕒 Timeline</div></div>', unsafe_allow_html=True)
    timeline_items = [
        ("23:45", "Login Event", "User: admin  |  IP: 45.67.89.10", "#ffbd3f"),
        ("23:50", "Web Activity", "URL: http://phishing-site.com", "#ff4f6d"),
        ("23:55", "File Access", "File: confidential_password.txt", "#ff4f6d"),
        ("00:10", "Unknown Activity", "Device: Android Phone", "#36d28a"),
    ]
    for tm, title, desc, color in timeline_items:
        st.markdown(
            f'<div style="border-left:3px solid {color};padding:2px 0 12px 13px;margin-left:6px;">'
            f'<span style="color:{color};font-weight:800;">● {tm}</span><br>'
            f'<b>{title}</b><br><span style="color:#a9bed8;font-size:12px;">{desc}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="panel"><div class="panel-title">💡 Key Findings</div></div>', unsafe_allow_html=True)
    st.markdown(":material/gpp_bad:<span style='color:red;font-weight:bold;'>Suspicious Website Detected-Phishing Indicator<span>",unsafe_allow_html=True)
    st.markdown(":material/lock_open:<span style='color:#EA580C;font-weight:bold,'>Sensitive File Accessed</span>",unsafe_allow_html=True)
    st.markdown(":material/public:<span style='color:#16A34A;font-weight:bold;'>External IP Address Used</span>",unsafe_allow_html=True)
    st.markdown(":material/schedule:<span style='color:#DB2777;font-weight:bold;'>Unusual Login Time(23:45)</span>",unsafe_allow_html=True)
    st.markdown(":material/account_tree:<span style='color:#DC2626;font-weight:bold;'>Possible Attack Chain Detected</span>",unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#111f57;border:1px solid #293d85;border-radius:12px;padding:15px;margin-top:12px;">
    <b>🛡️ Stay Safe</b><br>
    <span style="color:#c1ccef;font-size:12px;">Verify links, protect sensitive data, and use strong passwords.</span>
    </div>
    """, unsafe_allow_html=True)

st.caption("Demo dashboard • Sample data only • Verify evidence and preserve original files before drawing forensic conclusions.")
