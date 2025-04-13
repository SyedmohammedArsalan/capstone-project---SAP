import streamlit as st
import base64
from PIL import Image
import requests
from detect import detect_clothes
from recommend import (
    get_item_description,
    get_style_feedback,
    get_personalized_recommendations,
    get_color_palette
)
from feedback import UserPreferences
from shop_integration import get_shopping_links

# Custom CSS Loader
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize User Preferences
prefs = UserPreferences()

# Page Config
st.set_page_config(
    page_title="FashionMind AI",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
local_css("styles.css")

# Authored By Section
st.sidebar.markdown("""
<div class="authored-by">
    <div class="pulse"></div>
    AI Stylist v2.0
</div>
""", unsafe_allow_html=True)

# Main Navigation
page = st.sidebar.radio("Navigate", [
    "🖼️ Virtual Dressing Room",
    "🎨 Style Analyzer", 
    "✨ AI Recommendations",
    "🛍️ Shop Looks",
    "⚙️ Preferences"
])

# --------------------------
# Virtual Dressing Room Page
# --------------------------
if page == "🖼️ Virtual Dressing Room":
    st.header("👗 Virtual Dressing Room")
    col1, col2 = st.columns([2, 3])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Your Photo", type=["jpg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Your Base Look", use_column_width=True)
            
    with col2:
        st.markdown("### Try These AI-Generated Outfits")
        outfits = get_personalized_recommendations(prefs)
        
        # Responsive Grid
        cols = st.columns(3)
        for idx, outfit in enumerate(outfits[:6]):
            with cols[idx % 3]:
                with st.container():
                    st.image(outfit['image'], use_column_width=True)
                    st.markdown(f"**{outfit['name']}**")
                    st.caption(outfit['description'])
                    st.button("Try This →", key=f"try_{idx}")

# ----------------------
# Style Analyzer Page
# ----------------------
elif page == "🎨 Style Analyzer":
    st.header("🔍 AI Style Analysis")
    
    uploaded_file = st.file_uploader("Upload Your Outfit", type=["jpg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        with st.spinner("Analyzing..."):
            # Detection
            items = detect_clothes(img)
            
            # Color Analysis
            palette = get_color_palette(img)
            
            # Create Layout
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.image(img, use_column_width=True)
                st.markdown("### 🎨 Color Palette")
                st.image(palette, width=300)
                
            with col2:
                st.markdown("### 👕 Detected Items")
                for item in items:
                    with st.expander(f"{item['label']} ({(item['score']*100):.1f}%)"):
                        st.json(item)
                        desc = get_item_description(item['image'])
                        st.markdown(f"*{desc}*")
                        
                st.markdown("### 💡 Style Feedback")
                feedback = get_style_feedback(items, prefs)
                st.success(feedback)
                
                # Shopping Links
                st.markdown("### 🛍️ Buy Similar Items")
                links = get_shopping_links(items)
                for link in links[:3]:
                    st.markdown(f"[{link['store']}] {link['name']}")

# --------------------------
# AI Recommendations Page
# --------------------------
elif page == "✨ AI Recommendations":
    st.header("🌟 Personalized Recommendations")
    
    # Recommendation Filters
    with st.sidebar:
        st.subheader("Filters")
        style = st.selectbox("Preferred Style", prefs.get_styles())
        price_range = st.slider("Price Range", 0, 500, (50, 200))
        
    # Generate Recommendations
    recs = get_personalized_recommendations(prefs, style, price_range)
    
    # Animated Cards
    for rec in recs:
        with st.container():
            st.markdown(f"### {rec['title']}")
            cols = st.columns([1, 4])
            with cols[0]:
                st.image(rec['image'], width=200)
            with cols[1]:
                st.markdown(rec['description'])
                st.progress(rec['match_score'])
                st.markdown(f"**Price Range:** ${rec['price'][0]} - ${rec['price'][1]}")
                st.button("View Details →", key=rec['id'])

# ------------------
# Shop Looks Page
# ------------------
elif page == "🛍️ Shop Looks":
    st.header("🛒 Shop Curated Looks")
    
    # Partner Integrations
    partners = st.columns(3)
    partners[0].image("assets/hm.png", width=100)
    partners[1].image("assets/myntra.png", width=100)
    partners[2].image("assets/ajio.png", width=100)
    
    # Product Grid
    st.markdown("### Trending Now")
    products = get_shopping_links([], category="trending")
    cols = st.columns(4)
    for idx, product in enumerate(products[:8]):
        with cols[idx % 4]:
            with st.container():
                st.image(product['image'], use_column_width=True)
                st.markdown(f"**{product['name']}**")
                st.markdown(f"${product['price']}")
                st.markdown(f"[Buy Now]({product['url']})")

# ------------------
# Preferences Page
# ------------------
elif page == "⚙️ Preferences":
    st.header("⚙️ Style Preferences")
    
    with st.form("prefs_form"):
        # Style Preferences
        st.subheader("Your Style Profile")
        styles = st.multiselect(
            "Favorite Styles",
            ["Casual", "Formal", "Bohemian", "Streetwear"],
            default=prefs.styles
        )
        
        # Color Preferences
        colors = st.multiselect(
            "Preferred Colors",
            ["Neutral", "Pastel", "Vibrant", "Dark Tones"],
            default=prefs.colors
        )
        
        # Budget
        budget = st.slider(
            "Monthly Fashion Budget ($)",
            0, 1000, prefs.budget
        )
        
        if st.form_submit_button("Save Preferences"):
            prefs.update(styles, colors, budget)
            st.success("Preferences Updated!")