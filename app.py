
import os
import html
import textwrap

import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RentIQ | Rental Intelligence",
    page_icon="assets/rentiq_logo.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME
# =========================================================

BG = "#F5F0E7"
CARD = "#FFFCF7"
OLIVE = "#68704B"
FOREST = "#193C2D"
RUST = "#98634A"
BURGUNDY = "#653D46"
WALNUT = "#342F29"
MUTED = "#746D62"
BORDER = "#E4DBCE"
GRID = "#E8DFD2"


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --ivory: #F5F0E7;
    --cream: #FFFCF7;
    --olive: #68704B;
    --forest: #193C2D;
    --rust: #98634A;
    --burgundy: #653D46;
    --walnut: #342F29;
    --muted: #746D62;
    --border: #E4DBCE;
}

.stApp {
    background: var(--ivory);
    color: var(--walnut);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: var(--ivory);
}

.block-container {
    max-width: 1550px;
    padding: 1.8rem 2rem 2.5rem;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--walnut) !important;
}

p, label, input, button {
    font-family: 'DM Sans', sans-serif;
}

/* SIDEBAR: keep normal Streamlit layout */
[data-testid="stSidebar"] {
    background: var(--forest);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] > div:first-child {
    background: var(--forest);
    padding: 1.3rem 1rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #E5E9E0;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.16);
    margin: 1.3rem 0;
}

.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 31px;
    font-weight: 700;
    color: #FFFCF7;
    letter-spacing: -0.8px;
}

.brand-mark {
    display: inline-flex;
    width: 49px;
    height: 49px;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: #E8E9DA;
    margin-right: 9px;
    vertical-align: middle;
}

.brand-subtitle {
    color: #C3CDBF;
    font-size: 9px;
    letter-spacing: 1.6px;
    line-height: 1.8;
    font-weight: 700;
    margin-top: 10px;
}

.sidebar-label {
    color: #B8C5B5;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin: 7px 0 12px;
}

.sidebar-footer {
    border-top: 1px solid rgba(255,255,255,0.16);
    margin-top: 95px;
    padding-top: 18px;
    padding-bottom: 12px;
    color: #E5E9E0;
    font-size: 12px;
    line-height: 2;
}

/* Navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none;
}

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
    gap: 5px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    padding: 10px 12px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:hover {
    background: rgba(255,255,255,0.07);
}

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    background: #E8E9DA;
    border-color: #E8E9DA;
}

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) span {
    color: #193C2D !important;
    font-weight: 700;
}

/* Page heading */
.page-top {
    border-bottom: 1px solid var(--border);
    padding-bottom: 22px;
    margin-bottom: 25px;
}

.eyebrow {
    color: var(--olive);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
}

.page-heading {
    color: var(--walnut);
    font-family: 'Playfair Display', serif;
    font-size: 35px;
    font-weight: 600;
    line-height: 1.3;
    letter-spacing: -0.8px;
    margin-top: 7px;
}

.page-description {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.8;
    margin-top: 5px;
}

.section-title {
    color: var(--walnut);
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 4px;
}

.section-description {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.7;
    margin-bottom: 13px;
}

/* Metric cards */
.metric-card {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    min-height: 112px;
    box-shadow: 0 3px 12px rgba(52,47,41,0.025);
}

.metric-label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.8px;
    line-height: 1.6;
}

.metric-value {
    color: var(--walnut);
    font-size: 25px;
    font-weight: 700;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

/* Charts and tables */
div[data-testid="stPlotlyChart"] {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 5px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* Predictor form */
.panel-title {
    color: var(--walnut);
    font-family: 'Playfair Display', serif;
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 5px;
}

.panel-description {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.7;
}

[data-testid="stForm"] {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px;
}

[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stForm"] label {
    color: var(--walnut) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: var(--cream) !important;
    color: var(--walnut) !important;
    border-color: var(--border) !important;
    border-radius: 7px !important;
}

[data-testid="stNumberInput"] button {
    background: #EDE5D9 !important;
    color: var(--walnut) !important;
    border-color: var(--border) !important;
}

.stButton > button,
.stFormSubmitButton > button {
    background: var(--forest);
    color: #FFFCF7;
    border: 1px solid var(--forest);
    border-radius: 8px;
    min-height: 44px;
    font-weight: 600;
    transition: background 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--olive);
    color: white;
    border-color: var(--olive);
}

/* Prediction output */
.result-card {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 25px;
    margin-top: 10px;
}

.result-label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.result-value {
    font-family: 'Playfair Display', serif;
    font-size: 39px;
    font-weight: 700;
    margin: 13px 0;
}

.result-badge {
    display: inline-block;
    border-radius: 30px;
    padding: 7px 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.7px;
}

.result-description {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.8;
    margin-top: 18px;
}

.property-summary {
    background: #F0E9DC;
    border-radius: 10px;
    padding: 16px;
    margin-top: 12px;
    color: var(--walnut);
    font-size: 13px;
    line-height: 2;
}

.empty-card {
    background: var(--cream);
    border: 1px dashed #D4C8B6;
    border-radius: 14px;
    padding: 35px 20px;
    text-align: center;
    margin-top: 10px;
}

.empty-title {
    color: var(--walnut);
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    margin: 12px 0 6px;
}

.empty-description {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.8;
}

.stCaption {
    color: var(--muted);
    font-size: 11px;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: var(--border);
}

footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .page-heading {
        font-size: 28px;
    }

    .metric-value {
        font-size: 21px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def render_html(content):
    """Render HTML without indentation accidentally becoming a code block."""
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )


def metric_card(label, value):
    render_html(f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
    """)


def section_heading(title, description=None):
    render_html(f"""
        <div class="section-title">{html.escape(str(title))}</div>
    """)

    if description:
        render_html(f"""
            <div class="section-description">
                {html.escape(str(description))}
            </div>
        """)


def load_csv(path):
    if not os.path.exists(path):
        return None

    try:
        return pd.read_csv(path)
    except Exception as error:
        st.warning(f"Could not read {path}: {error}")
        return None


def style_chart(fig, height=330):
    fig.update_layout(
        height=height,
        autosize=True,
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(
            family="DM Sans, sans-serif",
            color=WALNUT,
            size=12
        ),
        margin=dict(l=75, r=25, t=30, b=70),
        showlegend=False,
        hoverlabel=dict(
            bgcolor=FOREST,
            bordercolor=FOREST,
            font=dict(
                family="DM Sans, sans-serif",
                color="#FFFCF7",
                size=12
            )
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor=BORDER,
            linewidth=1,
            ticks="outside",
            tickcolor=BORDER,
            tickfont=dict(color=WALNUT, size=11),
            title_font=dict(color=WALNUT, size=12),
            automargin=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID,
            zeroline=False,
            showline=True,
            linecolor=BORDER,
            linewidth=1,
            ticks="outside",
            tickcolor=BORDER,
            tickfont=dict(color=WALNUT, size=11),
            title_font=dict(color=WALNUT, size=12),
            automargin=True
        )
    )
    return fig


def show_image(path, title, caption=None):
    if os.path.exists(path):
        st.markdown(f"**{title}**")
        st.image(path, use_container_width=True)

        if caption:
            st.caption(caption)
    else:
        st.info(f"{title} is unavailable. Run main.py to generate it.")


def format_metrics(df):
    result = df.copy()
    format_dict = {}

    for column in ["Accuracy", "Precision", "Recall", "F1-score"]:
        if column in result.columns:
            result[column] = pd.to_numeric(
                result[column], errors="coerce"
            )
            format_dict[column] = "{:.2%}"

    return result.style.format(format_dict) if format_dict else result


def cluster_summary(clusters):
    required = {"cluster", "price", "square_feet", "bedrooms"}

    if not required.issubset(clusters.columns):
        return None

    return clusters.groupby("cluster").agg(
        Listings=("cluster", "size"),
        Median_Price=("price", "median"),
        Median_Size=("square_feet", "median"),
        Average_Bedrooms=("bedrooms", "mean")
    ).round(2)


def make_histogram(values, bins, x_label, color):
    clipped = values.clip(upper=values.quantile(0.99))

    fig = px.histogram(
        x=clipped,
        nbins=bins,
        labels={
            "x": x_label,
            "count": "Number of listings"
        },
        color_discrete_sequence=[color]
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate=(
            f"{html.escape(x_label)}: %{{x:,.0f}}"
            "<br>Listings: %{y:,}<extra></extra>"
        )
    )

    return style_chart(fig)


def house_logo(size=48):
    return f"""
    <div style="display:flex;justify-content:center;align-items:center">
        <svg viewBox="0 0 40 40" width="{size}" height="{size}"
             fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 19 L20 8 L33 19"
                  stroke="#193C2D" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M11 17 V32 H29 V17"
                  stroke="#193C2D" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M17 32 V23 H23 V32"
                  stroke="#68704B" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    """


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    render_html("""
        <div>
            <span class="brand-mark">
                <svg viewBox="0 0 40 40" width="29" height="29"
                     fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 19 L20 8 L33 19"
                          stroke="#193C2D" stroke-width="2.5"
                          stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M11 17 V32 H29 V17"
                          stroke="#193C2D" stroke-width="2.5"
                          stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M17 32 V23 H23 V32"
                          stroke="#68704B" stroke-width="2.5"
                          stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </span>
            <span class="brand-name">RentIQ</span>
        </div>

        <div class="brand-subtitle">
            APARTMENT RENTAL<br>INTELLIGENCE
        </div>

        <hr>

        <div class="sidebar-label">YOUR WORKSPACE</div>
    """)

    page = st.radio(
        "Navigation",
        ["Overview", "Rental Insights", "Price Predictor"],
        label_visibility="collapsed",
        key="rentiq_page"
    )

    # Normal document flow; no fixed positioning or forced heights.
    # The extra margin moves the footer lower while preserving the sidebar.
    render_html("""
        <div class="sidebar-footer">
            <div class="sidebar-label">POWERED BY DATA</div>
            Machine learning<br>
            Rental analytics<br><br>
            <span style="color:#B8C5B5;font-size:10px;letter-spacing:1px">
                RENTIQ · PROJECT WORKSPACE
            </span>
        </div>
    """)


# =========================================================
# PAGE HEADER
# =========================================================

page_info = {
    "Overview": (
        "MARKET OVERVIEW",
        "Understand the rental market",
        "A clear snapshot of listings, pricing patterns and model performance."
    ),
    "Rental Insights": (
        "EXPLORE THE DATA",
        "Discover rental patterns",
        "Explore apartment sizes, bedroom distributions and rental clusters."
    ),
    "Price Predictor": (
        "PREDICTION STUDIO",
        "Explore a property's price segment",
        "Enter apartment details to classify its relative price category."
    )
}

eyebrow, heading, description = page_info[page]

render_html(f"""
    <div class="page-top">
        <div class="eyebrow">{html.escape(eyebrow)}</div>
        <div class="page-heading">{html.escape(heading)}</div>
        <div class="page-description">{html.escape(description)}</div>
    </div>
""")


# =========================================================
# OVERVIEW PAGE
# =========================================================

if page == "Overview":
    df = load_csv("data/cleaned_apartments.csv")
    metrics = load_csv("outputs/classification/classification_metrics.csv")
    clusters = load_csv("outputs/clustering/clustering_results.csv")

    if df is None:
        st.error("Cleaned dataset not found. Run main.py first.")
        st.stop()

    for column in ["price", "square_feet", "bedrooms", "bathrooms"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    prices = (
        df.loc[df["price"] > 0, "price"].dropna()
        if "price" in df.columns
        else pd.Series(dtype=float)
    )

    sizes = (
        df.loc[df["square_feet"] > 0, "square_feet"].dropna()
        if "square_feet" in df.columns
        else pd.Series(dtype=float)
    )

    best_accuracy = None

    if metrics is not None and {"Model", "Accuracy"}.issubset(metrics.columns):
        metrics["Accuracy"] = pd.to_numeric(
            metrics["Accuracy"], errors="coerce"
        )
        available = metrics.dropna(subset=["Accuracy"])

        if not available.empty:
            best_accuracy = available.loc[
                available["Accuracy"].idxmax(), "Accuracy"
            ]

    section_heading(
        "Market at a glance",
        "Key indicators calculated from your cleaned rental dataset."
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        metric_card("CLEANED LISTINGS", f"{len(df):,}")

    with c2:
        metric_card(
            "MEDIAN LISTING PRICE",
            f"{prices.median():,.0f}" if not prices.empty else "N/A"
        )

    with c3:
        metric_card(
            "MEDIAN APARTMENT SIZE",
            f"{sizes.median():,.0f} sq. ft." if not sizes.empty else "N/A"
        )

    with c4:
        metric_card(
            "BEST MODEL ACCURACY",
            f"{best_accuracy:.2%}" if best_accuracy is not None else "N/A"
        )

    st.caption(
        "Price values use the dataset's original units. Confirm currency "
        "and rental period before interpreting them as monthly rent."
    )

    st.write("")
    left, right = st.columns(2, gap="large")

    with left:
        section_heading(
            "Rental price distribution",
            "The top 1% of values is clipped for chart readability."
        )

        if not prices.empty:
            st.plotly_chart(
                make_histogram(prices, 30, "Listing price", OLIVE),
                use_container_width=True,
                key="overview_price_hist"
            )
        else:
            st.info("No valid price data is available.")

    with right:
        section_heading(
            "Apartment size distribution",
            "Distribution of apartment sizes in square feet."
        )

        if not sizes.empty:
            st.plotly_chart(
                make_histogram(
                    sizes, 25, "Apartment size (sq. ft.)", RUST
                ),
                use_container_width=True,
                key="overview_size_hist"
            )
        else:
            st.info("No valid size data is available.")

    st.write("")
    section_heading(
        "Price versus apartment size",
        "Hover over points to inspect individual listings."
    )

    if {"price", "square_feet"}.issubset(df.columns):
        relationship = df[["square_feet", "price"]].dropna()
        relationship = relationship[
            (relationship["square_feet"] > 0)
            & (relationship["price"] > 0)
        ]

        if not relationship.empty:
            relationship = relationship.sample(
                n=min(3000, len(relationship)),
                random_state=42
            )

            fig = px.scatter(
                relationship,
                x="square_feet",
                y="price",
                labels={
                    "square_feet": "Apartment size (sq. ft.)",
                    "price": "Listing price"
                },
                color_discrete_sequence=[OLIVE],
                opacity=0.55
            )

            fig.update_traces(
                marker=dict(size=6),
                hovertemplate=(
                    "Apartment size: %{x:,.0f} sq. ft."
                    "<br>Listing price: %{y:,.0f}<extra></extra>"
                )
            )

            style_chart(fig, 390)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="overview_price_size"
            )

    st.write("")
    section_heading(
        "Model performance",
        "Compare classification models using their saved evaluation metrics."
    )

    if metrics is not None and not metrics.empty:
        display_metrics = metrics.copy()

        if {"Model", "Accuracy"}.issubset(display_metrics.columns):
            display_metrics["Accuracy"] = pd.to_numeric(
                display_metrics["Accuracy"], errors="coerce"
            )
            chart_data = display_metrics.dropna(subset=["Accuracy"])

            if not chart_data.empty:
                fig = px.bar(
                    chart_data,
                    x="Model",
                    y="Accuracy",
                    text=chart_data["Accuracy"].map(
                        lambda value: f"{value:.1%}"
                    ),
                    labels={
                        "Model": "Classification model",
                        "Accuracy": "Test accuracy"
                    },
                    color_discrete_sequence=[OLIVE]
                )

                fig.update_traces(
                    textposition="outside",
                    cliponaxis=False,
                    hovertemplate=(
                        "%{x}<br>Accuracy: %{y:.2%}<extra></extra>"
                    )
                )

                style_chart(fig, 290)
                fig.update_yaxes(tickformat=".0%", range=[0, 1])

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key="overview_model_comparison"
                )

        st.dataframe(
            format_metrics(display_metrics),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Model metrics are unavailable. Run main.py first.")

    st.write("")
    section_heading(
        "Rental clusters",
        "Summary of groups discovered by K-Means clustering."
    )

    if clusters is not None:
        summary = cluster_summary(clusters)

        if summary is not None:
            st.dataframe(summary, use_container_width=True)
        else:
            st.info("The clustering CSV is missing expected columns.")

        show_image(
            "outputs/clustering/rental_clusters.png",
            "Cluster visualization",
            "Groups formed using apartment price, size, bedrooms and bathrooms."
        )
    else:
        st.info("Clustering results are unavailable. Run main.py first.")


# =========================================================
# RENTAL INSIGHTS PAGE
# =========================================================

elif page == "Rental Insights":
    df = load_csv("data/cleaned_apartments.csv")

    if df is None:
        st.error("Cleaned dataset not found. Run main.py first.")
        st.stop()

    section_heading(
        "Explore the listings",
        "Explore the distributions and relationships in your dataset."
    )

    left, right = st.columns(2, gap="large")

    with left:
        show_image(
            "outputs/eda/price_distribution.png",
            "Rental price distribution",
            "The spread of listing prices in the dataset."
        )

    with right:
        show_image(
            "outputs/eda/size_distribution.png",
            "Apartment size distribution",
            "The spread of apartment sizes."
        )

    left, right = st.columns(2, gap="large")

    with left:
        show_image(
            "outputs/eda/bedroom_distribution.png",
            "Bedroom distribution",
            "Listings grouped by the number of bedrooms."
        )

    with right:
        show_image(
            "outputs/eda/price_vs_size.png",
            "Price versus apartment size",
            "Relationship between apartment size and listing price."
        )

    st.write("")
    section_heading(
        "Apartment clusters",
        "Groups identified from the numerical characteristics of listings."
    )

    clusters = load_csv("outputs/clustering/clustering_results.csv")

    if clusters is not None:
        summary = cluster_summary(clusters)

        if summary is not None:
            st.dataframe(summary, use_container_width=True)
        else:
            st.info("Clustering results are missing expected columns.")

        show_image(
            "outputs/clustering/rental_clusters.png",
            "K-Means visualization",
            "The saved visualization of the discovered apartment groups."
        )
    else:
        st.info("Clustering output unavailable. Run main.py first.")

    st.write("")
    section_heading(
        "Classification performance",
        "Evaluation metrics and confusion matrices from the trained models."
    )

    metrics = load_csv("outputs/classification/classification_metrics.csv")

    if metrics is not None:
        st.dataframe(
            format_metrics(metrics),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Classification metrics unavailable. Run main.py first.")

    left, right = st.columns(2, gap="large")

    with left:
        show_image(
            "outputs/classification/decision_tree_confusion_matrix.png",
            "Decision Tree confusion matrix",
            "Actual categories compared with predicted categories."
        )

    with right:
        show_image(
            "outputs/classification/random_forest_confusion_matrix.png",
            "Random Forest confusion matrix",
            "Actual categories compared with predicted categories."
        )


# --------------------------------------------------
# PRICE PREDICTOR
# --------------------------------------------------

elif page == "Price Predictor":
    model_path = "outputs/rent_iq_model.pkl"

    section_heading(
        "Property details",
        "Enter the property characteristics to estimate its relative price category."
    )

    if not os.path.exists(model_path):
        st.error(
            "The trained model was not found at "
            "`outputs/rent_iq_model.pkl`. Run main.py first."
        )
        st.stop()

    try:
        model = joblib.load(model_path)
    except Exception as error:
        st.error(f"The saved model could not be loaded: {error}")
        st.stop()

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown(
            '<div class="panel-title">Property information</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="panel-description">Provide the apartment size, '
            'room count and geographic coordinates.</div>',
            unsafe_allow_html=True
        )

        with st.form("rentiq_prediction_form"):
            square_feet = st.number_input(
                "Apartment size (sq. ft.)",
                min_value=1,
                max_value=100000,
                value=900,
                step=50
            )

            col1, col2 = st.columns(2)

            with col1:
                bedrooms = st.number_input(
                    "Bedrooms",
                    min_value=0,
                    max_value=20,
                    value=2,
                    step=1
                )

            with col2:
                bathrooms = st.number_input(
                    "Bathrooms",
                    min_value=0.5,
                    max_value=20.0,
                    value=1.0,
                    step=0.5
                )

            st.markdown("**Location coordinates**")

            col3, col4 = st.columns(2)

            with col3:
                latitude = st.number_input(
                    "Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    value=40.75,
                    format="%.4f"
                )

            with col4:
                longitude = st.number_input(
                    "Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    value=-73.98,
                    format="%.4f"
                )

            submitted = st.form_submit_button(
                "Predict price category",
                use_container_width=True
            )

    with right:
        st.markdown(
            '<div class="panel-title">Prediction result</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="panel-description">Your model result will appear here.</div>',
            unsafe_allow_html=True
        )

        if submitted:
            apartment = pd.DataFrame([{
                "square_feet": square_feet,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "latitude": latitude,
                "longitude": longitude
            }])

            try:
                # Use the feature order saved by the fitted pipeline,
                # when available. This helps avoid column-order mismatches.
                expected_features = getattr(
                    model, "feature_names_in_", None
                )

                if expected_features is not None:
                    missing = [
                        name for name in expected_features
                        if name not in apartment.columns
                    ]

                    if missing:
                        st.error(
                            "The saved model expects additional features: "
                            + ", ".join(missing)
                        )
                        st.stop()

                    apartment = apartment[list(expected_features)]

                prediction = model.predict(apartment)[0]
                prediction = str(prediction)

                categories = {
                    "Low": (
                        OLIVE,
                        "#EDF0E5",
                        "This property falls in the lower-price segment "
                        "defined by the model's training data."
                    ),
                    "Medium": (
                        RUST,
                        "#F5E8DC",
                        "This property falls in the middle-price segment "
                        "defined by the model's training data."
                    ),
                    "High": (
                        BURGUNDY,
                        "#F2E4E7",
                        "This property falls in the higher-price segment "
                        "defined by the model's training data."
                    )
                }

                # Also handle classifiers that store longer category labels.
                normalized = prediction.strip().lower()

                if normalized.startswith("low"):
                    key = "Low"
                elif normalized.startswith("high"):
                    key = "High"
                elif normalized.startswith("medium"):
                    key = "Medium"
                else:
                    key = prediction

                if key in categories:
                    color, badge_bg, explanation = categories[key]
                else:
                    color, badge_bg, explanation = (
                        FOREST,
                        "#E8E9DA",
                        "The model returned a category from its training labels."
                    )

                safe_prediction = html.escape(prediction)
                safe_key = html.escape(key.upper())

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">
                            PREDICTED PRICE CATEGORY
                        </div>
                        <div class="result-value" style="color:{color}">
                            {safe_prediction}
                        </div>
                        <span class="result-badge"
                              style="background:{badge_bg};color:{color}">
                            {safe_key} PRICE SEGMENT
                        </span>
                        <div class="result-description">
                            {html.escape(explanation)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="section-title" style="font-size:19px;'
                    'margin-top:20px">Property summary</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="property-summary">
                        <b>Apartment size</b>: {square_feet:,} sq. ft.<br>
                        <b>Bedrooms</b>: {bedrooms}<br>
                        <b>Bathrooms</b>: {bathrooms:g}<br>
                        <b>Latitude</b>: {latitude:.4f}<br>
                        <b>Longitude</b>: {longitude:.4f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as error:
                st.error(
                    "The model could not complete this prediction. "
                    "Check the error details below."
                )
                st.code(str(error))

                st.info(
                    "If the error mentions missing or unexpected features, "
                    "the saved model may have been trained with a different "
                    "feature set. We can correct the model pipeline without "
                    "redesigning the dashboard."
                )

        
        else:
            st.markdown(
                """
                <div style="background:#F1F6FC;
                            border:1px dashed #B8CBE0;
                            border-radius:16px;
                            padding:35px 20px;
                            text-align:center;
                            margin-top:14px;">
                    <div style="margin-bottom:12px;">
                        <svg viewBox="0 0 40 40" width="48" height="48"
                             fill="none"
                             xmlns="http://www.w3.org/2000/svg">
                            <path d="M7 19 L20 8 L33 19"
                                  stroke="#193C2D" stroke-width="2.5"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"/>
                            <path d="M11 17 V32 H29 V17"
                                  stroke="#193C2D" stroke-width="2.5"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"/>
                            <path d="M17 32 V23 H23 V32"
                                  stroke="#68704B" stroke-width="2.5"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <h3 style="color:#153E75; font-size:21px;
                               margin:12px 0 8px;">
                        Your result will appear here
                    </h3>
                    <p style="color:#64748B; font-size:13px;
                              line-height:1.7; margin:0;">
                        Enter the property details and click
                        <b>Predict price category</b> to see your result.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

footer_left, footer_right = st.columns(2)

with footer_left:
    st.caption("RentIQ  |  Apartment Rental Intelligence")

with footer_right:
    st.markdown(
        '<div style="text-align:right;color:#746D62;font-size:11px">'
        'Python · Streamlit · Machine Learning</div>',
        unsafe_allow_html=True
    )
