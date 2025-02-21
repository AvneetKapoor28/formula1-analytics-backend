import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting
import io
from fastapi import Response

# Load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

def generate_position_changes_plot(year: int, round_no: int, session_type: str):
    try:
        # Load the race session
        session = fastf1.get_session(year, int(round_no), session_type)
        session.load(telemetry=False, weather=False)

        # Create figure
        fig, ax = plt.subplots(figsize=(8.0, 4.9))

        # Loop through each driver and plot their position over laps
        for drv in session.drivers:
            drv_laps = session.laps.pick_driver(drv)
            if drv_laps.empty:
                continue  # Skip drivers with no lap data

            abb = drv_laps['Driver'].iloc[0]
            style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)

            ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)

        # Formatting
        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Position')

        # Add legend outside the plot
        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.tight_layout()

        # Save figure to an in-memory file
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
        plt.close(fig)  # Free memory
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}
