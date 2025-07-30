import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Research Paper Viewer", layout="wide")
st.title("📝 Research Paper Viewer")

API_URL = "http://127.0.0.1:5000/data"

# --- Categories list ---
LIST_CS_CATEGORIES = [
    'cs.AI', 'cs.AR', 'cs.CC', 'cs.CE', 'cs.CG', 'cs.CL', 'cs.CV',
    'cs.CR', 'cs.CY', 'cs.DB', 'cs.DC', 'cs.DL', 'cs.DM', 'cs.DS',
    'cs.ET', 'cs.FL', 'cs.GL', 'cs.GR', 'cs.GT', 'cs.HC',
    'cs.IR', 'cs.IT', 'cs.LG', 'cs.LO', 'cs.MA',
    'cs.MM', 'cs.MS', 'cs.NA', 'cs.NE', 'cs.NI', 'cs.OH', 'cs.OS',
    'cs.PF', 'cs.PL', 'cs.RO', 'cs.SC', 'cs.SD',
    'cs.SE', 'cs.SI', 'cs.SY'
]

# --- Query params ---
query_params = st.query_params
current_page = int(query_params.get("page", 1))
page_size = 10

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔍 Filters")

    available_years = [str(y) for y in range(2000, 2026)]
    selected_year = st.selectbox("Year", ["All"] + available_years)

    selected_categories = st.multiselect("Categories", LIST_CS_CATEGORIES)

    if st.button("Find"):
        # Reset page to 1
        st.query_params.update(page=1)
        st.session_state['filters_applied'] = True

# --- Only apply filters after clicking "Find" ---
if 'filters_applied' not in st.session_state:
    st.session_state['filters_applied'] = False

if st.session_state['filters_applied']:
    # Prepare backend request
    params = {'page': current_page, 'size': page_size}
    if selected_year != "All":
        params['year'] = selected_year
    for cat in selected_categories:
        params.setdefault('category', []).append(cat)

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        result = response.json()

        records = result['data']
        total_pages = result['total_pages']
        total_num_paper = result['total_rows']

        st.markdown(f"- Found {total_num_paper} papers.")
        st.markdown("---")

        # Display each record
        for record in records:
            with st.container():
                st.markdown(f"**{record.get('title')}**")
                st.markdown(f"**ID**: {record.get('id')}")
                st.markdown(f"**Authors**: {record.get('authors')}")
                st.markdown(f"**Journal Reference**: {record.get('journal-ref')}")
                st.markdown(f"**Categories**: `{record.get('categories')}`")
                st.markdown(f"**Updated**: {record.get('update_date')}")
                st.markdown(f"**Abstract:** {record.get('abstract')}")
                st.markdown(f"[Paper Link]({record.get('paper_url')})")
                st.markdown("---")

        if total_pages >= 1:
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("⬅️ Previous") and current_page > 1:
                    st.query_params.update(page=current_page - 1)
                    st.rerun()
            with col2:
                if st.button("Next ➡️") and current_page < total_pages:
                    st.query_params.update(page=current_page + 1)
                    st.rerun()
            with col3:
                new_page = st.number_input("Go to page ", min_value=1, max_value=total_pages, value=current_page)
                if new_page != current_page:
                    st.query_params.update(page=new_page)
                    st.rerun()
        else:
            st.warning("No results found for your filters. Try adjusting year or categories.")


    except Exception as e:
        st.error(f"Error fetching data: {e}")
else:
    st.info("Select filters and click **Find** to view results.")
