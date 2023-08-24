import threading

from My2D import rotatePoly, movePoly, degToRad

# the polygon and associated kinematics for the turn coordinator graphic
class Coordinator:
    def __init__(self, x, y, theta):
        self.lock = threading.Lock()

        self.id = 0
        self._cx = x
        self._cy = y
        self._polygon = [
                (0, 20), (-300, 7), (-300, 0),
                (-3, 0), (-3, -25), (-50, -25), (-50, -30), (-3, -30), (-3, -80),
                (3, -80), (3, -30), (50, -30), (50, -25), (3, -25), (3, 0),
                (300, 0), (300, 7)
                ]
        self._theta = theta

    def roll(self, dTheta):
        with self.lock:
            self._theta += dTheta

    @property
    def theta(self):
        with self.lock:
            return self._theta

    @theta.setter
    def theta(self, value):
        with self.lock:
            self._theta = value

    @property
    def points(self):
        primes = []
        for px, py in self._polygon:
            primes += [px, py]

        rotatePoly(primes, self.theta)
        movePoly(primes, self._cx, self._cy)

        return primes
