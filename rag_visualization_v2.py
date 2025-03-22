from manim import *
import numpy as np
import random

class RAGVisualizationV2(Scene):
    def construct(self):
        # Title
        title = Text("Retrieval-Augmented Generation (RAG)", font_size=40)
        subtitle = Text("Using LlamaIndex Concepts", font_size=28).next_to(title, DOWN)
        header = VGroup(title, subtitle)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait()
        self.play(header.animate.scale(0.6).to_edge(UP))
        
        # Create a stages diagram
        stages_title = Text("RAG Pipeline Stages", font_size=32).next_to(header, DOWN, buff=0.5)
        
        # Create the 5 stages boxes
        stages = ["Loading", "Indexing", "Storing", "Querying", "Evaluation"]
        stage_boxes = VGroup(*[
            VGroup(
                Rectangle(width=2.2, height=1, fill_opacity=0.3, fill_color=BLUE),
                Text(stage, font_size=24)
            ).arrange(ORIGIN)
            for stage in stages
        ]).arrange(RIGHT, buff=0.5)
        
        stage_group = VGroup(stages_title, stage_boxes).arrange(DOWN, buff=0.5)
        
        self.play(Write(stages_title))
        self.play(*[Create(box[0]) for box in stage_boxes])
        self.play(*[Write(box[1]) for box in stage_boxes])
        self.wait()
        
        # Fade out the stages
        self.play(FadeOut(stage_group))
        self.play(FadeOut(header))
        
        # Create detailed visualization components
        
        # 1. Loading Stage
        loading_title = VGroup(
            Text("Loading", font_size=28, color=BLUE),
            Text("Stage", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        
        doc_box = Rectangle(width=1.5, height=2, fill_opacity=0.2, fill_color=GRAY)
        doc_text = Text("Documents", font_size=20).next_to(doc_box, UP)
        docs = VGroup(doc_box, doc_text)
        
        node_boxes = VGroup(*[
            Rectangle(width=1.2, height=0.5, fill_opacity=0.3, fill_color=GREEN_B)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.1)
        node_text = Text("Nodes", font_size=20).next_to(node_boxes, UP)
        nodes = VGroup(node_boxes, node_text)
        
        connector = Arrow(doc_box.get_right(), node_boxes.get_left(), color=WHITE)
        connector_text = Text("Connectors/\nReaders", font_size=18).next_to(connector, UP, buff=0.1)
        
        loading_group = VGroup(loading_title, docs, nodes, connector, connector_text).arrange(RIGHT, buff=1)
        loading_title.shift(RIGHT * 1)  # Move title more to the right
        
        # Explanation text for loading stage
        loading_explanation = Text(
            "Loading: Ingesting data from sources (PDFs, websites, APIs).",
            font_size=16
        ).next_to(loading_group, DOWN)
        
        self.play(Write(loading_title))
        self.play(Create(doc_box), Write(doc_text))
        self.play(
            *[Create(box) for box in node_boxes],
            Write(node_text)
        )
        self.play(Create(connector), Write(connector_text))
        self.play(Write(loading_explanation))
        self.wait(2)
        
        # Clear previous content
        self.play(
            *[FadeOut(mob) for mob in [loading_title, docs, nodes, connector, connector_text, loading_explanation]]
        )
        
        # 2. Indexing Stage
        indexing_title = Text("Indexing Stage", font_size=28, color=BLUE)
        
        # Nodes (left side)
        node_boxes_small = VGroup(*[
            Rectangle(width=1.5, height=0.3, fill_opacity=0.3, fill_color="#556B2F")  # Dark olive green
            for _ in range(4)
        ]).arrange(DOWN, buff=0.1)
        node_text_small = Text("Nodes", font_size=20).next_to(node_boxes_small, UP)
        nodes_small = VGroup(node_boxes_small, node_text_small)
        
        # Embedding Model box and text (between nodes and embeddings)
        embed_model_box = Rectangle(width=1.8, height=0.6, fill_opacity=0.1, color=WHITE)
        embed_model_text = Text("Embedding\nModel", font_size=16)
        embed_model = VGroup(embed_model_box, embed_model_text).arrange(ORIGIN)
        
        # Embedding vectors (middle)
        vectors = VGroup(*[
            Line(
                start=ORIGIN,
                end=RIGHT * random.uniform(0.5, 1),
                color=YELLOW
            )
            for _ in range(4)
        ]).arrange(DOWN, buff=0.2)
        vector_box = Rectangle(width=1.5, height=1.5, fill_opacity=0.1, color=WHITE)
        vector_text = Text("Embeddings", font_size=20).next_to(vector_box, UP)
        vector_group = VGroup(vectors, vector_box, vector_text)
        vectors.move_to(vector_box)
        
        # Vector database (right)
        db_box = Rectangle(width=2, height=1.8, fill_opacity=0.3, fill_color="#8B4513")  # Brown color
        db_text = Text("Vector Store", font_size=20).next_to(db_box, UP)
        db = VGroup(db_box, db_text)
        
        # Position all components horizontally with reduced spacing
        components = VGroup(nodes_small, embed_model, vector_group, db).arrange(RIGHT, buff=1.2)
        
        # Create horizontal arrows
        nodes_to_model = Arrow(
            node_boxes_small.get_right(),
            embed_model.get_left(),
            color=WHITE,
            buff=0.1
        )
        
        model_to_vectors = Arrow(
            embed_model.get_right(),
            vector_box.get_left(),
            color=WHITE,
            buff=0.1
        )
        
        vectors_to_db = Arrow(
            vector_box.get_right(),
            db_box.get_left(),
            color=WHITE,
            buff=0.1
        )
        
        # Position title and explanation
        indexing_title.next_to(components, UP, buff=0.5)
        
        # Explanation text for indexing stage
        indexing_explanation = Text(
            "Indexing: Transforming Nodes into vector embeddings\n"
            "and storing them in a vector database for efficient retrieval",
            font_size=14
        ).next_to(components, DOWN, buff=0.3)
        
        # Animate the indexing stage
        self.play(Write(indexing_title))
        self.play(
            *[Create(box) for box in node_boxes_small],
            Write(node_text_small)
        )
        self.play(Create(nodes_to_model))
        self.play(Create(embed_model_box), Write(embed_model_text))
        self.play(Create(model_to_vectors))
        self.play(
            Create(vector_box),
            Write(vector_text),
            *[Create(v) for v in vectors]
        )
        self.play(Create(vectors_to_db))
        self.play(Create(db_box), Write(db_text))
        self.play(Write(indexing_explanation))
        self.wait(2)
        
        # Clear previous content
        self.play(
            *[FadeOut(mob) for mob in [indexing_title, nodes_small, vector_group, db, 
                                      nodes_to_model, model_to_vectors, vectors_to_db,
                                      embed_model, indexing_explanation]]
        )
        
        # 3. Querying Stage
        querying_title = Text("Querying Stage", font_size=28, color=BLUE)
        
        # Vector DB (central component)
        db_box = Rectangle(width=2.0, height=2.0, fill_opacity=0.3, fill_color="#8B4513")  # Brown color, reduced from 3x3
        db_text = Text("Vector Store", font_size=24).next_to(db_box, UP)
        db = VGroup(db_box, db_text)
        
        # User query (left side)
        query_box = Rectangle(width=2, height=0.8, fill_opacity=0.3, fill_color="#556B2F")  # Dark olive green
        query_text = Text("User Query", font_size=20)
        query = VGroup(query_box, query_text).arrange(ORIGIN)
        
        # Retrieved nodes (right side)
        retrieved_nodes = VGroup(*[
            Rectangle(width=2, height=0.6, fill_opacity=0.3, fill_color="#556B2F")
            for _ in range(2)
        ]).arrange(DOWN, buff=0.3)
        retrieved_text = Text("Retrieved\nNodes", font_size=20).next_to(retrieved_nodes, UP)
        retrieved = VGroup(retrieved_nodes, retrieved_text)
        
        # LLM circle (below)
        llm_circle = Circle(radius=0.6, fill_opacity=0.4, fill_color="#483D8B")  # Dark slate blue, reduced from 1.2
        llm_text = Text("LLM", font_size=24)
        llm = VGroup(llm_circle, llm_text).arrange(ORIGIN)
        
        # Output (bottom)
        output_box = Rectangle(width=2.5, height=0.8, fill_opacity=0.3, fill_color="#2F4F4F")  # Dark slate gray
        output_text = Text("Generated\nResponse", font_size=20)
        output = VGroup(output_box, output_text).arrange(ORIGIN)
        
        # Position components
        db.move_to(UP * 1)  # Move the central Vector Store up
        query.move_to(LEFT * 4)  # Position horizontally first
        retrieved.move_to(RIGHT * 4 + UP * 1.1)  # Move retrieved nodes up to match Vector Store
        llm.move_to(DOWN * 1)  # Move LLM up
        output.move_to(DOWN * 3)  # Move output up
        querying_title.move_to(db.get_top() + UP * 1.5)  # Title will follow Vector Store position
        
        # Align query with vector store center
        query.align_to(db_box, UP).shift(DOWN * db_box.height/2 + UP *.4)
        
        # Arrows and labels
        query_to_db = Arrow(
            query_box.get_right(),
            db_box.get_left(),
            color=WHITE,
            buff=0.1
        )
        router_text = Text("Router", font_size=16).next_to(query_to_db, UP, buff=0.1)
        
        db_to_retrieved = Arrow(
            db_box.get_right(),
            retrieved_nodes.get_left(),
            color=WHITE,
            buff=0.1
        )
        retriever_text = Text("Retriever", font_size=16).next_to(db_to_retrieved, UP, buff=0.1)
        
        # Arrows to LLM
        query_to_llm = Arrow(
            query.get_bottom(),
            llm_circle.get_left(),
            color=WHITE,
            buff=0
        )
        
        retrieved_to_llm = Arrow(
            retrieved_nodes.get_bottom(),
            llm_circle.get_right(),
            color=WHITE,
            buff=0
        )
        context_text = Text("Context", font_size=20).next_to(retrieved_to_llm, RIGHT, buff=0.1)
        
        # Arrow to output
        llm_to_output = Arrow(llm_circle.get_bottom(), output.get_top(), color=WHITE)
        response_text = Text("Response\nSynthesizer", font_size=16).next_to(llm_to_output, RIGHT, buff=0.1)
        
        # Animate the querying stage
        self.play(Write(querying_title))
        self.play(Create(db_box), Write(db_text))
        self.play(Create(query_box), Write(query_text))
        self.play(Create(query_to_db), Write(router_text))
        self.play(*[Create(node) for node in retrieved_nodes], Write(retrieved_text))
        self.play(Create(db_to_retrieved), Write(retriever_text))
        self.play(Create(llm_circle), Write(llm_text))
        self.play(Create(query_to_llm))
        self.play(Create(retrieved_to_llm), Write(context_text))
        self.play(Create(llm_to_output), Write(response_text))
        self.play(Create(output_box), Write(output_text))
        
        # Explanation text for querying stage
        querying_explanation = Text(
            "Querying: User query is converted to an embedding, relevant context is retrieved,\n"
            "and both query and context are sent to the LLM to generate a response",
            font_size=16
        ).next_to(output, DOWN, buff=0.5)
        
        self.play(Write(querying_explanation))
        self.wait(2)
        
        # Fade out everything except stage diagram at top
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [*stage_boxes, stages_title, header]]
        )
        
        # Benefits of RAG
        benefits_title = Text("Benefits of RAG", font_size=32).move_to(DOWN * 1)
        
        benefits = VGroup(
            Text("• No training needed - more cost-effective", font_size=24),
            Text("• Always up-to-date with latest data", font_size=24),
            Text("• Transparent and trustworthy results", font_size=24),
            Text("• Reduces hallucinations with factual grounding", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(benefits_title, DOWN, buff=0.5)
        
        self.play(Write(benefits_title))
        for benefit in benefits:
            self.play(Write(benefit))
            self.wait(0.5)
        
        self.wait(2)
        
        # Final fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Final message
        final_message = Text("RAG: Enhancing LLMs with Your Data", font_size=40)
        self.play(Write(final_message))
        self.wait(2)
        self.play(FadeOut(final_message)) 