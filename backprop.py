from manim import *
import numpy as np
import random


class BackpropExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Backpropagation", font_size=48)
        subtitle = Text("The Mathematics Behind Neural Network Learning", font_size=28)
        subtitle.next_to(title, DOWN)
        header = VGroup(title, subtitle)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait()
        self.play(header.animate.scale(0.6).to_edge(UP))
        
        # Overview of sections
        sections = ["Neural Network Architecture", "Forward Pass", "Loss Computation", "Backward Pass"]
        section_boxes = VGroup(*[
            VGroup(
                Rectangle(width=3, height=0.8, fill_opacity=0.3, fill_color=BLUE),
                Text(section, font_size=20)
            ).arrange(ORIGIN)
            for section in sections
        ]).arrange(DOWN, buff=0.3)
        
        self.play(Create(section_boxes))
        self.wait()
        self.play(FadeOut(section_boxes))
        
        # Show each section
        self.show_network_architecture()
        self.show_forward_pass()
        self.show_loss_computation()
        self.show_backward_pass()
        
        # Conclusion
        conclusion = Text("Backpropagation: The Foundation of Deep Learning", font_size=40)
        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion))

    def create_network(self, layer_sizes=[3, 4, 4, 2], spacing=2.5):
        """Create a neural network visualization with the given layer sizes."""
        layers = []
        edges = []
        edge_groups = []
        
        # Create layers
        for i, size in enumerate(layer_sizes):
            layer = VGroup(*[
                Circle(radius=0.25, fill_opacity=0.8, fill_color=BLUE if i < len(layer_sizes)-1 else GREEN)
                for _ in range(size)
            ]).arrange(DOWN, buff=0.4)
            
            # Add layer label
            if i == 0:
                label = Text("Input Layer", font_size=20)
            elif i == len(layer_sizes) - 1:
                label = Text("Output Layer", font_size=20)
            else:
                label = Text(f"Hidden Layer {i}", font_size=20)
            
            label.next_to(layer, DOWN, buff=0.5)
            layer = VGroup(layer, label)
            
            # Position layer
            if i > 0:
                layer.shift(RIGHT * spacing * i)
            
            layers.append(layer)
            
            # Create edges between this layer and the previous one
            if i > 0:
                prev_neurons = layers[i-1][0]
                curr_neurons = layer[0]
                
                layer_edges = []
                for prev_neuron in prev_neurons:
                    for curr_neuron in curr_neurons:
                        edge = Line(
                            prev_neuron.get_right(),
                            curr_neuron.get_left(),
                            stroke_opacity=0.6,
                            stroke_width=1
                        )
                        edges.append(edge)
                        layer_edges.append(edge)
                
                edge_groups.append(VGroup(*layer_edges))
        
        network = VGroup(*layers)
        all_edges = VGroup(*edges)
        
        return network, all_edges, edge_groups

    def show_network_architecture(self):
        # Title
        title = Text("Neural Network Architecture", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Create neural network
        network, edges, edge_groups = self.create_network(layer_sizes=[3, 5, 4, 2])
        
        # Group network components
        nn_group = VGroup(network, edges)
        nn_group.scale(0.9).center()
        
        # Add formula for neuron computation
        formula_text = MathTex(
            "z_j^{(l)} = \\sum_i w_{ji}^{(l)} a_i^{(l-1)} + b_j^{(l)}"
        ).scale(0.8)
        
        activation_text = MathTex(
            "a_j^{(l)} = \\sigma(z_j^{(l)})"
        ).scale(0.8)
        
        formulas = VGroup(formula_text, activation_text).arrange(DOWN, buff=0.3)
        formulas.next_to(nn_group, DOWN, buff=0.7)
        
        # Animate
        self.play(Write(title))
        self.play(
            *[Create(layer) for layer in network],
            run_time=2
        )
        
        self.play(
            *[Create(edge_group) for edge_group in edge_groups],
            run_time=2
        )
        
        # Highlight neuron activation path
        selected_neuron = network[2][0][1]  # Select a neuron in the second hidden layer
        self.play(
            selected_neuron.animate.set_fill(YELLOW),
            run_time=0.5
        )
        
        # Show incoming connections
        incoming_edges = []
        for edge in edge_groups[1]:
            if edge.get_end() == selected_neuron.get_left():
                incoming_edges.append(edge)
        
        self.play(
            *[edge.animate.set_stroke(YELLOW, width=3) for edge in incoming_edges],
            run_time=1
        )
        
        # Show weighted sum formula
        self.play(Write(formula_text))
        self.wait()
        
        # Show activation function
        activation_curve = FunctionGraph(
            lambda x: 1 / (1 + np.exp(-x)),
            x_range=[-5, 5, 0.01],
            color=YELLOW
        ).scale(0.3)
        
        activation_curve.next_to(selected_neuron, UP, buff=0.5)
        activation_label = Text("σ(x)", font_size=16).next_to(activation_curve, UP, buff=0.1)
        
        self.play(
            Create(activation_curve),
            Write(activation_label)
        )
        self.play(Write(activation_text))
        
        # Reset colors for next section
        self.play(
            selected_neuron.animate.set_fill(BLUE),
            *[edge.animate.set_stroke(WHITE, width=1, opacity=0.6) for edge in incoming_edges],
            FadeOut(activation_curve),
            FadeOut(activation_label)
        )
        
        # Include description
        explanation = Text(
            "Neural networks consist of layers of neurons connected by weighted edges",
            font_size=16
        )
        explanation.next_to(formulas, DOWN, buff=0.5)
        explanation.width = config.frame_width - 1
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Save network for next sections
        self.network = network
        self.edges = edges
        self.edge_groups = edge_groups
        
        # Clear screen for next section
        self.play(
            FadeOut(title),
            FadeOut(explanation),
            FadeOut(formulas)
        )

    def show_forward_pass(self):
        # Title
        title = Text("Forward Pass", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Use the network from the previous section
        network = self.network
        edges = self.edges
        edge_groups = self.edge_groups
        
        # Create data flow
        input_data = MathTex("\\mathbf{x} = [0.2, 0.7, -0.1]").scale(0.8)
        input_data.next_to(network[0], LEFT, buff=1)
        
        # Animate
        self.play(Write(title))
        self.play(Write(input_data))
        
        # Activate input layer neurons
        input_neurons = network[0][0]
        self.play(
            *[neuron.animate.set_fill(YELLOW) for neuron in input_neurons],
            run_time=1
        )
        
        # Propagate through layers with cascading activation
        for i in range(1, len(network)):
            # Light up the edges from previous layer
            self.play(
                *[edge.animate.set_stroke(YELLOW, width=2, opacity=1) 
                  for edge in edge_groups[i-1]],
                run_time=1
            )
            
            # Activate the current layer
            current_neurons = network[i][0]
            self.play(
                *[neuron.animate.set_fill(YELLOW) for neuron in current_neurons],
                run_time=1
            )
            
            # Create computation visualization for first neuron in layer
            if i < len(network) - 1:  # Not for the output layer
                weighted_sum = MathTex("\\sum w_{ji} a_i + b_j").scale(0.7)
                weighted_sum.next_to(current_neurons[0], UP, buff=0.4)
                
                activation = MathTex("\\sigma(z_j)").scale(0.7)
                activation.next_to(weighted_sum, UP, buff=0.2)
                
                self.play(Write(weighted_sum))
                self.play(Write(activation))
                
                self.play(
                    FadeOut(weighted_sum),
                    FadeOut(activation)
                )
        
        # Show predicted output
        output_value = MathTex("\\hat{y} = [0.85, 0.23]").scale(0.8)
        output_value.next_to(network[-1], RIGHT, buff=1)
        
        self.play(Write(output_value))
        
        # Add explanation
        explanation = Text(
            "Forward pass: Data flows through the network, with each neuron computing a weighted sum followed by activation",
            font_size=16
        )
        explanation.next_to(network, DOWN, buff=1)
        explanation.width = config.frame_width - 1
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Reset colors for next section but keep network visible
        self.play(
            *[neuron.animate.set_fill(BLUE) for group in network for neuron in group[0] if isinstance(neuron, Circle) and neuron.get_fill_color() != GREEN],
            *[neuron.animate.set_fill(GREEN) for neuron in network[-1][0]],
            *[edge.animate.set_stroke(WHITE, width=1, opacity=0.6) for edge in edges]
        )
        
        # Clear additional elements
        self.play(
            FadeOut(title),
            FadeOut(input_data),
            FadeOut(output_value),
            FadeOut(explanation)
        )

    def show_loss_computation(self):
        # Title
        title = Text("Loss Computation", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Network from previous sections
        network = self.network
        
        # Create actual vs predicted
        predicted = MathTex("\\hat{y} = [0.85, 0.23]").scale(0.8)
        actual = MathTex("y = [1, 0]").scale(0.8)
        
        prediction_group = VGroup(predicted, actual).arrange(DOWN, buff=0.3)
        prediction_group.next_to(network[-1], RIGHT, buff=1)
        
        # Loss function
        loss_formula = MathTex(
            "L(\\hat{y}, y) = \\frac{1}{2} \\sum_j (\\hat{y}_j - y_j)^2"
        ).scale(0.8)
        
        loss_value = MathTex(
            "L = \\frac{1}{2}[(0.85 - 1)^2 + (0.23 - 0)^2] = 0.03"
        ).scale(0.8)
        
        loss_group = VGroup(loss_formula, loss_value).arrange(DOWN, buff=0.3)
        loss_group.next_to(prediction_group, DOWN, buff=0.7)
        
        # Error visualization
        error_arrows = []
        for i, neuron in enumerate(network[-1][0]):
            # Create error indicator
            error_value = 0.15 if i == 0 else 0.23  # Example error values
            error_text = MathTex(f"e_{i} = {error_value}").scale(0.7)
            error_text.next_to(neuron, UP, buff=0.4)
            error_arrows.append(error_text)
        
        error_group = VGroup(*error_arrows)
        
        # Animate
        self.play(Write(title))
        self.play(Write(prediction_group))
        
        # Show error on output neurons
        output_neurons = network[-1][0]
        self.play(
            *[neuron.animate.set_fill(RED_E if i == 0 else YELLOW) for i, neuron in enumerate(output_neurons)],
            Write(error_group),
            run_time=1.5
        )
        
        # Show loss computation
        self.play(Write(loss_formula))
        self.play(Write(loss_value))
        
        # Add explanation
        explanation = Text(
            "Loss function measures the difference between predicted and actual outputs",
            font_size=16
        )
        explanation.next_to(loss_group, DOWN, buff=0.5)
        explanation.width = config.frame_width - 1
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Clear screen for next section but keep network
        self.play(
            FadeOut(title),
            FadeOut(prediction_group),
            FadeOut(error_group),
            FadeOut(loss_group),
            FadeOut(explanation)
        )

    def show_backward_pass(self):
        # Title
        title = Text("Backward Pass (Backpropagation)", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Network from previous sections
        network = self.network
        edges = self.edges
        edge_groups = self.edge_groups
        
        # Mathematical formulation
        gradient_formula = MathTex(
            "\\frac{\\partial L}{\\partial w_{ji}^{(l)}} = \\delta_j^{(l)} a_i^{(l-1)}"
        ).scale(0.8)
        
        delta_formula = MathTex(
            "\\delta_j^{(l)} = \\delta_j^{(l+1)} w_{kj}^{(l+1)} \\sigma'(z_j^{(l)})"
        ).scale(0.8)
        
        formulas = VGroup(gradient_formula, delta_formula).arrange(DOWN, buff=0.3)
        formulas.next_to(network, DOWN, buff=0.7)
        
        # Animate
        self.play(Write(title))
        self.play(Write(formulas))
        
        # Start with error at output layer
        output_neurons = network[-1][0]
        self.play(
            *[neuron.animate.set_fill(RED) for neuron in output_neurons],
            run_time=1
        )
        
        # Propagate error backwards through the network
        for i in range(len(network)-1, 0, -1):
            # Light up the edges to previous layer in red (gradient flow)
            self.play(
                *[edge.animate.set_stroke(RED, width=2, opacity=1) 
                  for edge in edge_groups[i-1]],
                run_time=1
            )
            
            # Propagate error to previous layer
            prev_neurons = network[i-1][0]
            self.play(
                *[neuron.animate.set_fill(RED) for neuron in prev_neurons],
                run_time=1
            )
            
            # Show delta computation for first neuron
            if i > 1:  # Not for the input layer
                delta_computation = MathTex(
                    "\\delta_j^{(" + str(i-1) + ")} = \\sum_k \\delta_k^{(" + str(i) + ")} w_{kj} \\sigma'(z_j)"
                ).scale(0.7)
                delta_computation.next_to(prev_neurons[0], UP, buff=0.4)
                
                self.play(Write(delta_computation))
                self.wait(0.5)
                self.play(FadeOut(delta_computation))
        
        # Weight update visualization
        self.play(
            *[edge.animate.set_stroke(YELLOW, width=2, opacity=0.8) for edge in edges],
            run_time=1
        )
        
        weight_update = MathTex(
            "w_{ji}^{new} = w_{ji}^{old} - \\alpha \\frac{\\partial L}{\\partial w_{ji}}"
        ).scale(0.8)
        weight_update.next_to(formulas, DOWN, buff=0.5)
        
        self.play(Write(weight_update))
        
        # Add explanation
        explanation = Text(
            "Backpropagation: Error gradients flow backward through the network to update weights",
            font_size=16
        )
        explanation.next_to(weight_update, DOWN, buff=0.5)
        explanation.width = config.frame_width - 1
        
        self.play(Write(explanation))
        
        # Gradient descent visualization
        loss_surface = Surface(
            lambda u, v: np.array([u, v, 0.5*u**2 + 0.3*v**2]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            fill_opacity=0.5
        ).scale(0.5)
        
        loss_surface.shift(RIGHT * 5 + UP * 0.5)
        
        # Add point showing gradient descent
        point = Sphere(radius=0.1, fill_color=RED)
        point.move_to(loss_surface.get_point_from_function(1.5, 1.2))
        
        path = VMobject()
        path.set_points_as_corners([
            loss_surface.get_point_from_function(1.5, 1.2),
            loss_surface.get_point_from_function(1.2, 1.0),
            loss_surface.get_point_from_function(0.9, 0.8),
            loss_surface.get_point_from_function(0.6, 0.5),
            loss_surface.get_point_from_function(0.3, 0.3),
            loss_surface.get_point_from_function(0.1, 0.1),
        ])
        
        path.set_stroke(YELLOW, 4)
        
        gd_label = Text("Gradient Descent", font_size=16)
        gd_label.next_to(loss_surface, DOWN)
        
        self.play(
            Create(loss_surface),
            Create(point),
            Write(gd_label)
        )
        
        self.play(
            MoveAlongPath(point, path),
            Create(path),
            run_time=3
        )
        
        self.wait(2)
        
        # Final cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]]) 