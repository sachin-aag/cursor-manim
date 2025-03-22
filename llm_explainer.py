from manim import *
import numpy as np
import random

class LLMExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Large Language Models (LLMs)", font_size=40)
        subtitle = Text("Understanding How They Work", font_size=28).next_to(title, DOWN)
        header = VGroup(title, subtitle)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait()
        self.play(header.animate.scale(0.6).to_edge(UP))
        
        # Create main components stages
        stages = ["Pre-training", "Fine-tuning", "Inference"]
        stage_boxes = VGroup(*[
            VGroup(
                Rectangle(width=2.5, height=1, fill_opacity=0.3, fill_color=BLUE),
                Text(stage, font_size=24)
            ).arrange(ORIGIN)
            for stage in stages
        ]).arrange(RIGHT, buff=1)
        
        self.play(*[Create(box[0]) for box in stage_boxes])
        self.play(*[Write(box[1]) for box in stage_boxes])
        self.wait()
        self.play(FadeOut(stage_boxes))
        
        # 1. Pre-training Stage
        self.show_pretraining_stage()
        
        # 2. Fine-tuning Stage
        self.show_finetuning_stage()
        
        # 3. Inference Stage
        self.show_inference_stage()
        
        # Final message
        final_message = Text("Understanding LLMs: From Data to Intelligence", font_size=40)
        self.play(Write(final_message))
        self.wait(2)
        self.play(FadeOut(final_message))

    def show_pretraining_stage(self):
        # Pre-training Stage
        pretraining_title = Text("Pre-training Stage", font_size=28, color=BLUE)
        
        # Create data sources
        data_sources = VGroup(*[
            Rectangle(width=1.2, height=0.6, fill_opacity=0.3, fill_color="#556B2F")
            for _ in range(3)
        ]).arrange(DOWN, buff=0.2)
        
        source_labels = VGroup(
            Text("Wikipedia", font_size=16),
            Text("Books", font_size=16),
            Text("Web Data", font_size=16)
        )
        
        for label, source in zip(source_labels, data_sources):
            label.move_to(source)
        
        data_group = VGroup(data_sources, source_labels)
        data_title = Text("Training Data", font_size=20).next_to(data_group, UP)
        data_group = VGroup(data_group, data_title)
        
        # Create model architecture
        model_box = Rectangle(width=2, height=3, fill_opacity=0.2, fill_color="#483D8B")
        model_layers = VGroup(*[
            Rectangle(width=1.5, height=0.3, fill_opacity=0.4, fill_color=BLUE)
            for _ in range(6)
        ]).arrange(DOWN, buff=0.2).move_to(model_box)
        
        layer_labels = VGroup(
            Text("Attention", font_size=12),
            Text("Feed Forward", font_size=12),
            Text("Attention", font_size=12),
            Text("Feed Forward", font_size=12),
            Text("Attention", font_size=12),
            Text("Feed Forward", font_size=12)
        )
        
        for label, layer in zip(layer_labels, model_layers):
            label.move_to(layer).scale(0.8)
        
        model_text = Text("Transformer\nArchitecture", font_size=20).next_to(model_box, UP)
        model_group = VGroup(model_box, model_layers, layer_labels, model_text)
        
        # Create output representation
        output_box = Rectangle(width=1.5, height=2, fill_opacity=0.3, fill_color="#2F4F4F")
        
        # Tokens inside the output box
        embedding_vectors = VGroup(*[
            Line(
                start=ORIGIN,
                end=RIGHT * random.uniform(0.5, 1.0),
                color=YELLOW
            )
            for _ in range(5)
        ]).arrange(DOWN, buff=0.2).move_to(output_box)
        
        output_text = Text("Pre-trained\nWeights", font_size=20).next_to(output_box, UP)
        output_group = VGroup(output_box, embedding_vectors, output_text)
        
        # Arrange components
        components = VGroup(data_group, model_group, output_group).arrange(RIGHT, buff=1.5)
        pretraining_title.next_to(components, UP, buff=0.5)
        
        # Create arrows
        data_to_model = Arrow(data_sources.get_right(), model_box.get_left(), color=WHITE)
        model_to_output = Arrow(model_box.get_right(), output_box.get_left(), color=WHITE)
        
        # Add explanation
        explanation = Text(
            "Pre-training: Model learns language patterns and knowledge from vast amounts of text data through self-supervised learning",
            font_size=16
        ).next_to(components, DOWN, buff=0.5)
        explanation.width = config.frame_width - 1
        
        # Animate
        self.play(Write(pretraining_title))
        self.play(
            Create(data_sources),
            *[Write(label) for label in source_labels],
            Write(data_title)
        )
        self.play(
            Create(model_box),
            *[Create(layer) for layer in model_layers],
            Write(model_text)
        )
        self.wait(0.5)
        self.play(*[Write(label) for label in layer_labels])
        self.play(Create(data_to_model))
        self.play(
            Create(output_box),
            *[Create(line) for line in embedding_vectors],
            Write(output_text)
        )
        self.play(Create(model_to_output))
        self.play(Write(explanation))
        self.wait(2)
        
        # Clear screen for next section
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])

    def show_finetuning_stage(self):
        # Fine-tuning Stage
        finetuning_title = Text("Fine-tuning Stage", font_size=28, color=BLUE)
        
        # Pre-trained model
        pretrained_box = Rectangle(width=1.5, height=2, fill_opacity=0.2, fill_color="#483D8B")
        pretrained_text = Text("Pre-trained\nModel", font_size=20).next_to(pretrained_box, UP)
        pretrained_group = VGroup(pretrained_box, pretrained_text)
        
        # Task-specific data
        task_data = VGroup(*[
            Rectangle(width=1.2, height=0.4, fill_opacity=0.3, fill_color="#8B4513")
            for _ in range(3)
        ]).arrange(DOWN, buff=0.2)
        
        data_labels = VGroup(
            Text("Task Instructions", font_size=14),
            Text("Input/Output Examples", font_size=14),
            Text("Human Feedback", font_size=14)
        )
        
        for label, rect in zip(data_labels, task_data):
            label.move_to(rect).scale(0.8)
        
        task_text = Text("Task-specific\nData", font_size=20).next_to(task_data, UP)
        task_group = VGroup(task_data, data_labels, task_text)
        
        # Fine-tuned model
        finetuned_box = Rectangle(width=1.5, height=2, fill_opacity=0.3, fill_color="#4682B4")
        finetuned_text = Text("Fine-tuned\nModel", font_size=20).next_to(finetuned_box, UP)
        finetuned_group = VGroup(finetuned_box, finetuned_text)
        
        # Arrange components
        components = VGroup(pretrained_group, task_group, finetuned_group).arrange(RIGHT, buff=2)
        finetuning_title.next_to(components, UP, buff=0.5)
        
        # Arrows
        data_to_pretrained = Arrow(task_data.get_left(), pretrained_box.get_right(), color=WHITE).flip()
        pretrained_to_finetuned = Arrow(pretrained_box.get_right(), finetuned_box.get_left(), color=WHITE)
        
        # Add explanation
        explanation = Text(
            "Fine-tuning: Adapting the pre-trained model to specific tasks using labeled examples and feedback",
            font_size=16
        ).next_to(components, DOWN, buff=0.5)
        explanation.width = config.frame_width - 1
        
        # Animate
        self.play(Write(finetuning_title))
        self.play(Create(pretrained_box), Write(pretrained_text))
        self.play(
            Create(task_data),
            *[Write(label) for label in data_labels],
            Write(task_text)
        )
        self.play(Create(data_to_pretrained))
        self.play(Create(finetuned_box), Write(finetuned_text))
        self.play(Create(pretrained_to_finetuned))
        self.play(Write(explanation))
        self.wait(2)
        
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])

    def show_inference_stage(self):
        # Inference Stage
        inference_title = Text("Inference Stage", font_size=28, color=BLUE)
        
        # User query
        query_box = Rectangle(width=2, height=0.6, fill_opacity=0.3, fill_color="#556B2F")
        query_text = Text("User Query", font_size=20)
        query = VGroup(query_box, query_text).arrange(ORIGIN)
        
        # Model component
        model_circle = Circle(radius=1, fill_opacity=0.4, fill_color="#483D8B")
        model_text = Text("LLM", font_size=24)
        model = VGroup(model_circle, model_text).arrange(ORIGIN)
        
        # Example of a prompt being processed
        prompt_box = Rectangle(width=3, height=1, fill_opacity=0.1, color=WHITE)
        prompt_text = Text("What is a transformer model?", font_size=16).move_to(prompt_box)
        prompt = VGroup(prompt_box, prompt_text)
        
        # Generated response
        response_box = Rectangle(width=3, height=2, fill_opacity=0.2, fill_color="#2F4F4F")
        response_text = Text("A transformer model is\na neural network...", font_size=16).move_to(response_box)
        response = VGroup(response_box, response_text)
        
        # Arrange horizontally
        top_row = VGroup(query, model).arrange(RIGHT, buff=2)
        bottom_row = VGroup(prompt, response).arrange(RIGHT, buff=2)
        components = VGroup(top_row, bottom_row).arrange(DOWN, buff=2)
        
        inference_title.next_to(components, UP, buff=0.5)
        
        # Arrows
        query_to_model = Arrow(query_box.get_right(), model_circle.get_left(), color=WHITE)
        model_to_prompt = Arrow(model_circle.get_bottom(), prompt_box.get_top(), color=WHITE)
        prompt_to_response = Arrow(prompt_box.get_right(), response_box.get_left(), color=WHITE)
        
        # Add explanation
        explanation = Text(
            "Inference: Processing user queries and generating responses based on learned patterns",
            font_size=16
        ).next_to(components, DOWN, buff=0.5)
        
        # Animate
        self.play(Write(inference_title))
        self.play(Create(query_box), Write(query_text))
        self.play(Create(model_circle), Write(model_text))
        self.play(Create(query_to_model))
        self.play(Create(prompt_box), Write(prompt_text))
        self.play(Create(model_to_prompt))
        self.play(Create(response_box), Write(response_text))
        self.play(Create(prompt_to_response))
        self.play(Write(explanation))
        self.wait(2)
        
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]]) 