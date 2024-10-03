import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np

class VisualizationUtils:
    def __init__(self, max_nodes):
        self.max_nodes = max_nodes
        self.events = []
        self.node_positions = {}
        self.G = nx.Graph()
        self.node_health = {}

    def log_event(self, time, event_type, data):
        self.events.append((time, event_type, data))

    def generate_node_positions(self):
        for i in range(self.max_nodes):
            angle = 2 * np.pi * i / self.max_nodes
            self.node_positions[i] = (np.cos(angle), np.sin(angle))

    def create_animation(self, output_file='aging_simulation.mp4', fps=30, duration=60):
        self.generate_node_positions()
        fig, ax = plt.subplots(figsize=(10, 10))
        
        def update(frame):
            ax.clear()
            current_time = frame / fps
            relevant_events = [e for e in self.events if e[0] <= current_time]
            
            self.G.clear()
            self.node_health.clear()
            
            for _, event_type, data in relevant_events:
                if event_type == 'add_node':
                    self.G.add_node(data)
                    self.node_health[data] = 1.0  # Initialize with full health
                elif event_type == 'add_edge':
                    self.G.add_edge(*data)
                elif event_type == 'update_health':
                    node_id, health = data
                    if node_id in self.G.nodes:
                        self.node_health[node_id] = health

            node_colors = [plt.cm.RdYlGn(self.node_health[node]) for node in self.G.nodes()]
            node_sizes = [300 * self.node_health[node] + 100 for node in self.G.nodes()]
            
            pos = {node: self.node_positions[node] for node in self.G.nodes()}
            nx.draw(self.G, pos, ax=ax, node_color=node_colors, node_size=node_sizes, with_labels=True)
            ax.set_title(f"Time: {current_time:.2f}")

        total_frames = int(fps * duration)
        anim = animation.FuncAnimation(fig, update, frames=total_frames, interval=1000/fps, repeat=False)
        anim.save(output_file, writer='ffmpeg', fps=fps)
        plt.close(fig)

    def plot_system_health(self, times, health_values, resilience_values, output_file='system_health.png'):
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        ax1.set_xlabel('Time')
        ax1.set_ylabel('System Health', color='tab:blue')
        ax1.plot(times, health_values, color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('Resilience', color='tab:orange')
        ax2.plot(times, resilience_values, color='tab:orange')
        ax2.tick_params(axis='y', labelcolor='tab:orange')
        
        plt.title('System Health and Resilience Over Time')
        fig.tight_layout()
        plt.savefig(output_file)
        plt.close(fig)

# Example usage remains the same as before
# Example usage
vis_utils = VisualizationUtils(max_nodes=100)

# In your simulation loop:
# vis_utils.log_event(time, 'add_node', node_id)
# vis_utils.log_event(time, 'add_edge', (node1_id, node2_id))
# vis_utils.log_event(time, 'update_health', (node_id, health))

# After simulation:
# vis_utils.create_animation()
# vis_utils.plot_system_health(times, health_values, resilience_values)