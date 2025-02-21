import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import io
from fastapi import Response

def generate_team_pace_comparison_plot(year: int, round_no: str, session_type: str):
    try:
        # Load FastF1's dark color scheme
        fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False,
                                  color_scheme='fastf1')

        # Load the race session
        race = fastf1.get_session(year, int(round_no), session_type)
        race.load(telemetry=False, weather=False)
        laps = race.laps.pick_quicklaps()

        # Convert lap times to seconds for Seaborn
        transformed_laps = laps.copy()
        transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

        # Order teams by their median lap times (fastest to slowest)
        team_order = (
            transformed_laps.groupby("Team")["LapTime (s)"]
            .median()
            .sort_values()
            .index
        )

        # Assign team colors
        team_palette = {team: fastf1.plotting.get_team_color(team, session=race) for team in team_order}

        # Create plot
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.boxplot(
            data=transformed_laps,
            x="Team",
            y="LapTime (s)",
            hue="Team",
            order=team_order,
            palette=team_palette,
            whiskerprops=dict(color="white"),
            boxprops=dict(edgecolor="white"),
            medianprops=dict(color="grey"),
            capprops=dict(color="white"),
        )

        plt.title(race.event['EventName'])
        plt.grid(visible=False)

        # Remove redundant x-label
        ax.set(xlabel=None)
        plt.tight_layout()

        # Save figure to an in-memory file
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
        plt.close(fig)  # Free memory
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}
