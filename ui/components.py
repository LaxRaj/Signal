import streamlit as st

def render_header():
    """Renders the main header of the application."""
    st.title("📡 Project Signal: VC Tech & Startup Tracker")
    st.markdown("An automated deal sourcing and trend analysis tool for venture capitalists.")

def render_footer():
    """Renders the footer."""
    st.markdown("---")
    st.markdown("Built by Lakshyaraj Bhati as a case study in automated VC tooling.")

def render_analysis_section(trends_df):
    """Renders the trend analysis chart and interpretation."""
    st.header("Automated Market Trend Analysis")
    st.subheader("Keyword Frequency in Recent News & Launches")
    st.bar_chart(trends_df.set_index('Keyword'))
    st.markdown("""
    **How to interpret this:** This chart provides a quick snapshot of which technology sectors 
    are currently generating the most buzz. A VC analyst can use this to quickly identify hot 
    sectors and dig deeper into the corresponding articles and products.
    """)
