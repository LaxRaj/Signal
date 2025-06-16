import streamlit as st
import pandas as pd
import asyncio

# Import your modules
from scrapers import techcrunch, producthunt
from core import analysis, scoring, ner
from ui import components
from core import ai_analyst

# --- Helper function to load data ---
@st.cache_data
def load_historical_data():
    try:
        return pd.read_csv('historical_data.csv', parse_dates=['date'])
    except FileNotFoundError:
        return None

# --- Main App Logic ---
def main():
    st.set_page_config(page_title="Project Signal", page_icon="📡", layout="wide")
    components.render_header()
    
    historical_df = load_historical_data()
    if historical_df is None:
        st.error("Historical data not found. Please run generate_historical_data.py first.")
        return

    # --- Sidebar ---
    st.sidebar.title("App Mode")
    app_mode = st.sidebar.radio("Choose your mode:", ('Live Tracker', 'Historical Analysis'))
    
    # --- Secrets Status Indicator ---
    st.sidebar.title("API Configuration")
    try:
        if st.secrets["GEMINI_API_KEY"]:
            st.sidebar.success("✅ Gemini API Key found.")
    except (KeyError, FileNotFoundError):
        st.sidebar.error("❌ Gemini API Key not found.")
        st.sidebar.info("Please add your key to the `.streamlit/secrets.toml` file and restart the app.")
    
    st.sidebar.title("About the Signal Score")
    with st.sidebar.expander("How is the score calculated?"):
        st.markdown("""
        The **Signal Score** is a weighted average designed to mimic how a VC analyst evaluates a news item.
        - **Content (40%):** A funding announcement is the strongest signal.
        - **Source (30%):** A report in a top-tier publication like TechCrunch is more significant than a community post.
        - **AI Confidence (30%):** News about core AI technology (e.g., "foundational models") scores higher than general "AI" mentions.
        """)
        st.markdown("""
        **Signal Tiers:**
        - 🔴 **Priority Review (> 85):** Drop everything.
        - 🟠 **Emerging Trend (70-84):** Research this week.
        - 🔵 **Monitor (50-69):** Keep an eye on this.
        """)

    if app_mode == 'Live Tracker':
        st.header("Live Company Signal Tracker")
        if 'data' not in st.session_state:
            st.session_state.data = pd.DataFrame()

        if st.button("Fetch Latest News & Products", type="primary"):
            with st.spinner('Scanning the web for emerging tech...'):
                tc_df = techcrunch.scrape()
                ph_df = producthunt.scrape()
                combined_df = pd.concat([tc_df, ph_df], ignore_index=True)
                st.session_state.data = combined_df
            st.success("Successfully fetched the latest data!")

        if not st.session_state.data.empty:
            df = st.session_state.data.copy()
            df['Companies'] = (df['title'] + ' ' + df['description']).apply(ner.extract_company_names)
            
            company_df = df.explode('Companies').rename(columns={'Companies': 'company_name'})
            if not company_df.empty:
                company_df['Signal Score'] = company_df.apply(scoring.calculate_signal_score, axis=1)
                company_df['Tier'] = company_df['Signal Score'].apply(scoring.get_signal_tier)

                agg_df = company_df.groupby('company_name').agg(
                    Signal_Score=('Signal Score', 'max'),
                    Tier=('Tier', 'first'),
                    Mentions=('company_name', 'size'),
                    Sources=('source', lambda x: list(x.unique()))
                ).sort_values(by='Signal_Score', ascending=False)
                
                st.dataframe(agg_df, use_container_width=True)
        else:
            st.info("Click the button to fetch live data.")

    elif app_mode == 'Historical Analysis':
        st.header("Time Machine & ROI Simulator")

        # --- The Time Machine Slider ---
        selected_date = st.slider(
            "Select a date to analyze:",
            min_value=historical_df['date'].min().to_pydatetime(),
            max_value=historical_df['date'].max().to_pydatetime(),
            value=historical_df['date'].min().to_pydatetime(),
            format="YYYY-MM-DD"
        )

        # Filter data up to the selected date
        past_df = historical_df[historical_df['date'] <= pd.to_datetime(selected_date)].copy()
        past_df['Signal Score'] = past_df.apply(scoring.calculate_signal_score, axis=1)
        past_df['Tier'] = past_df['Signal Score'].apply(scoring.get_signal_tier)
        
        st.subheader(f"Top Signals as of {selected_date.strftime('%Y-%m-%d')}")
        top_signals_df = past_df.sort_values(by='Signal Score', ascending=False).head(10)

        st.dataframe(
            top_signals_df[['Tier', 'Signal Score', 'company_name', 'title']],
            use_container_width=True,
            hide_index=True
        )
        
        selected_company = st.selectbox("Select a company to deep dive:", top_signals_df['company_name'].unique())

        if selected_company:
            # --- Use a container for the deep dive section for better layout ---
            with st.container(border=True):
                company_data = top_signals_df[top_signals_df['company_name'] == selected_company].iloc[0]
                
                # --- Display AI Analyst Take ---
                st.subheader(f"🤖 AI Analyst Take for {selected_company}", divider='rainbow')
                st.markdown(f"**News Item:** *{company_data['title']}*")

                with st.spinner("Generating AI analysis..."):
                    analyst_take = asyncio.run(ai_analyst.get_analyst_take(
                        company_data['title'], 
                        company_data['description']
                    ))
                    st.markdown(analyst_take)

                # --- The ROI Simulator ---
                st.subheader("📈 Simulate Investment & Reveal Outcome", divider='rainbow')
                if st.button(f"Simulate a $1M Investment in {selected_company}"):
                    true_outcome_row = historical_df[historical_df['company_name'] == selected_company].iloc[0]
                    
                    outcome = true_outcome_row['outcome']
                    roi = true_outcome_row['roi_potential']

                    # Use columns for a cleaner layout
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if pd.notna(outcome) and isinstance(outcome, str):
                            st.markdown(f"**Outcome:**")
                            st.info(f"{outcome}")
                        else:
                            st.markdown("**Outcome:**")
                            st.warning("No outcome data available.")

                    with col2:
                        if pd.notna(roi) and roi > 0:
                            st.metric(label="Simulated Return on Investment", value=f"{roi:.2f}x")
                        elif pd.notna(roi) and roi < 0:
                            st.metric(label="Simulated Return on Investment", value="-100%", delta_color="inverse")
                        else:
                            st.metric(label="Simulated Return on Investment", value="N/A")

    components.render_footer()

if __name__ == "__main__":
    main()
