import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("🔍 SHL Assessment Recommender")

st.markdown("Enter a full SHL URL or a slug (e.g., `account-manager-solution`)")

user_input = st.text_input("SHL URL or Slug")

if st.button("Get Recommendations"):
    if not user_input.strip():
        st.warning("Please enter a valid URL or slug.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.post(
                    "https://shl-api-ns2u.onrender.com/recommend",
                    json={"input": user_input}
                )

                if response.status_code != 200:
                    st.error("❌ Something went wrong: " + response.text)
                else:
                    data = response.json()
                    st.write(data)

                    if "recommendations" in data:
                        st.success(f"✅ Recommendations for: `{data['job_slug']}`")

                        # Display tabular format
                        df = pd.DataFrame(data["recommendations"])
                        df["Assessment Name"] = df["Assessment Name"].apply(
                            lambda x: x.replace("[", "").replace(")", "").split("](")[0]
                        )
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("⚠️ Couldn't parse into table. Showing raw markdown:")
                        st.markdown(data.get("markdown_table", "*No result*"))
            except Exception as e:
                st.error(f"❌ Request failed: {str(e)}")
