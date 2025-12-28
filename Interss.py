import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

SAFE_DISTANCE = 1.5

class TrafficLight:
    def __init__(self, green_time_ns=60, green_time_ew=60):
        self.green_time_ns = green_time_ns
        self.green_time_ew = green_time_ew
        self.timer = 0
        self.state = "NS"

    def step(self):
        self.timer += 1
        if self.state == "NS" and self.timer >= self.green_time_ns:
            self.state = "EW"
            self.timer = 0
        elif self.state == "EW" and self.timer >= self.green_time_ew:
            self.state = "NS"
            self.timer = 0

    def is_green(self, direction):
        return (direction in ["N", "S"] and self.state == "NS") or \
               (direction in ["E", "W"] and self.state == "EW")


class Car:
    speed = 0.5
    lane_offset = 1.2

    def __init__(self, direction, lane):
        self.direction = direction
        self.lane = lane
        self.has_crossed = False
        self.counted = False

        offset = (lane + 0.5) * self.lane_offset

        if direction == "N":
            self.x, self.y = +offset, 22
        elif direction == "S":
            self.x, self.y = -offset, -22
        elif direction == "E":
            self.x, self.y = 22, -offset
        elif direction == "W":
            self.x, self.y = -22, +offset

    def check_crossing(self):
        if self.direction in ["N", "S"]:
            if (self.direction == "N" and self.y <= 0) or \
               (self.direction == "S" and self.y >= 0):
                self.has_crossed = True
        else:
            if (self.direction == "E" and self.x <= 0) or \
               (self.direction == "W" and self.x >= 0):
                self.has_crossed = True

    def distance_to(self, other):
        if self.direction == "N":
            return self.y - other.y
        if self.direction == "S":
            return other.y - self.y
        if self.direction == "E":
            return self.x - other.x
        if self.direction == "W":
            return other.x - self.x

    def move_forward(self):
        if self.direction == "N":
            self.y -= self.speed
        elif self.direction == "S":
            self.y += self.speed
        elif self.direction == "E":
            self.x -= self.speed
        elif self.direction == "W":
            self.x += self.speed

    def step(self, light, cars):
        if not self.has_crossed:
            self.check_crossing()

        cars_ahead = [
            c for c in cars
            if c is not self
            and c.direction == self.direction
            and c.lane == self.lane
            and self.distance_to(c) > 0
        ]

        if cars_ahead:
            nearest = min(cars_ahead, key=lambda c: self.distance_to(c))
            if self.distance_to(nearest) < SAFE_DISTANCE:
                return 

        stop_dist = 2

        if self.has_crossed:
            self.move_forward()
            return

        if self.direction == "N":
            if self.y > stop_dist or light.is_green("N"):
                self.move_forward()
        elif self.direction == "S":
            if self.y < -stop_dist or light.is_green("S"):
                self.move_forward()
        elif self.direction == "E":
            if self.x > stop_dist or light.is_green("E"):
                self.move_forward()
        elif self.direction == "W":
            if self.x < -stop_dist or light.is_green("W"):
                self.move_forward()

class IntersectionEnv:
    def __init__(self, spawn_rate=0.08):
        self.light = TrafficLight()
        self.cars = []
        self.spawn_rate = spawn_rate
        self.flow = 0

    def spawn_car(self):
        if np.random.rand() < self.spawn_rate:
            direction = np.random.choice(["N", "S", "E", "W"])
            lane = np.random.choice([0, 1])
            self.cars.append(Car(direction, lane))

    def step(self):
        self.light.step()
        self.spawn_car()

        for car in self.cars:
            car.step(self.light, self.cars)
            if car.has_crossed and not car.counted:
                self.flow += 1
                car.counted = True

        self.cars = [c for c in self.cars if abs(c.x) < 25 and abs(c.y) < 25]

def render(env, ax):
    ax.clear()

    ax.add_patch(plt.Rectangle((-3, -25), 6, 50, color="#444"))
    ax.add_patch(plt.Rectangle((-25, -3), 50, 6, color="#444"))

    for o in [-1.2, 1.2]:
        ax.plot([o, o], [-25, 25], "w--", linewidth=1)
        ax.plot([-25, 25], [o, o], "w--", linewidth=1)

    ax.scatter(0, 4, c="green" if env.light.state == "NS" else "red", s=150)
    ax.scatter(4, 0, c="green" if env.light.state == "EW" else "red", s=150)

    for car in env.cars:
        ax.scatter(car.x, car.y, c="cyan", s=35)

    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Tráfico en Intersección | Flujo: {env.flow}")
plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))

env = IntersectionEnv()

while True:
    env.step()
    render(env, ax)
    plt.pause(0.03)
