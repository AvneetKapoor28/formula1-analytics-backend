import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import io
from fastapi import Response

# Enable FastF1's dark color scheme and setup timedelta support
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

def generate_laptime_distribution_plot(year: int, round_no: str, session_type: str):
    try:
        # Load the race session
        race = fastf1.get_session(year, int(round_no), session_type)
        race.load()

        # Get point finishers and their lap times
        point_finishers = race.drivers[:10]
        driver_laps = race.laps.pick_drivers(point_finishers).pick_quicklaps().reset_index()

        # Get drivers' abbreviations in finishing order
        finishing_order = [race.get_driver(i)["Abbreviation"] for i in point_finishers]

        # Convert LapTime to seconds for plotting
        driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 5))

        sns.violinplot(
            data=driver_laps,
            x="Driver",
            y="LapTime(s)",
            hue="Driver",
            inner=None,
            density_norm="area",
            order=finishing_order,
            palette=fastf1.plotting.get_driver_color_mapping(session=race)
        )

        sns.swarmplot(
            data=driver_laps,
            x="Driver",
            y="LapTime(s)",
            order=finishing_order,
            hue="Compound",
            palette=fastf1.plotting.get_compound_mapping(session=race),
            hue_order=["SOFT", "MEDIUM", "HARD"],
            linewidth=0,
            size=4
        )

        # Formatting
        ax.set_xlabel("Driver")
        ax.set_ylabel("Lap Time (s)")
        plt.suptitle(f"{year} {race.event['EventName']} Lap Time Distributions")
        sns.despine(left=True, bottom=True)

        plt.tight_layout()

        # Save figure to an in-memory file
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
        plt.close(fig)  # Free memory
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}
