# biomech_logic.py

import pandas as pd
import os
import datetime
import plotly.express as px

DATA_FILE = "responses.csv"

# Create CSV if not exists
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "timestamp", "age", "gender", "weight", "foot_type",
        "activity", "current_footwear", "arch_support",
        "cushioning", "shoe_type", "materials", "notes"
    ]).to_csv(DATA_FILE, index=False)

def recommend_biomechanics(age, gender, weight, foot_type, activity, current_footwear):
    """Biomechanics logic and recommendation engine."""
    age = int(age)
    weight = float(weight)

    # Arch Support
    if foot_type.lower() == "flat":
        arch = "High Stability / Motion Control"
    elif foot_type.lower() == "high arch":
        arch = "Low Support / Flexible Cushioning"
    else:
        arch = "Moderate / Neutral Arch Support"

    # Cushioning
    cushioning = (
        "High" if weight > 80 or age > 55
        else "Moderate" if 60 < weight <= 80
        else "Lightweight Responsive"
    )

    # Shoe Type
    if "high" in activity.lower():
        shoe = "Performance Running / Cross Training"
    elif "moderate" in activity.lower():
        shoe = "Walking / Gym"
    else:
        shoe = "Casual / Comfort Wear"

    # Material Recommendation
    materials = []

    if cushioning == "High":
        materials.append("EVA or PU midsole for maximum shock absorption")
    elif cushioning == "Moderate":
        materials.append("Dual-density EVA/TPU for balanced support and flexibility")
    else:
        materials.append("Pebax or TPU foam for lightweight responsiveness")

    if "flat" in foot_type.lower():
        materials.append("Orthotic insole with firm medial arch support")
    elif "high" in foot_type.lower():
        materials.append("Full-length gel/memory foam insole for pressure balance")
    else:
        materials.append("Neutral EVA insole for comfort and stability")

    if age > 50:
        materials.append("Engineered mesh upper with structural overlays")
    else:
        materials.append("Lightweight knit upper for breathability")

    materials.append("Durable rubber outsole with flex grooves")

    # Additional Notes
    notes = []
    if gender.lower() == "female":
        notes.append("Use women-specific lasts for narrow heels and fit accuracy.")
    if weight > 100:
        notes.append("Choose reinforced outsole and midsole for durability.")
    if "casual" in shoe.lower():
        notes.append("Opt for slip-resistant sole for daily comfort.")

    # Save to CSV
    df = pd.read_csv(DATA_FILE)
    new_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "age": age,
        "gender": gender,
        "weight": weight,
        "foot_type": foot_type,
        "activity": activity,
        "current_footwear": current_footwear,
        "arch_support": arch,
        "cushioning": cushioning,
        "shoe_type": shoe,
        "materials": ", ".join(materials),
        "notes": " ".join(notes),
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    return arch, cushioning, shoe, materials, notes


def build_trend_chart():
    """Return Plotly chart (HTML) for foot type vs shoe type."""
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return "<p>No data available yet. Submit a few entries to view trends.</p>"
    fig = px.histogram(
        df,
        x="foot_type",
        color="shoe_type",
        title="Biomechanics Trends: Foot Type vs Shoe Category",
        barmode="group",
        text_auto=True
    )
    fig.update_layout(width=700, height=400, margin=dict(l=20, r=20, t=50, b=20))
    return fig.to_html(full_html=False)
