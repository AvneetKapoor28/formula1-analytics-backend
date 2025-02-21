import fastf1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # to prevent NSException 
import io
from matplotlib import colormaps
from matplotlib.collections import LineCollection
from fastapi import Response

def generate_gear_shift_plot(year: int, round_no: str, session_type: str):
   try:
        round_no = int(round_no)
        # Load session data
        session = fastf1.get_session(year, round_no, session_type)
        session.load()

        # Get fastest lap telemetry
        lap = session.laps.pick_fastest()
        tel = lap.get_telemetry()

        x = np.array(tel['X'].values)
        y = np.array(tel['Y'].values)

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        gear = tel['nGear'].to_numpy().astype(float)

        # Create line collection
        cmap = colormaps['Paired']
        lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
        lc_comp.set_array(gear)
        lc_comp.set_linewidth(4)

        # Create plot
        fig, ax = plt.subplots()
        ax.add_collection(lc_comp)
        ax.axis('equal')
        ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

        plt.suptitle(
            f"Fastest Lap Gear Shift Visualization\n"
            f"{lap['Driver']} - {session.event['EventName']} {session.event.year}"
        )

        cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
        cbar.set_ticks(np.arange(1.5, 9.5))
        cbar.set_ticklabels(np.arange(1, 9))

        # Save figure to an in-memory file
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png", bbox_inches="tight")
        plt.close(fig)  # Free memory
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")
   
   except Exception as e:
    return {"error": str(e)}
    


