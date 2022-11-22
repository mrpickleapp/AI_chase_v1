import net

class AI():

    def __init__(self):
        self.network = net.Network()
        self.network.add(net.FCLayer(6, 6))
        self.network.add(net.ActivationLayer(net.tanh, net.tanh_prime))
        self.network.add(net.FCLayer(6, 6))
        self.network.add(net.ActivationLayer(net.tanh, net.tanh_prime))
        self.network.add(net.FCLayer(6, 2))
        self.network.add(net.ActivationLayer(net.tanh, net.tanh_prime))

    def compute(self, input):
        out = self.network.predict(input)
        return out

    def evolve(self, evolution_rate):
        self.network.evolve(evolution_rate=evolution_rate)