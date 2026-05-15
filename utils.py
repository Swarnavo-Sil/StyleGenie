import pandas as pd
import streamlit as st
import random

# Dataset Paths (GitHub Raw URLs)
DATA_PATHS = {
    "upper": "https://raw.githubusercontent.com/Swarnavo-Sil/StyleGenie/main/Upper_Cloth.csv",
    "lower": "https://raw.githubusercontent.com/Swarnavo-Sil/StyleGenie/main/Lower_Wear.csv", 
    "fabric": "https://raw.githubusercontent.com/Swarnavo-Sil/StyleGenie/main/Fabrics.csv",
    "accessories": "https://raw.githubusercontent.com/Swarnavo-Sil/StyleGenie/main/Accessories.csv"
}

@st.cache_data
def load_data():
    """
    Loads all datasets and performs basic cleaning.
    """
    datasets = {}
    for key, url in DATA_PATHS.items():
        try:
            df = pd.read_csv(url, encoding="utf-8")
            # Standardize column names to striped lowercase
            df.columns = df.columns.str.strip().str.lower()
            # Clean string values
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            datasets[key] = df
        except Exception as e:
            st.error(f"Dataset loading failed: {e}")
            datasets[key] = pd.DataFrame()
    return datasets

def convert_to_cm(value, unit):
    """
    Converts measurement to cm if unit is inches.
    """
    if unit == "Inches" or unit == "in":
        return value * 2.54
    return value

def determine_body_type(gender, chest, waist, hips):
    """
    Determines body type based on measurements (in cm) and gender.
    Uses high-precision logic with ranges and ratios.
    Returns a tuple (body_type, reason).
    """
    # Precision Tolerance (cm)
    TOL = 2.5 
    
    classification = "Unknown"
    reason = "Could not classify based on current data."

    if gender == "Female" or gender == "Women":
        # Ratios calculations
        # Bust-Hips Difference
        bust_hips_diff = chest - hips
        
        # Waist Definition
        is_waist_defined = (chest - waist >= 15) and (hips - waist >= 15)
        
        # 1. Hourglass
        # Balanced Bust/Hips (within tolerance) AND Defined Waist
        if abs(bust_hips_diff) <= TOL + 3.0 and is_waist_defined:
            classification = "Hourglass"
            reason = "Your bust and hips are balanced with a clearly defined waist."
            
        # 2. Triangle (Pear)
        # Hips are significantly larger than bust
        elif hips > (chest + TOL):
            classification = "Triangle"
            reason = "Your hips are wider than your bust, creating a triangle shape."
            
        # 3. Inverted Triangle
        # Bust is significantly larger than hips
        elif chest > (hips + TOL):
            classification = "Inverted Triangle"
            reason = "Your bust/shoulders are wider than your hips."
            
        # 4. Round (Apple)
        # Waist is the largest measurement or close to largest
        elif (waist > chest - TOL) or (waist > hips - TOL):
            classification = "Round"
            reason = "Your waist is fuller, often wider than your bust or hips."
            
        # 5. Rectangle (Straight)
        # Measurements are fairly uniform
        else:
            classification = "Rectangle"
            reason = "Your bust, waist, and hips are fairly aligned with little curve."

    elif gender == "Male" or gender == "Men":
        # 1. V-Shape
        # Chest dominant over waist and hips
        if (chest > waist + 15) and (chest > hips + 5):
            classification = "V-Shape"
            reason = "Your broad chest tapers significantly to a narrower waist."
            
        # 2. Triangle
        # Hips are wider than chest
        elif hips > (chest + TOL):
            classification = "Triangle"
            reason = "Your hips are wider than your chest."
            
        # 3. Apple
        # Waist is wider than chest
        elif waist > (chest + TOL):
            classification = "Apple"
            reason = "Your waist measurement is larger than your chest measurement."
            
        # 4. Rectangle
        # Consistent measurements
        else:
            classification = "Rectangle"
            reason = "Your chest, waist, and hips are roughly the same width."
            
    # Fallback to key-only for dataset compatibility if needed, but returning full detail for UI
    # We must ensure the returned key matches CSV keys strictly.
    # CSV Keys: 'Hourglass', 'Triangle', 'Inverted Triangle', 'Round', 'Rectangle' (Female)
    # CSV Keys: 'V-Shape', 'Triangle', 'Apple', 'Rectangle' (Male)
    
    return classification, reason

def get_shoe_recommendation(gender, occasion, season):
    """
    Returns a single rule-based shoe recommendation based on constraints.
    """
    gender = gender.lower()
    occasion = occasion.lower()
    season = season.lower()
    
    shoe = "Classic Stylist Pick" # Default
    
    if gender == "men":
        if occasion == "casual":
            if season in ["winter", "autumn"]:
                shoe = "Leather Chelsea Boots"
            else:
                shoe = "Minimalist White Sneakers"
        elif occasion == "business":
            shoe = "Classic Leather Oxfords"
        elif occasion == "party":
            shoe = "Polished Dress Loafers"
        elif occasion == "gym/sport":
            shoe = "Performance Running Shoes"
        elif occasion == "ethnic":
            shoe = "Traditional Leather Juttis"
            
    elif gender == "women":
        if occasion == "casual":
            if season in ["summer", "spring"]:
                shoe = "Comfy Espadrilles or Flats"
            else:
                shoe = "Ankle Boots"
        elif occasion == "business":
            shoe = "Classic Pointed Pumps"
        elif occasion == "party":
            shoe = "Strappy High Heels"
        elif occasion == "gym/sport":
            shoe = "Lightweight Trainers"
        elif occasion == "ethnic":
            shoe = "Embellished Mojaris/Heels"
            
    return shoe

def get_recommendation(datasets, gender, body_type, season, occasion):
    """
    Filters datasets and returns a complete outfit recommendation.
    """
    outfit = {}
    
    # Get Shoe Recommendation (Rule-Based)
    outfit['shoe'] = get_shoe_recommendation(gender, occasion, season)
    
    # Common filter function
    def filter_df(df, item_col):
        if df.empty:
            return None
            
        # Flexible filtering:
        # 1. Exact Match
        mask = (
            (df['gender'].str.lower() == gender.lower()) & 
            (df['body_type'].str.lower() == body_type.lower()) & 
            (df['season'].str.lower() == season.lower()) & 
            (df['occasion'].str.lower() == occasion.lower())
        )
        filtered = df[mask]
        
        # 2. Relaxed Match (Drop Season if empty) implies classic pieces
        if filtered.empty:
             mask = (
                (df['gender'].str.lower() == gender.lower()) & 
                (df['body_type'].str.lower() == body_type.lower()) & 
                (df['occasion'].str.lower() == occasion.lower())
            )
             filtered = df[mask]
        
        # 3. Last Resort (Just Gender & Occasion)
        if filtered.empty:
             mask = (
                (df['gender'].str.lower() == gender.lower()) & 
                (df['occasion'].str.lower() == occasion.lower())
            )
             filtered = df[mask]
             
        if not filtered.empty:
            return filtered.sample(1).iloc[0]
        return None

    # Upper Wear
    upper_row = filter_df(datasets['upper'], 'upper_cloth')
    if upper_row is not None:
        outfit['upper'] = upper_row.get('upper_cloth', 'Top')
        outfit['upper_color'] = upper_row.get('color', 'Neutral')
    else:
        outfit['upper'] = "Classic Shirt"
        outfit['upper_color'] = "White"

    # Lower Wear
    lower_row = filter_df(datasets['lower'], 'lower_wear')
    if lower_row is not None:
        outfit['lower'] = lower_row.get('lower_wear', 'Pants')
        outfit['lower_color'] = lower_row.get('color', 'Black')
    else:
        outfit['lower'] = "Trousers"
        outfit['lower_color'] = "Black"

    # Fabric
    fabric_row = filter_df(datasets['fabric'], 'fabrics')
    if fabric_row is not None:
        outfit['fabric'] = fabric_row.get('fabrics', 'Cotton')
    else:
        outfit['fabric'] = "Cotton Blend"

    # Accessories
    acc_row = filter_df(datasets['accessories'], 'accessories')
    # Custom Multi-Select Logic for Accessories
    # We want 2-4 accessories. filter_df returns a single row series if successful, 
    # but we need the raw filtered df to sample multiple. We must re-filter manually or modify filter_df.
    # To avoid changing filter_df structure which affects others, we do a targeted re-filter here.
    
    acc_df = datasets['accessories']
    # Re-apply matching logic
    if not acc_df.empty:
        # Exact Match
        mask = (
            (acc_df['gender'].str.lower() == gender.lower()) & 
            (acc_df['season'].str.lower() == season.lower()) & 
            (acc_df['occasion'].str.lower() == occasion.lower())
        )
        filtered_acc = acc_df[mask]
        
        # Fallback: Relaxed (Gender + Occasion)
        if filtered_acc.empty:
             mask = (
                (acc_df['gender'].str.lower() == gender.lower()) & 
                (acc_df['occasion'].str.lower() == occasion.lower())
            )
             filtered_acc = acc_df[mask]
        
        if not filtered_acc.empty:
            # Sample 2 to 4 items
            import random
            count = min(len(filtered_acc), random.randint(2, 4))
            selected = filtered_acc.sample(count)
            items = selected['accessories'].unique().tolist()
            # Join uniques
            outfit['accessory'] = ", ".join(items)
        else:
            outfit['accessory'] = "Minimalist Watch"
    else:
        outfit['accessory'] = "Minimalist Watch"

    return outfit
