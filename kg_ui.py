import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from io import BytesIO
from kg_extraction import extract_kg_from_pdf_bytes, create_directed_tree_graph_from_graph_object
from collections import defaultdict, deque
from kg_gen import KGGen
@st.cache_resource(show_spinner="Loading KGGen...")
def get_kg():
    return KGGen(
        model="openai/gpt-4o",
        temperature=0.0,
        api_key="your-api-key"
    )

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-left: 5vw !important;
        padding-right: 5vw !important;
        padding-top: 2vh !important;
        padding-bottom: 2vh !important;
    }
    </style>
""", unsafe_allow_html=True)


kg = get_kg()


# Helper for prerequisites (define once)
def get_prerequisites(entities, relations, node, visited=None):
    if visited is None:
        visited = set()
    for src, tgt in relations:
        if tgt == node and src not in visited:
            visited.add(src)
            get_prerequisites(entities, relations, src, visited)
    return visited

# Tree-like graph visualization function
def create_tree_layout_figure(graph, selected_nodes=None):
    if selected_nodes is None:
        selected_nodes = set()

    
    # Build directed graph
    G = nx.DiGraph()
    for entity in graph.entities:
        G.add_node(entity)
    
    # Add edges and filter out edges with missing nodes
    valid_edges = []
    for src, tgt in graph.relations:
        if src in graph.entities and tgt in graph.entities:
            G.add_edge(src, tgt)
            valid_edges.append((src, tgt))
        else:
            # Log or handle missing nodes
            if src not in graph.entities:
                print(f"Warning: Edge source '{src}' not found in entities")
            if tgt not in graph.entities:
                print(f"Warning: Edge target '{tgt}' not found in entities")
    print("DEBUG: Total nodes in graph:", len(G.nodes))
    print("DEBUG: Total edges in graph:", len(G.edges))

    # Compute depths (layers) using BFS with consistent ordering
    roots = sorted([n for n in G.nodes() if G.in_degree(n) == 0])
    depth_map = {}
    queue = deque([(root, 0) for root in roots])
    while queue:
        node, depth = queue.popleft()
        if node not in depth_map:
            depth_map[node] = depth
            # Sort children to ensure consistent ordering
            children = sorted(G.successors(node))
            for child in children:
                queue.append((child, depth + 1))

    # Group nodes by depth and sort within each layer for consistency
    layer_nodes = defaultdict(list)
    for node, depth in depth_map.items():
        layer_nodes[depth].append(node)
    
    # Sort nodes within each layer for consistent positioning
    for depth in layer_nodes:
        layer_nodes[depth].sort()

    # Assign x/y positions manually
    pos = {}
    layer_gap = 2.5
    node_gap = 2.5
    for depth in sorted(layer_nodes.keys()):
        nodes = layer_nodes[depth]
        for i, node in enumerate(nodes):
            x = i * node_gap - (len(nodes) - 1) * node_gap / 2
            y = -depth * layer_gap
            pos[node] = (x, y)

    # Prepare node and edge traces

    node_x, node_y, node_text, text_pos, node_colors = [], [], [], [], []

    # Group nodes by y (layer) so we can alternate positions per layer
    y_to_nodes = defaultdict(list)
    for node, (x, y) in pos.items():
        y_to_nodes[y].append((x, node))

    print("DEBUG: Number of positioned nodes:", len(pos))
    print("DEBUG: First few positions:", list(pos.items())[:5])

    for y in sorted(y_to_nodes.keys(), reverse=True):
        nodes_in_layer = sorted(y_to_nodes[y])  # Sort by x for consistent layout
        for i, (x, node) in enumerate(nodes_in_layer):
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            text_pos.append('top center' if i % 2 == 0 else 'bottom center')  # alternate
            node_colors.append('red' if node in selected_nodes else 'blue')

    print("DEBUG: node_x length:", len(node_x))
    print("DEBUG: node_text (first 5):", node_text[:5])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition=text_pos,
        textfont=dict(color='white', size=10),
        marker=dict(color=node_colors, size=20),
        hoverinfo='text',
        showlegend=False
    )

    # Draw edges with arrows
    annotations = []
    for src, tgt in G.edges():
        # Only draw edges where both nodes exist in the position dictionary
        if src in pos and tgt in pos:
            x0, y0 = pos[src]
            x1, y1 = pos[tgt]
            if y0 == y1:
                x1 += 0.2
                y1 -= 0.3
            dx, dy = x1 - x0, y1 - y0
            shrink = 0.1
            x_start = x0 + dx * shrink
            y_start = y0 + dy * shrink
            x_end = x1 - dx * shrink
            y_end = y1 - dy * shrink
            annotations.append(dict(
                ax=x_start, ay=y_start,
                x=x_end, y=y_end,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=1.8,
                arrowcolor='red' if tgt in selected_nodes else 'blue',
                opacity=0.8
            ))

    fig = go.Figure()
    fig.add_trace(node_trace)
    fig.update_layout(
        title='Knowledge Graph (Tree Layout)',
        annotations=annotations,
        hovermode='closest',
        autosize=False,
        width=2000,      # or even 5000 or more
        height=1500,     # increase as much as you want
        margin=dict(b=40, l=40, r=40, t=60),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)',  # <-- transparent background
        plot_bgcolor='rgba(0,0,0,0)'    # <-- transparent plot area
    )
    return fig

st.title("Knowledge Graph Curriculum Extractor")
st.write("Upload a paper to extract a Knowledge Graph from.")

def update_selected_nodes_and_colors(graph, selected_node, selected_nodes):
    """
    Updates the selected_nodes set by adding the selected node and propagating
    selection to its children if all their parents are also selected.
    """
    G = nx.DiGraph()
    G.add_nodes_from(graph.entities)
    G.add_edges_from((src, tgt) for src, tgt in graph.relations)

    if selected_node not in selected_nodes:
        selected_nodes.add(selected_node)

    # Propagate: iteratively add children if all their parents are selected
    added = True
    while added:
        added = False
        for node in graph.entities:
            if node not in selected_nodes:
                parents = list(G.predecessors(node))
                if parents and all(p in selected_nodes for p in parents):
                    selected_nodes.add(node)
                    added = True
    return selected_nodes

uploaded_file = st.file_uploader("Upload a PDF paper", type=["pdf"])
if uploaded_file:
    pdf_bytes = uploaded_file.read()
    # Step 3: Run the function in kg_extraction.py
    if 'graph' not in st.session_state or st.session_state.last_uploaded != pdf_bytes:
        graph = extract_kg_from_pdf_bytes(pdf_bytes, get_kg())
        print(graph.entities)
        st.session_state.graph = graph
        st.session_state.selected_nodes = set()
        st.session_state.last_uploaded = pdf_bytes
    else:
        graph = st.session_state.graph

    st.write("**Select concepts from the dropdown below.** Selected nodes will turn red. Press **Done** to delete them")

    # Node selection UI
    all_nodes = list(graph.entities)
    selected_nodes = st.multiselect("Select concepts to remove:", all_nodes, default=list(st.session_state.selected_nodes))
    
    # Update selection when dropdown changes and propagate to children
    if set(selected_nodes) != st.session_state.selected_nodes:
        st.session_state.selected_nodes = set(selected_nodes)
        
        # Build graph for propagation
        G = nx.DiGraph()
        G.add_nodes_from(graph.entities)
        G.add_edges_from((src, tgt) for src, tgt in graph.relations)
        
        # Propagate: iteratively add children if all their parents are selected
        added = True
        while added:
            added = False
            for node in graph.entities:
                if node not in st.session_state.selected_nodes:
                    parents = list(G.predecessors(node))
                    if parents and all(p in st.session_state.selected_nodes for p in parents):
                        st.session_state.selected_nodes.add(node)
                        added = True
        
        st.rerun()

    # Display the tree-like graph with current selection
    from streamlit.components.v1 import html

    try:
        fig = create_tree_layout_figure(graph, st.session_state.selected_nodes)
        fig_html = fig.to_html(include_plotlyjs="cdn", full_html=False)
        
        html(
            f"""
            <div style="width: 100%; overflow: auto; height: 700px; border: 1px solid #444;">
                <div style="width: fit-content; height: fit-content;">
                    {fig_html}
                </div>
            </div>
            """,
            height=800,
        )
    except Exception as e:
        st.error("❌ The graph is too complex or large to display properly.")
        st.exception(e)




    # Show selected nodes container
    if st.session_state.selected_nodes:
        st.write("**Selected nodes:**")
        for node in sorted(st.session_state.selected_nodes):
            st.write(f"• {node}")

    if st.button("Done"):
        if st.session_state.selected_nodes:
            # Remove only the selected nodes (not their prerequisites)
            to_remove = set(st.session_state.selected_nodes)
            
            # Remove nodes from entities
            original_entity_count = len(graph.entities)
            graph.entities = [e for e in graph.entities if e not in to_remove]
            
            # Remove edges that involve any of the removed nodes
            original_relation_count = len(graph.relations)
            graph.relations = [(src, tgt) for (src, tgt) in graph.relations 
                              if src not in to_remove and tgt not in to_remove]
            
            # Update session state
            st.session_state.graph = graph
            st.session_state.selected_nodes = set()
            
            # Show success message with details
            removed_entities = original_entity_count - len(graph.entities)
            removed_relations = original_relation_count - len(graph.relations)
            st.success(f"Removed {removed_entities} entities and {removed_relations} relations. "
                      f"Graph now has {len(graph.entities)} entities and {len(graph.relations)} relations.")
            
            # Rerun to update the display
            st.rerun()
        else:
            st.warning("No nodes selected for removal.")
else:
    st.write("Please upload a PDF to see the knowledge graph.")
