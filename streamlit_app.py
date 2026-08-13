import streamlit as st

from app.scanner import WebsiteScanner


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Website Health Agent",
    page_icon="🔍",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "scan_url" not in st.session_state:
    st.session_state.scan_url = ""


# ============================================================
# HEADER
# ============================================================

st.title("🔍 AI Website Health Agent")

st.markdown(
    """
    ### Intelligent Website Health Monitoring

    Enter a website URL and the system will scan its webpages,
    detect broken resources, calculate a health score, and use
    **Ollama** to generate an AI-powered health report.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Scan Configuration")

    max_pages = st.number_input(
        "Maximum Pages",
        min_value=1,
        max_value=500,
        value=5,
        step=1
    )

    timeout = st.number_input(
        "Request Timeout (seconds)",
        min_value=1,
        max_value=60,
        value=10,
        step=1
    )

    st.info(
        "AI Model: Ollama\n\n"
        "Model: llama3.2:latest"
    )


# ============================================================
# WEBSITE URL
# ============================================================

url = st.text_input(
    "🌐 Website URL",
    value=st.session_state.scan_url,
    placeholder="https://example.com"
)


# ============================================================
# START SCAN
# ============================================================

scan_button = st.button(
    "🚀 START WEBSITE SCAN",
    type="primary",
    use_container_width=True
)


# ============================================================
# RUN SCAN ONLY WHEN BUTTON IS CLICKED
# ============================================================

if scan_button:

    if not url.strip():

        st.error(
            "❌ Please enter a website URL."
        )

        st.stop()

    # --------------------------------------------------------
    # NORMALIZE URL
    # --------------------------------------------------------

    if not url.startswith(
        ("http://", "https://")
    ):

        url = "https://" + url

    # --------------------------------------------------------
    # SAVE URL
    # --------------------------------------------------------

    st.session_state.scan_url = url

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    progress = st.progress(0)

    status = st.empty()

    try:

        # ----------------------------------------------------
        # CRAWLING
        # ----------------------------------------------------

        status.info(
            "🔎 Crawling website..."
        )

        progress.progress(10)

        scanner = WebsiteScanner(
            max_pages=max_pages,
            timeout=timeout,
            ollama_model="llama3.2:latest"
        )

        # ----------------------------------------------------
        # SCAN
        # ----------------------------------------------------

        result = scanner.scan(url)

        progress.progress(100)

        status.success(
            "✅ Website scan completed!"
        )

        # ----------------------------------------------------
        # IMPORTANT
        # SAVE RESULT IN SESSION STATE
        # ----------------------------------------------------

        st.session_state.scan_result = result

    except Exception as e:

        progress.empty()

        status.error(
            "❌ Scan failed"
        )

        st.exception(e)

        st.stop()


# ============================================================
# GET SAVED RESULT
# ============================================================

result = st.session_state.scan_result


# ============================================================
# DISPLAY RESULTS
# ============================================================

if result is not None:

    health = result["health_result"]

    summary = result["summary"]

    # ========================================================
    # WEBSITE HEALTH
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Website Health"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Health Score",
            f'{health["health_score"]}/100'
        )

    with col2:

        st.metric(
            "Health Status",
            health["health_status"]
        )

    # ========================================================
    # SCAN RESULTS
    # ========================================================

    st.subheader(
        "🔎 Scan Results"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    # --------------------------------------------------------
    # PAGES
    # --------------------------------------------------------

    with col1:

        st.metric(
            "Pages",
            result[
                "website_results"
            ]["pages_checked"]
        )

    # --------------------------------------------------------
    # BROKEN LINKS
    # --------------------------------------------------------

    with col2:

        st.metric(
            "Broken Links",
            len(
                summary.get(
                    "broken_links",
                    []
                )
            )
        )

    # --------------------------------------------------------
    # BROKEN IMAGES
    # --------------------------------------------------------

    with col3:

        st.metric(
            "Broken Images",
            len(
                summary.get(
                    "broken_images",
                    []
                )
            )
        )

    # --------------------------------------------------------
    # BROKEN CSS
    # --------------------------------------------------------

    with col4:

        st.metric(
            "Broken CSS",
            len(
                summary.get(
                    "broken_css",
                    []
                )
            )
        )

    # --------------------------------------------------------
    # BROKEN JAVASCRIPT
    # --------------------------------------------------------

    with col5:

        st.metric(
            "Broken JS",
            len(
                summary.get(
                    "broken_scripts",
                    []
                )
            )
        )

    # ========================================================
    # SEVERITY
    # ========================================================

    st.subheader(
        "🚨 Severity"
    )

    severity = health[
        "severity_counts"
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Critical",
            severity.get(
                "critical",
                0
            )
        )

    with col2:

        st.metric(
            "High",
            severity.get(
                "high",
                0
            )
        )

    with col3:

        st.metric(
            "Medium",
            severity.get(
                "medium",
                0
            )
        )

    with col4:

        st.metric(
            "Low",
            severity.get(
                "low",
                0
            )
        )

    # ========================================================
    # AI REPORT
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 AI Website Health Report"
    )

    st.markdown(
        result["ai_report"]
    )

    # ========================================================
    # DOWNLOAD REPORTS
    # ========================================================

    st.divider()

    st.subheader(
        "📁 Download Reports"
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # RAW JSON
    # --------------------------------------------------------

    with col1:

        with open(
            result["raw_report_file"],
            "r",
            encoding="utf-8"
        ) as file:

            raw_json = file.read()

        st.download_button(
            label="⬇️ Download Raw Scan JSON",
            data=raw_json,
            file_name="raw_scan.json",
            mime="application/json",
            key="download_raw_json"
        )

    # --------------------------------------------------------
    # AI REPORT
    # --------------------------------------------------------

    with col2:

        st.download_button(
            label="⬇️ Download AI Health Report",
            data=result["ai_report"],
            file_name="ai_health_report.txt",
            mime="text/plain",
            key="download_ai_report"
        )

    # ========================================================
    # REPORT LOCATIONS
    # ========================================================

    st.caption(
        f"Raw scan: {result['raw_report_file']}"
    )

    st.caption(
        f"AI report: {result['ai_report_file']}"
    )

else:

    # ========================================================
    # INITIAL SCREEN
    # ========================================================

    st.info(
        "👆 Enter a website URL and click "
        "**START WEBSITE SCAN** to begin."
    )