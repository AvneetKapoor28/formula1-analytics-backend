from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import io
from fastapi import Response

def generate_tyre_strategy_plot(year: int, round_no: str, session_type: str):
    try:
        # Load the race session
        session = fastf1.get_session(year, int(round_no), session_type)
        session.load()
        laps = session.laps

        # Get driver abbreviations
        drivers = [session.get_driver(driver)["Abbreviation"] for driver in session.drivers]

        # Group laps by driver, stint, and compound to count stint length
        stints = laps[["Driver", "Stint", "Compound", "LapNumber"]].groupby(["Driver", "Stint", "Compound"])
        stints = stints.count().reset_index().rename(columns={"LapNumber": "StintLength"})

        # Create figure
        fig, ax = plt.subplots(figsize=(5, 10))

        for driver in drivers:
            driver_stints = stints.loc[stints["Driver"] == driver]

            previous_stint_end = 0
            for _, row in driver_stints.iterrows():
                # Get compound color
                compound_color = fastf1.plotting.get_compound_color(row["Compound"], session=session)
                plt.barh(
                    y=driver,
                    width=row["StintLength"],
                    left=previous_stint_end,
                    color=compound_color,
                    edgecolor="black",
                    fill=True
                )
                previous_stint_end += row["StintLength"]

        # Formatting the plot
        plt.title(f"{year} {session.event['EventName']} Tyre Strategies")
        plt.xlabel("Lap Number")
        plt.grid(False)
        ax.invert_yaxis()  # Invert y-axis so higher finishers are on top

        # Aesthetics
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.tight_layout()

        # Save figure to an in-memory file
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=300)
        plt.close(fig)  # Free memory
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}
