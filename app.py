import streamlit as st
import utils
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="StyleGenie | Digital Stylist",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&family=Montserrat:wght@400;500;600&display=swap');

        /* PALETTE replaced by CSS Variables */
        :root {
            --bg-main: #F6F1E9; /* Soft Cream */
            --bg-nav: rgba(246, 241, 233, 0.98);
            --bg-card: #FFFFFF;
            --bg-secondary: #FAFAFA; /* Warm White */
            --text-heading: #1F1F1F; /* Charcoal */
            --text-body: #1F1F1F;
            --text-secondary: #6E6E6E; /* Soft Grey */
            --text-accent: #6E6E6E;
            --accent-color: #C6A969; /* Luxury Gold */
            --border-color: #E6E6E6; /* Light Grey Dividers */
            --btn-bg: #1F1F1F;
            --btn-text: #FFFFFF;
            --btn-hover-bg: #C6A969;
            --btn-hover-text: #FFFFFF;
            --btn-secondary-border: #1F1F1F;
            --btn-secondary-text: #1F1F1F;
            --btn-secondary-hover: #FAFAFA;
            --shadow-color: rgba(0,0,0,0.04);
            --sidebar-bg: #FFFFFF;
            --sidebar-border: #E6E6E6;
            --footer-bg: #1F1F1F;
            --footer-text: #FAFAFA;
            --footer-secondary: #FAFAFA;
            --feature-num: #E6E6E6;
            --hero-gradient: linear-gradient(135deg, #F6F1E9 0%, #FAFAFA 100%);
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-main: #0A0A0A;
                --bg-nav: rgba(10, 10, 10, 0.98);
                --bg-card: #141414;
                --bg-secondary: #1E1E1E;
                --text-heading: #FFFFFF;
                --text-body: #E0E0E0;
                --text-secondary: #888888;
                --text-accent: #888888;
                --accent-color: #D4AF37;
                --border-color: #2A2A2A;
                --btn-bg: #FFFFFF;
                --btn-text: #121212;
                --btn-hover-bg: #D4AF37;
                --btn-hover-text: #121212;
                --btn-secondary-border: #FFFFFF;
                --btn-secondary-text: #FFFFFF;
                --btn-secondary-hover: #1A1A1A;
                --shadow-color: rgba(0,0,0,0.6);
                --sidebar-bg: #101010;
                --sidebar-border: #2A2A2A;
                --footer-bg: #050505;
                --footer-text: #FFFFFF;
                --footer-secondary: #777777;
                --feature-num: #1A1A1A;
                --hero-gradient: linear-gradient(135deg, #0A0A0A 0%, #141414 100%);
            }
        }

        /* Streamlit Input Overrides for Seamless Look */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            background-color: var(--bg-secondary) !important;
            color: var(--text-heading) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 6px !important;
            padding: 10px !important;
        }

        /* Sidebar Styling Refinements */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            padding: 20px;
            background-image: linear-gradient(
                rgba(0,0,0,0.85),
                rgba(0,0,0,0.92)
            ), url("https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?q=80&w=1000&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }
        
        /* Fix Streamlit Header Background */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Global Reset */
        .stApp {
            background-color: var(--bg-main) !important;
        }

        /* Smooth Scrolling */
        html {
            scroll-behavior: smooth;
        }

        /* Typography */
        h1, h2, h3, h4, h5 {
            font-family: 'Playfair Display', serif !important;
            color: var(--text-heading) !important;
            letter-spacing: -0.5px;
        }
        
        p, div, span, label, input {
            font-family: 'Lato', sans-serif !important;
            color: var(--text-body);
        }

        /* Navbar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            background-color: var(--bg-nav);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 9999;
            border-bottom: 1px solid var(--border-color);
            box-shadow: 0 4px 15px var(--shadow-color);
            margin: -6rem -4rem 2rem -4rem; /* Extend to edges of Streamlit container */
        }
        .navbar-brand {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-heading);
            letter-spacing: -0.5px;
        }
        .navbar-links {
            display: flex;
            align-items: center;
        }
        .navbar-links a.nav-link {
            text-decoration: none;
            color: var(--text-body);
            font-size: 0.95rem;
            font-weight: 500;
            margin-left: 35px;
            position: relative;
            transition: color 0.3s ease;
        }
        .navbar-links a.nav-link:hover {
            color: var(--text-heading);
        }
        .navbar-links a.nav-link::after {
            content: '';
            position: absolute;
            width: 0;
            height: 1px;
            bottom: -5px;
            left: 0;
            background-color: var(--text-heading);
            transition: width 0.3s ease;
        }
        .navbar-links a.nav-link:hover::after {
            width: 100%;
        }

        .nav-btn-outline {
            text-decoration: none !important;
            color: var(--btn-secondary-text) !important;
            border: 1px solid var(--btn-secondary-border);
            padding: 6px 16px;
            border-radius: 4px;
            margin-left: 35px !important;
            transition: all 0.3s ease;
            font-weight: 600 !important;
            font-size: 0.95rem;
        }
        .nav-btn-outline:hover {
            background-color: var(--btn-secondary-hover) !important;
            color: var(--btn-secondary-text) !important;
        }

        .nav-btn-solid {
            text-decoration: none !important;
            background-color: var(--btn-bg) !important;
            color: var(--btn-text) !important;
            padding: 6px 16px;
            border-radius: 4px;
            margin-left: 15px !important;
            transition: all 0.3s ease;
            font-weight: 600 !important;
            font-size: 0.95rem;
            box-shadow: 0 4px 6px var(--shadow-color);
        }
        .nav-btn-solid:hover {
            background-color: var(--btn-hover-bg) !important;
            color: var(--btn-hover-text) !important;
            transform: translateY(-2px);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Hero Section (Re-styled for Full Width Background) */
        .hero-wrapper {
            margin: -2rem -4rem 3rem -4rem;
            padding: 100px 40px;
            background-image: linear-gradient(
                rgba(0,0,0,0.75),
                rgba(0,0,0,0.85)
            ), url("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed; /* Subtle parallax effect */
            box-shadow: inset 0 0 150px rgba(0,0,0,0.9); /* Vignette */
            position: relative;
        }

        .hero-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            animation: fadeIn 1s ease-out;
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
            border-radius: 12px;
        }
        
        .hero-content {
            flex: 1;
            padding-right: 20px;
        }

        .hero-title {
            font-size: 4.5rem;
            font-weight: 700;
            margin-bottom: 5px;
            color: #FFFFFF !important;
            line-height: 1.1;
            text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        
        .hero-tagline {
            font-size: 1.5rem;
            color: #D4AF37 !important; /* Soft Gold */
            font-family: 'Playfair Display', serif !important;
            font-style: italic;
            margin-bottom: 20px;
        }

        .hero-desc {
            font-size: 1.1rem;
            color: #F0F0F0 !important;
            max-width: 500px;
            margin-bottom: 40px;
            line-height: 1.6;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        .hero-image-wrapper {
            flex: 1;
            display: flex;
            justify-content: flex-end;
            position: relative;
        }

        .hero-img {
            width: 100%;
            max-width: 550px;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 20px 40px var(--shadow-color);
            object-fit: cover;
            aspect-ratio: 4/5;
        }

        /* Feature Cards (Home) */
        .feature-card {
            background-color: var(--bg-card);
            padding: 40px 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px var(--shadow-color);
            text-align: center;
            height: 100%;
            border: 1px solid var(--border-color);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 35px var(--shadow-color);
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: var(--accent-color);
        }
        .feature-number {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            color: var(--feature-num);
            font-weight: 700;
            line-height: 1;
            margin-bottom: -15px;
            text-align: center;
            opacity: 0.7;
        }
        .feature-card h4 {
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: var(--text-heading) !important;
            z-index: 1;
        }

        /* Featured Styles Card (With Image) */
        .style-card-container {
            background-color: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px var(--shadow-color);
            transition: all 0.4s ease;
            border: 1px solid var(--border-color);
            text-decoration: none;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .style-card-container:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 15px 30px var(--shadow-color);
        }
        .style-img-wrapper {
            width: 100%;
            height: 250px;
            overflow: hidden;
        }
        .style-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.8s ease;
        }
        .style-card-container:hover .style-img {
            transform: scale(1.08); /* Zoom effect on hover */
        }
        .style-card-content {
            padding: 20px 15px;
            text-align: center;
        }
        .style-card-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-heading);
            margin-bottom: 5px;
        }
        .style-card-desc {
            font-family: 'Lato', sans-serif;
            font-size: 0.85rem;
            color: var(--text-body);
            line-height: 1.4;
        }

        /* Buttons - Primary Charcoal/Gold */
        .stButton > button {
            background-color: var(--btn-bg) !important;
            color: var(--btn-text) !important;
            border: none !important;
            border-radius: 2px !important;
            padding: 14px 40px !important;
            text-transform: uppercase;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 500 !important;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px var(--shadow-color);
        }
        .stButton > button:hover {
            background-color: var(--btn-hover-bg) !important;
            color: var(--btn-hover-text) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(198,169,105,0.3);
        }
        
        /* Footer */
        .footer-container {
            background-color: var(--footer-bg);
            padding: 60px 40px 30px 40px;
            text-align: center;
            margin: 60px -4rem -4rem -4rem; /* Extend to edges */
        }
        .footer-brand {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            color: var(--footer-text);
            margin-bottom: 10px;
        }
        .footer-tagline {
            color: var(--footer-secondary);
            font-size: 0.95rem;
            margin-bottom: 30px;
            font-style: italic;
            font-family: 'Playfair Display', serif;
        }
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 40px;
        }
        .footer-links a {
            color: var(--footer-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            font-family: 'Montserrat', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: color 0.3s ease;
        }
        .footer-links a:hover {
            color: var(--accent-color);
        }
        .footer-bottom {
            border-top: 1px solid var(--text-body);
            padding-top: 20px;
            color: var(--footer-secondary);
            font-size: 0.85rem;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            border-right: 1px solid var(--sidebar-border);
        }
        
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.7);
        }
        
        section[data-testid="stSidebar"] label {
            color: #FFFFFF !important;
            font-weight: 500 !important;
            letter-spacing: 0.5px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.7);
        }
        
        section[data-testid="stSidebar"] .stMarkdown p {
             color: #E0E0E0 !important;
             text-shadow: 0 1px 2px rgba(0,0,0,0.7);
        }
        
        section[data-testid="stSidebar"] div[role="radiogroup"] label p,
        section[data-testid="stSidebar"] div[data-baseweb="select"] div,
        section[data-testid="stSidebar"] .stNumberInput label p,
        section[data-testid="stSidebar"] .stSelectbox label p {
            color: #FFFFFF !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.7);
        }

        /* Result Cards (App) - Refined */
        .rec-container {
            background-color: var(--bg-card);
            border-radius: 10px;
            padding: 50px;
            box-shadow: 0 4px 12px var(--shadow-color);
            border: 1px solid var(--border-color);
            margin-top: 20px;
        }

        .divider-vertical {
            border-left: 1px solid var(--border-color);
            height: 100%;
            margin: 0 auto;
        }
        
        .label-small {
            font-family: 'Montserrat', sans-serif;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-secondary);
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .value-large {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            color: var(--text-heading);
            line-height: 1.2;
            margin-bottom: 5px;
        }
        
        .rec-subtext {
             font-family: 'Lato', sans-serif;
             font-size: 0.95rem;
             color: var(--text-accent);
             font-style: italic;
        }

        /* Body Type Hero Display */
        .body-type-container {
            background-color: var(--bg-card);
            padding: 50px 40px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid var(--border-color);
            margin-bottom: 30px;
            box-shadow: 0 4px 15px var(--shadow-color);
        }
        .body-type-label {
            font-family: 'Montserrat', sans-serif;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 15px;
        }
        .body-type-title {
            font-family: 'Playfair Display', serif;
            font-size: 4rem; 
            font-weight: 700;
            color: var(--text-heading);
            margin: 0;
            line-height: 1;
        }
        .body-type-reason {
            margin-top: 20px;
            font-size: 1.05rem;
            color: var(--text-body);
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }
        
        /* Accessory Pills */
        .acc-pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 10px;
        }
        .acc-pill {
            background-color: var(--border-color);
            border: 1px solid transparent;
            color: var(--text-heading);
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-family: 'Lato', sans-serif;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        .acc-pill:hover {
            background-color: var(--accent-color);
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

# --- VIEWS ---

def show_home():
    """Renders the Professional Home Page"""
    
    # Navbar
    st.markdown("""
        <div class="navbar" id="home">
            <div class="navbar-brand">StyleGenie</div>
            <div class="navbar-links">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#how-it-works" class="nav-btn-outline">How It Works</a>
                <a href="#" class="nav-btn-solid">Deploy</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero-wrapper">
            <div class="hero-container">
                <div class="hero-content">
                    <h1 class="hero-title">StyleGenie</h1>
                    <p class="hero-tagline">The Art of Algorithmic Elegance</p>
                    <p class="hero-desc">AI-powered styling based on body geometry. Elevate your wardrobe with algorithmic precision and absolute luxury.</p>
                </div>
                <div class="hero-image-wrapper">
                    <img class="hero-img" src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" alt="Fashion Model styling a modern outfit">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Call to Action Center
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        if st.button("GET STYLE RECOMMENDATION", use_container_width=True):
            navigate_to('app')

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # Features Section (How It Works)
    st.markdown("<h2 id='how-it-works' style='text-align: center; margin-bottom: 50px; font-size: 2.5rem;'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-number">01</div>
                <div class="feature-icon">📏</div>
                <h4>Analyze</h4>
                <p style="font-size: 1rem; line-height: 1.6; color: var(--text-accent);">
                    We process your precise measurements using advanced ratio logic to accurately identify your unique body geometry.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-number">02</div>
                <div class="feature-icon">✨</div>
                <h4>Curate</h4>
                <p style="font-size: 1rem; line-height: 1.6; color: var(--text-accent);">
                    Our engine meticulously filters through exclusive datasets to hand-select pieces that harmonize flawlessly with your shape.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-number">03</div>
                <div class="feature-icon">👔</div>
                <h4>Style</h4>
                <p style="font-size: 1rem; line-height: 1.6; color: var(--text-accent);">
                    Receive a complete, cohesive ensemble including seasonal premium fabrics and carefully matched finishing accessories.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Featured Styles Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px; font-size: 2.5rem;'>Explore Style Categories</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--text-accent); font-size: 1.1rem; margin-bottom: 50px;'>Discover aesthetics crafted for every occasion.</p>", unsafe_allow_html=True)
    
    style_c1, style_c2, style_c3, style_c4, style_c5 = st.columns(5)
    
    with style_c1:
        st.markdown("""
            <a href="#" class="style-card-container">
                <div class="style-img-wrapper">
                    <img class="style-img" src="https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Casual Style">
                </div>
                <div class="style-card-content">
                    <div class="style-card-title">Casual</div>
                    <div class="style-card-desc">Effortless everyday wear</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    with style_c2:
        st.markdown("""
            <a href="#" class="style-card-container">
                <div class="style-img-wrapper">
                    <img class="style-img" src="https://images.unsplash.com/photo-1507679799987-c73779587ccf?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Business Style">
                </div>
                <div class="style-card-content">
                    <div class="style-card-title">Business</div>
                    <div class="style-card-desc">Sharp professional attire</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    with style_c3:
        st.markdown("""
            <a href="#" class="style-card-container">
                <div class="style-img-wrapper">
                    <img class="style-img" src="https://images.unsplash.com/photo-1566206091558-7f218b696731?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Party Outfit">
                </div>
                <div class="style-card-content">
                    <div class="style-card-title">Party</div>
                    <div class="style-card-desc">Elegant evening looks</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    with style_c4:
        st.markdown("""
            <a href="#" class="style-card-container">
                <div class="style-img-wrapper">
                    <img class="style-img" src="https://images.unsplash.com/photo-1518310383802-640c2de311b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Athleisure">
                </div>
                <div class="style-card-content">
                    <div class="style-card-title">Athleisure</div>
                    <div class="style-card-desc">Active lifestyle pieces</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
        
    with style_c5:
        st.markdown("""
            <a href="#" class="style-card-container">
                <div class="style-img-wrapper">
                    <img class="style-img" src="https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=600&q=80" alt="Ethnic Wear">
                </div>
                <div class="style-card-content">
                    <div class="style-card-title">Ethnic</div>
                    <div class="style-card-desc">Traditional elegance</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # Bottom CTA Section
    st.markdown("""
        <div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
            <h2 style="font-size: 2.8rem; margin-bottom: 15px;">Discover your perfect outfit</h2>
            <p style="font-size: 1.15rem; color: var(--text-accent); max-width: 600px; margin: 0 auto 30px auto; line-height: 1.6;">
                Our algorithm analyzes your body type and matches styles that suit you best.<br>Step into a world of algorithmic elegance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c_cta1, c_cta2, c_cta3 = st.columns([1, 1.5, 1])
    with c_cta2:
        if st.button("START STYLING", key="start_styling_bottom", use_container_width=True):
            navigate_to('app')
            
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer-container" id="about">
            <div class="footer-brand">StyleGenie</div>
            <div class="footer-tagline">AI-powered styling platform</div>
            <div class="footer-links">
                <a href="#home">Home</a>
                <a href="#how-it-works">Recommendation</a>
                <a href="#about">About</a>
            </div>
            <div class="footer-bottom">
                &copy; 2026 StyleGenie. All rights reserved. <br/> The Art of Algorithmic Elegance.
            </div>
        </div>
    """, unsafe_allow_html=True)


def show_app():
    """Renders the Recommendation App Page"""
    
    # Page-Specific Styling for Fashion Editorial Look
    st.markdown("""
        <style>
            /* Fashion Editorial Full Background */
            .stApp {
                background-image: 
                    linear-gradient(rgba(0,0,0,0.70), rgba(0,0,0,0.85)),
                    url("https://www.transparenttextures.com/patterns/woven-light.png"),
                    url("https://images.unsplash.com/photo-1469334031218-e382a71b716b?q=80&w=2070&auto=format&fit=crop") !important;
                background-color: transparent !important;
                background-size: auto, auto, cover !important;
                background-position: center, center, center !important;
                background-attachment: fixed, fixed, fixed !important;
                background-repeat: repeat, repeat, no-repeat !important;
                transition: background 0.5s ease-in-out;
            }

            /* Glassmorphism Cards */
            .body-type-container, .rec-container, .empty-state-container {
                background: rgba(20,20,20,0.75) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255,255,255,0.05) !important;
                border-radius: 14px !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
                color: #FFFFFF !important;
                animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                opacity: 0;
            }
            .rec-container {
                animation-delay: 0.2s;
            }

            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .body-type-container:hover, .rec-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.4) !important;
                transition: all 0.4s ease;
            }
            
            /* Body Type Highlight */
            .body-type-label {
                color: #A0A0A0 !important;
                letter-spacing: 4px !important;
            }
            .body-type-title {
                font-family: 'Playfair Display', serif !important;
                font-size: 4.5rem !important;
                color: #D4AF37 !important; /* Gold */
                text-shadow: 0 0 20px rgba(212,175,55,0.4) !important;
            }
            .body-type-reason {
                color: #E0E0E0 !important;
            }
            
            /* Typography in Sections */
            .label-small {
                font-variant: small-caps;
                font-size: 0.85rem !important;
                color: #A0A0A0 !important;
                letter-spacing: 2.5px !important;
            }
            .value-large {
                font-size: 2.4rem !important;
                color: #FFFFFF !important;
                font-family: 'Playfair Display', serif !important;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
            }
            .rec-subtext {
                color: #999999 !important;
            }

            /* Accessory Tags (Fashion Pill) */
            .acc-pill {
                background: rgba(255,255,255,0.08) !important;
                border-radius: 20px !important;
                padding: 6px 14px !important;
                font-size: 13px !important;
                color: #FFFFFF !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                letter-spacing: 1px !important;
                transition: all 0.3s ease !important;
            }
            .acc-pill:hover {
                background: rgba(212,175,55,0.2) !important; /* Gold tint */
                border-color: #D4AF37 !important;
                box-shadow: 0 0 10px rgba(212,175,55,0.3) !important;
                transform: translateY(-2px);
            }
            
            /* Main Divider */
            .divider-vertical {
                border-left: 1px solid rgba(255,255,255,0.1) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Load Data
    data = utils.load_data()

    # Sidebar
    with st.sidebar:
        # We can use empty containers or markdown to create spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; color: #FFFFFF !important; text-shadow: 0 1px 3px rgba(0,0,0,0.8); margin-bottom: 30px;'>Profile Setup</h2>", unsafe_allow_html=True)
        
        # Profile Inputs
        st.markdown("<p style='color: #E0E0E0; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(0,0,0,0.8);'>BASICS</p>", unsafe_allow_html=True)
        gender_input = st.selectbox("Gender", ["Female", "Male"], label_visibility="collapsed")
        gender_mapped = "Women" if gender_input == "Female" else "Men"
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #E0E0E0; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(0,0,0,0.8);'>MEASUREMENTS</p>", unsafe_allow_html=True)
        unit = st.radio("Unit", ["cm", "in"], horizontal=True, label_visibility="collapsed")
        input_unit = "Inches" if unit == "in" else "Cm"
        
        # Measurement Inputs
        # Using columns for tighter layout
        chest_val = st.number_input(f"Chest/Bust ({unit})", value=90.0 if unit=="cm" else 36.0, step=0.5)
        waist_val = st.number_input(f"Waist ({unit})", value=70.0 if unit=="cm" else 28.0, step=0.5)
        hips_val = st.number_input(f"Hips ({unit})", value=95.0 if unit=="cm" else 38.0, step=0.5)
        
        # Conversion
        chest_cm = utils.convert_to_cm(chest_val, input_unit)
        waist_cm = utils.convert_to_cm(waist_val, input_unit)
        hips_cm = utils.convert_to_cm(hips_val, input_unit)
        
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<p style='color: #E0E0E0; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 5px; text-shadow: 0 1px 2px rgba(0,0,0,0.8);'>CONTEXT</p>", unsafe_allow_html=True)
        season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
        occasion = st.selectbox("Occasion", ["Casual", "Business", "Party", "Gym/Sport", "Ethnic"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        generate_btn = st.button("GENERATE STYLE", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← GO BACK", use_container_width=True):
             navigate_to('home')


    # Main Area
    # Header
    st.markdown("<h2 style='text-align: left; margin-bottom: 5px; color: #FFFFFF; font-family: Playfair Display, serif; text-shadow: 0 2px 5px rgba(0,0,0,0.8);'>Your Curated Style</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='color: #D4AF37; margin-bottom: 40px; font-family: Lato; letter-spacing: 1px; text-shadow: 0 1px 3px rgba(0,0,0,0.8);'>Based on your unique geometry for <b>{season} {occasion}</b></div>", unsafe_allow_html=True)

    if generate_btn:
        with st.spinner("Analyzing proportions & curating look..."):
            time.sleep(0.8) # Premium feel delay
            
            # Logic
            body_type, reason = utils.determine_body_type(gender_input, chest_cm, waist_cm, hips_cm)
            outfits = utils.get_recommendation(data, gender_mapped, body_type, season, occasion)
            
            if outfits:
                # 1. BODY TYPE DISPLAY (Prominent)
                st.markdown(f"""
                    <div class="body-type-container">
                        <div class="body-type-label">Detected Body Architecture</div>
                        <h1 class="body-type-title">{body_type}</h1>
                        <div class="body-type-reason">{reason}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 2. MULTIPLE OUTFIT TABS
                tab_names = [f"✨ {o['Outfit Name']}" for o in outfits]
                tabs = st.tabs(tab_names)
                
                for i, tab in enumerate(tabs):
                    with tab:
                        o = outfits[i]
                        
                        # Score and Style Pill
                        st.markdown(f"""
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 10px; margin-bottom: 20px;'>
                                <div>
                                    <span style='background: rgba(212,175,55,0.2); border: 1px solid #D4AF37; color: #D4AF37; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; letter-spacing: 1px; margin-right: 15px; font-family: Montserrat;'>{o["Style Type"]}</span>
                                    <span style='background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #E0E0E0; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; letter-spacing: 1px; font-family: Montserrat;'>Score: {o["Fashion Score"]}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"<div style='color: #D4AF37; font-family: Lato; font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px; font-style: italic; border-left: 3px solid #D4AF37; padding-left: 15px;'>\"{o['Why It Matches']}\"</div>", unsafe_allow_html=True)

                        # RECOMMENDATION CARD
                        st.markdown('<div class="rec-container" style="margin-top: 0;">', unsafe_allow_html=True)
                        
                        c1, spacer, c2 = st.columns([1, 0.1, 1])
                        
                        with c1:
                            st.markdown('<div class="label-small">Upper Body</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="value-large" style="font-size: 1.8rem;">{o["Upper Wear"]}</div>', unsafe_allow_html=True)
                            
                            st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
                            
                            st.markdown('<div class="label-small">Lower Body</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="value-large" style="font-size: 1.8rem;">{o["Lower Wear"]}</div>', unsafe_allow_html=True)

                        with spacer:
                            st.markdown('<div class="divider-vertical"></div>', unsafe_allow_html=True)
                        
                        with c2:
                            st.markdown('<div class="label-small">Footwear</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="value-large" style="font-size: 1.6rem;">{o["Footwear"]}</div>', unsafe_allow_html=True)
                            
                            st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
                            
                            st.markdown('<div class="label-small">Curated Accessories</div>', unsafe_allow_html=True)
                            acc_list = [x.strip() for x in o["Accessories"].split(',')]
                            pills_html = '<div class="acc-pill-container">'
                            for acc in acc_list:
                                pills_html += f'<span class="acc-pill">{acc}</span>'
                            pills_html += '</div>'
                            st.markdown(pills_html, unsafe_allow_html=True)
                            
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Extra Details below card
                        st.markdown(f"""
                            <div style='display: flex; gap: 30px; margin-top: 20px; justify-content: center; color: #999999; font-size: 0.95rem; font-family: Lato;'>
                                <div><span style='color:#D4AF37;'>🎨</span> <b>Color Palette:</b> {o["Best Color Combination"]}</div>
                                <div><span style='color:#D4AF37;'>🌤️</span> <b>Season:</b> {o["Season Suitability"]}</div>
                                <div><span style='color:#D4AF37;'>🍷</span> <b>Occasion:</b> {o["Occasion Suitability"]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
            else:
                st.error("We couldn't match a specific outfit from the collection. Please try a different combination!")
    
    else:
        # Empty State
        st.markdown("""
            <div class="empty-state-container" style="
                height: 400px; 
                display: flex; 
                flex-direction: column;
                align-items: center; 
                justify-content: center; 
            ">
                <div style="font-size: 3rem; margin-bottom: 20px; opacity: 0.3;">✨</div>
                <div style="font-family: 'Lato'; letter-spacing: 1px; color: #E0E0E0;">Awaiting measurements to generate your profile.</div>
            </div>
        """, unsafe_allow_html=True)


# --- ROUTER ---
def main():
    if st.session_state.page == 'home':
        show_home()
    else:
        show_app()

if __name__ == "__main__":
    main()
