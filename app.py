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

    # --- Mode Selector ---
    st.sidebar.title("App Mode")
    app_mode = st.sidebar.radio("Choose your mode:", ('Live Tracker', 'Historical Analysis'))
    
    if app_mode == 'Live Tracker':
        st.header("Live Tracker")
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
            df = st.session_state.data
            df['Companies'] = df['title'].apply(ner.extract_company_names)
            df['Company Names'] = df['Companies'].apply(lambda x: ', '.join(x) if x else 'N/A')
            df['Signal Score'] = df.apply(scoring.calculate_signal_score, axis=1)
            display_columns = ['Company Names', 'Signal Score', 'source', 'title', 'description']
            display_df = df[df['Companies'].apply(lambda x: len(x) > 0)].copy()
            display_df = display_df.sort_values(by='Signal Score', ascending=False)
            st.dataframe(display_df[display_columns], use_container_width=True, hide_index=True)
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
        
        st.subheader(f"Top Signals as of {selected_date.strftime('%Y-%m-%d')}")
        top_signals_df = past_df.sort_values(by='Signal Score', ascending=False).head(10)

        # Let the user select a company to analyze
        st.dataframe(
            top_signals_df[['Signal Score', 'company_name', 'title']], 
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
