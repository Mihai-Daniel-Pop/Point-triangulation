import numpy as np
import time  # Import time module
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

class PointLocationStructure:
    def __init__(self, points):
        start_time = time.time()  # Start timing
        self.points = points
        self.triangulation = Delaunay(points)
        self.triangulation_time = time.time() - start_time  # Calculate elapsed time

    def locate_point(self, query_point):
        simplex = self.triangulation.find_simplex(query_point)
        if simplex == -1:
            return None
        return self.triangulation.simplices[simplex]

def generate_random_points(n, space):
    return np.random.rand(n, 2) * space

def generate_query_point_inside(points):
    weights = np.random.rand(len(points))
    weights /= weights.sum()
    return np.dot(weights, points)

def on_scroll(event):
    """ Zoom in and out with the scroll wheel """
    scale_factor = 1.2 if event.step > 0 else 0.8  # Zoom in or out
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()

    new_xlim = [event.xdata + (x - event.xdata) * scale_factor for x in xlim]
    new_ylim = [event.ydata + (y - event.ydata) * scale_factor for y in ylim]

    plt.gca().set_xlim(new_xlim)
    plt.gca().set_ylim(new_ylim)
    plt.draw()  # Redraw the plot

if __name__ == "__main__":
    num_points = int(input("Enter the number of points to generate: "))
    space = 10

    points = generate_random_points(num_points, space)
    query_point = generate_query_point_inside(points)

    pls = PointLocationStructure(points)

    print(f"Time taken to generate Delaunay triangulation: {pls.triangulation_time:.6f} seconds")

    result = pls.locate_point(query_point)

    plt.figure(figsize=(10, 10))
    plt.triplot(points[:, 0], points[:, 1], pls.triangulation.simplices, color="blue", alpha=0.5)
    plt.scatter(points[:, 0], points[:, 1], color="black", s=1, label="Points")  # Smaller marker size
    plt.scatter(query_point[0], query_point[1], color="red", s=50, label="Query Point")

    if result is not None:
        triangle = points[result]
        plt.fill(triangle[:, 0], triangle[:, 1], color="green", alpha=0.3, label="Located Triangle")
        print("Query point lies in triangle with vertices:", triangle)
    else:
        print("Query point is outside the triangulation.")

    plt.legend()
    plt.gcf().canvas.mpl_connect("scroll_event", on_scroll)  # Bind scroll wheel event
    plt.show()
