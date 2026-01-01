import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants (assuming running from src/ or similar, adjusting paths)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # src/
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")
WEATHER_PLUGIN_DIR = os.path.join(PLUGINS_DIR, "weather")
BASE_PLUGIN_DIR = os.path.join(PLUGINS_DIR, "base_plugin")
RENDER_DIR = os.path.join(WEATHER_PLUGIN_DIR, "render")
BASE_RENDER_DIR = os.path.join(BASE_PLUGIN_DIR, "render")
STATIC_DIR = os.path.join(BASE_DIR, "static")

def main():
    logger.info("Setting up Jinja2 environment...")
    loader = FileSystemLoader([RENDER_DIR, BASE_RENDER_DIR])
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Mock Data
    template_params = {
        "units": "metric",
        "last_refresh_time": "2023-10-27 10:00 AM",
        "title": "New York, NY",
        "current_date": "Friday, October 27",
        "current_day_icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/01d.png"),
        "current_temperature": "15",
        "feels_like": "14",
        "temperature_unit": "°C",
        "forecast": [
            {"day": "Fri", "high": 16, "low": 10, "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/01d.png"), "moon_phase_pct": "50", "moon_phase_icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/waxingcrescent.png")},
            {"day": "Sat", "high": 18, "low": 12, "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/02d.png"), "moon_phase_pct": "60", "moon_phase_icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/waxinggibbous.png")},
            {"day": "Sun", "high": 20, "low": 14, "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/03d.png"), "moon_phase_pct": "70", "moon_phase_icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/fullmoon.png")},
            {"day": "Mon", "high": 15, "low": 9,  "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/04d.png"), "moon_phase_pct": "80", "moon_phase_icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/waninggibbous.png")},
        ],
        "data_points": [
            {"label": "Sunrise", "measurement": "07:00", "unit": "AM", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/sunrise.png")},
            {"label": "Sunset", "measurement": "06:00", "unit": "PM", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/sunset.png")},
            {"label": "Wind", "measurement": "5", "unit": "m/s", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/wind.png"), "arrow": "->"},
            {"label": "Humidity", "measurement": "65", "unit": "%", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/humidity.png")},
            {"label": "Pressure", "measurement": "1012", "unit": "hPa", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/pressure.png")},
            {"label": "UV Index", "measurement": "3", "unit": "", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/uvi.png")},
            {"label": "Visibility", "measurement": ">10", "unit": "km", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/visibility.png")},
            {"label": "Air Quality", "measurement": "2", "unit": "Good", "icon": os.path.join(WEATHER_PLUGIN_DIR, "icons/aqi.png")},
        ],
        "hourly_forecast": [
            {"time": "10 AM", "temperature": 15, "precipitation": 0.0, "rain": 0.0},
            {"time": "11 AM", "temperature": 16, "precipitation": 0.1, "rain": 0.0},
            {"time": "12 PM", "temperature": 17, "precipitation": 0.2, "rain": 0.0},
            {"time": "1 PM", "temperature": 17, "precipitation": 0.0, "rain": 0.0},
            {"time": "2 PM", "temperature": 16, "precipitation": 0.0, "rain": 0.0},
        ],
        "plugin_settings": {
            "displayRefreshTime": "true",
            "displayMetrics": "true",
            "displayGraph": "true",
            "displayForecast": "true",
            "moonPhase": "true",
            "forecastDays": 4,
            "textColor": "#000000",
            "backgroundColor": "#ffffff",
            "selectedFrame": "None",
            # Margins
            "topMargin": 0,
            "rightMargin": 0,
            "bottomMargin": 0,
            "leftMargin": 0,
            
            "displayRain": "true"
        },
        "style_sheets": [
            os.path.join(BASE_RENDER_DIR, "plugin.css"),
            os.path.join(RENDER_DIR, "weather.css")
        ],
        "font_faces": [
            {"font_family": "Jost", "font_weight": "normal", "font_style": "normal", "url": os.path.join(STATIC_DIR, "fonts/Jost-Regular.ttf")},
            {"font_family": "Jost", "font_weight": "bold", "font_style": "normal", "url": os.path.join(STATIC_DIR, "fonts/Jost-Bold.ttf")}
        ],
        "static_dir": STATIC_DIR
    }

    # Generate Mock Chart
    times = [h["time"] for h in template_params["hourly_forecast"]]
    temps = [h["temperature"] for h in template_params["hourly_forecast"]]
    
    plt.figure(figsize=(10, 3), dpi=100)
    plt.plot(times, temps, marker='o', linestyle='-', color='white', linewidth=2)
    ax = plt.gca()
    ax.set_facecolor('none')
    plt.gcf().patch.set_alpha(0)
    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_visible(False)
    # Ticks
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.yticks([])
    # Labels
    for i, txt in enumerate(temps):
        ax.annotate(txt, (times[i], temps[i]), textcoords="offset points", xytext=(0,10), ha='center', color='white', fontweight='bold')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    plt.close()
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    template_params["chart_image"] = f"data:image/png;base64,{img_str}"

    # Render template
    logger.info("Rendering weather.html...")
    template = env.get_template("weather.html")
    rendered_html = template.render(template_params)

    output_file = "weather_debug.html"
    with open(output_file, "w") as f:
        f.write(rendered_html)
    
    logger.info(f"Generated {output_file}")
    print(f"File generated at: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
