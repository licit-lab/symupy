import matplotlib.pyplot as plt
import numpy as np


def render_trip(fig, trip):
    distances = [0]
    times = list()
    for ind, s in enumerate(trip.states):
        times.append(s.time.to_hhmmss())
        if ind > 0:
            dist = np.linalg.norm(
                trip.states[ind].absolute_position
                - trip.states[ind - 1].absolute_position
            )
            prev_dist = distances[-1]
            distances.append(dist + prev_dist)

    fig.gca().plot(times, distances)
    plt.xticks(rotation=75)
    fig.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
    plt.ylabel("distance travelled")
    plt.grid()
    plt.title(f"Trip id:{trip.vehicle}")
    plt.tight_layout()


if __name__ == "__main__":
    from symupy.plugins.reader.symuflow import SymuFlowTrafficDataReader

    # file = os.path.dirname(symupy.__file__)+'/../tests/mocks/bottlenecks/bottleneck_001.xml'
    # file = "/Users/florian/Work/visunet/data/Lyon63V/OUT5_less/defaultOut_063000_073000_traf.xml"
    # reader = SymuFlowTrafficDataReader(file)
    # t = reader.get_trip('23')
