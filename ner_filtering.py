import spacy
from collections import defaultdict
import types

def install_spacy_model():
    """Install spaCy English model if not already installed"""
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        # If model is not installed, install it
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
        return nlp

def tag_entities_with_ner(entities):
    """
    Tag entities with NER labels and return a dictionary mapping entities to their NER tags
    
    Args:
        entities: List of entity strings
        
    Returns:
        dict: Mapping of entities to their NER tags
    """
    nlp = install_spacy_model()
    entity_tags = {}
    
    for entity in entities:
        # Process the entity text with spaCy
        doc = nlp(entity)
        
        # Get NER tags for the entity
        ner_tags = []
        for ent in doc.ents:
            ner_tags.append(ent.label_)
        
        # If no NER tags found, mark as 'NO_TAG'
        if not ner_tags:
            entity_tags[entity] = ['NO_TAG']
        else:
            entity_tags[entity] = ner_tags
    
    return entity_tags

def filter_and_clean_entities(entities, relations, entity_tags):
    """
    Filter out entities with PERSON, LOCATION, ORG, and NORP tags (if ORG/NORP is not a source in any edge)
    
    Args:
        entities: List of entity strings
        relations: List of (subject, predicate, object) tuples
        entity_tags: Dictionary mapping entities to their NER tags
        
    Returns:
        tuple: (filtered_entities, filtered_relations)
    """
    # Find entities with PERSON, LOCATION, ORG, or NORP tags
    filtered_out_entities = set()
    person_entities = set()
    location_entities = set()
    org_entities = set()
    norp_entities = set()
    
    # Get all source entities from relations
    source_entities = set()
    for src, rel, tgt in relations:
        source_entities.add(src)
    
    for entity, tags in entity_tags.items():
        if 'PERSON' in tags:
            person_entities.add(entity)
            filtered_out_entities.add(entity)
        if 'LOC' in tags or 'GPE' in tags:  # LOC and GPE are spaCy's location tags
            location_entities.add(entity)
            filtered_out_entities.add(entity)
        if 'ORG' in tags:
            org_entities.add(entity)
            # Only filter out ORG entities if they are NOT used as sources in any edge
            if entity not in source_entities:
                filtered_out_entities.add(entity)
                print(f"Removing ORG entity '{entity}' (not used as source in any edge)")
            else:
                print(f"Keeping ORG entity '{entity}' (used as source in edges)")
        if 'NORP' in tags:
            norp_entities.add(entity)
            # Only filter out NORP entities if they are NOT used as sources in any edge
            if entity not in source_entities:
                filtered_out_entities.add(entity)
                print(f"Removing NORP entity '{entity}' (not used as source in any edge)")
            else:
                print(f"Keeping NORP entity '{entity}' (used as source in edges)")
    
    print(f"Found {len(person_entities)} entities with PERSON tags: {person_entities}")
    print(f"Found {len(location_entities)} entities with LOCATION tags: {location_entities}")
    print(f"Found {len(org_entities)} entities with ORG tags: {org_entities}")
    print(f"Found {len(norp_entities)} entities with NORP tags: {norp_entities}")
    
    # Filter out PERSON, LOCATION, unused ORG, and unused NORP entities from entities list
    filtered_entities = [entity for entity in entities if entity not in filtered_out_entities]
    
    # Filter out relations that involve filtered entities
    filtered_relations = []
    for src, rel, tgt in relations:
        if src not in filtered_out_entities and tgt not in filtered_out_entities:
            filtered_relations.append((src, rel, tgt))
    
    print(f"Original entities: {len(entities)}")
    print(f"After filtering PERSON, LOCATION, unused ORG, and unused NORP entities: {len(filtered_entities)}")
    print(f"Original relations: {len(relations)}")
    print(f"After filtering PERSON, LOCATION, unused ORG, and unused NORP entities: {len(filtered_relations)}")
    
    return filtered_entities, filtered_relations

def process_graph_with_ner(graph):
    """
    Main function to process a knowledge graph with NER tagging and filtering
    
    Args:
        graph: Knowledge graph object with .entities and .relations attributes
        
    Returns:
        object: New graph object with filtered entities and relations
    """
    # Tag all entities with NER
    print("Tagging entities with NER...")
    entity_tags = tag_entities_with_ner(graph.entities)
    
    # Show some examples of tagged entities
    print("\nSample entity tags:")
    for i, (entity, tags) in enumerate(list(entity_tags.items())[:10]):
        print(f"{entity}: {tags}")
    
    # Filter out PERSON, LOCATION, unused ORG, and unused NORP entities and clean the graph
    print("\nFiltering out PERSON, LOCATION, unused ORG, and unused NORP entities...")
    filtered_entities, filtered_relations = filter_and_clean_entities(
        list(graph.entities), 
        list(graph.relations), 
        entity_tags
    )
    
    # Return a SimpleNamespace for linter/static analysis friendliness

    return types.SimpleNamespace(entities=filtered_entities, relations=filtered_relations) 
