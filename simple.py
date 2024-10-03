import random
from viz_utils import VisualizationUtils

class Node:
    def __init__(self, id):
        self.id = id
        self.connections = set()
        self.health = 1.0  # 1.0 is perfect health

    def connect(self, other_node):
        self.connections.add(other_node)
        other_node.connections.add(self)

class AgingSystem:
    def __init__(self, initial_nodes=3, max_nodes=100):
        self.nodes = [Node(i) for i in range(initial_nodes)]
        self.max_nodes = max_nodes
        self.time = 0
        self.growth_rate = 0.2
        self.aging_rate = 0.001
        self.resilience = 1.0
        self.vis_utils = VisualizationUtils(max_nodes)
        
        # Log initial state
        for node in self.nodes:
            self.vis_utils.log_event(self.time, 'add_node', node.id)
            self.vis_utils.log_event(self.time, 'update_health', (node.id, node.health))

    def step(self):
        self.time += 1
        
        # Growth phase
        if len(self.nodes) < self.max_nodes:
            if random.random() < self.growth_rate:
                new_node = Node(len(self.nodes))
                self.nodes.append(new_node)
                self.vis_utils.log_event(self.time, 'add_node', new_node.id)
                self.vis_utils.log_event(self.time, 'update_health', (new_node.id, new_node.health))
                # Connect to random existing nodes
                for node in random.sample(self.nodes[:-1], min(3, len(self.nodes) - 1)):
                    new_node.connect(node)
                    self.vis_utils.log_event(self.time, 'add_edge', (new_node.id, node.id))

        # Aging phase
        self.resilience -= self.aging_rate
        for node in self.nodes:
            node.health -= random.uniform(0, self.aging_rate * 2)
            node.health = max(0, node.health)  # Ensure health doesn't go negative
            self.vis_utils.log_event(self.time, 'update_health', (node.id, node.health))

        # Attempt repair based on resilience
        for node in self.nodes:
            if random.random() < self.resilience:
                node.health = min(1.0, node.health + 0.01)
                self.vis_utils.log_event(self.time, 'update_health', (node.id, node.health))

    def system_health(self):
        return sum(node.health for node in self.nodes) / len(self.nodes)

    def run_simulation(self, steps):
        health_values = []
        resilience_values = []
        times = []

        for _ in range(steps):
            self.step()
            health_values.append(self.system_health())
            resilience_values.append(self.resilience)
            times.append(self.time)
            # print progress every 100 steps
            if self.time % 100 == 0:
                print(f"Time: {self.time}, System health: {health_values[-1]:.2f}, Resilience: {resilience_values[-1]:.2f}")

        self.vis_utils.create_animation()
        self.vis_utils.plot_system_health(times, health_values, resilience_values)

# Example usage
system = AgingSystem()
system.run_simulation(5000)