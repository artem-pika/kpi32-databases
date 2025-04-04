class Wind:

    def __init__(self, kph, mph, degree, direction):
        self.mph = mph
        self.kph = kph
        self.degree = degree
        self.direction = direction
    
    def go_outside(self):
        return self.kph <= 19