from manim import *
import numpy as np

class RAGScene(Scene):
    def construct(self):
        # Title
        title = Text("Retrieval-Augmented Generation (RAG)", font_size=40)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.scale(0.6).to_edge(UP))

        # Create query box
        query_box = Rectangle(height=0.8, width=2, fill_opacity=0.3, fill_color=GREEN)
        query_text = Text("Query", font_size=24)
        query = VGroup(query_box, query_text).shift(LEFT * 4)
        
        # Create encoder boxes
        query_encoder = Rectangle(height=1, width=1.5, fill_opacity=0.3, fill_color=YELLOW)
        query_encoder_text = Text("Query\nEncoder", font_size=20).scale(0.8)
        query_encoder_group = VGroup(query_encoder, query_encoder_text).next_to(query, RIGHT, buff=1)
        
        # Modified positioning: Document encoder to the right of query encoder
        doc_encoder = Rectangle(height=1, width=1.5, fill_opacity=0.3, fill_color=YELLOW)
        doc_encoder_text = Text("Document\nEncoder", font_size=20).scale(0.8)
        doc_encoder_group = VGroup(doc_encoder, doc_encoder_text).next_to(query_encoder_group, RIGHT, buff=1.5)
        
        # Move document corpus to align with document encoder
        docs = VGroup(*[
            Rectangle(height=0.8, width=1.2, fill_opacity=0.3, fill_color=BLUE)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.3)
        
        # Position the document corpus above the document encoder
        docs.move_to(doc_encoder.get_center() + UP * 2)
        docs_label = Text("Document Corpus", font_size=24).next_to(docs, UP)
        
        # Create generator
        generator = Rectangle(height=1.2, width=2, fill_opacity=0.3, fill_color=RED)
        generator_text = Text("Generator", font_size=24)
        generator_group = VGroup(generator, generator_text).shift(DOWN * 1.5)
        
        # Create output
        output_box = Rectangle(height=0.8, width=2, fill_opacity=0.3, fill_color=PURPLE)
        output_text = Text("Generated\nOutput", font_size=20)
        output = VGroup(output_box, output_text).next_to(generator_group, DOWN, buff=1)
        
        # Animate document corpus
        self.play(
            Write(docs_label),
            *[Create(doc) for doc in docs]
        )
        
        # Animate query
        self.play(Create(query_box), Write(query_text))
        
        # Animate encoders
        self.play(
            Create(query_encoder),
            Write(query_encoder_text),
            Create(doc_encoder),
            Write(doc_encoder_text)
        )
        
        # Show encoding process
        query_vec = Arrow(start=query.get_right(), end=query_encoder.get_left(), color=GREEN)
        
        # Individual arrows from each document to document encoder
        doc_vecs = VGroup(*[
            Arrow(
                start=doc.get_bottom(), 
                end=doc_encoder.get_top(), 
                color=BLUE
            )
            for doc in docs
        ])
        
        self.play(Create(query_vec))
        self.play(*[Create(vec) for vec in doc_vecs])
        
        # Show retrieval process - update arrows to connect to generator
        retrieval_lines = VGroup(*[
            DashedLine(
                start=doc_encoder.get_bottom(),
                end=generator.get_top() + RIGHT * 0.5,  # Offset slightly to the right
                color=YELLOW,
                dash_length=0.1
            )
            for _ in range(1)
        ])
        
        query_to_generator = Arrow(
            start=query_encoder.get_bottom(),
            end=generator.get_top() + LEFT * 0.5,  # Offset slightly to the left
            color=GREEN
        )
        
        self.play(
            Create(generator_group),
            Create(query_to_generator),
            *[Create(line) for line in retrieval_lines]
        )
        
        # Show output generation
        self.play(Create(output_box), Write(output_text))
        
        # Add explanation text
        explanation = VGroup(
            Text("1. Query and documents are encoded", font_size=20),
            Text("2. Relevant documents are retrieved", font_size=20),
            Text("3. Generator combines query & context", font_size=20),
            Text("4. Final output is generated", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8).to_edge(RIGHT)
        
        self.play(Write(explanation[0]))
        self.wait()
        self.play(Write(explanation[1]))
        self.wait()
        self.play(Write(explanation[2]))
        self.wait()
        self.play(Write(explanation[3]))
        self.wait(2)
        
        # Fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        ) 