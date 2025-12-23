import scipy.integrate as spi
import random
import matplotlib.pyplot as plt
import numpy as np


def create_plot(func, x_min, x_max, inside_points, outside_points):
    # Створення діапазону значень для x
    x = np.linspace(x_min-0.5, x_max+0.5, 400)
    y = func(x)

    # Створення графіка
    fig, ax = plt.subplots()

    # Малювання функції
    ax.plot(x, y, 'r', linewidth=2)

    # Заповнення області під кривою
    ix = np.linspace(x_min, x_max)
    iy = func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3)

    ax.scatter([point[0] for point in inside_points], [point[1] for point in inside_points], c='green', s=1)
    ax.scatter([point[0] for point in outside_points], [point[1] for point in outside_points], c='red', s=1)


    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    # Додавання меж інтегрування та назви графіка
    ax.axvline(x=x_min, color='gray', linestyle='--')
    ax.axvline(x=x_max, color='gray', linestyle='--')
    ax.set_title('Integral plot from ' + str(x_min) + ' to ' + str(x_max))
    plt.grid()
    plt.show()


def square_func(x, theor=False):
    if theor:
        return x**3/3
    return x**2

def quad_func(x, theor=False):
    if theor:
        return x**4/4
    return x**3

def is_inside(x, y, func):
    """Checks if the point (x, y) is inside the figure."""
    return y <= func(x)

def monte_carlo_simulation(a, b, num_experiments, func):
    """Performs a series of experiments using the Monte Carlo method."""
    average_area = 0
    global_inside_points = []
    global_outside_points = []
    for _ in range(num_experiments):
        # Random point generation
        points = [(random.uniform(0, a), random.uniform(0, b)) for _ in range(15000)]
        # Point selection
        inside_points = []
        outside_points = []
        for point in points:
            if is_inside(point[0], point[1], func):
                inside_points.append(point)
            else:
                outside_points.append(point)

        # Monte Carlo area calculation
        M = len(inside_points)
        N = len(points)
        area = M/N*(a*b)
        average_area += area
        
        global_inside_points.extend(inside_points)
        global_outside_points.extend(outside_points)

    average_area /= num_experiments
    return average_area, global_inside_points, global_outside_points

def main(func, x_min, x_max, num_experiments):
    
    # Calculation of the integral
    result, error = spi.quad(func, x_min, x_max)

    print(f"Scipy Integral: {result}, error: {error}")

    teoretical_square = func(x_max, theor=True)
    y_max = func(x_max)

    average_area, ip, op = monte_carlo_simulation(x_max, y_max, num_experiments, func)
    print(f"Theoretical square: {teoretical_square}")
    print(f"Monte Carlo average square of the figure after {num_experiments} experiments: {average_area}")
    print(f"Monte Carlo error comparing with SciPy: {(result-average_area)/result:.2%}")

    create_plot(func, x_min, x_max, ip, op)

if __name__ == "__main__":
    x_min = 3
    x_max = 10
    
    for exp_n in [1, 10, 100, 1000]:
        print(f"NUMBER OF EXPERIMENTS: {exp_n}")
        main(quad_func, x_min, x_max, exp_n)
        print()
