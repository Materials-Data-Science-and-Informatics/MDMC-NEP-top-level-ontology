from rdflib import Graph
from rdf_serializer import rdf_serializer


# Load data 
def main():
    G = Graph()
    iri = 'http://example.org/STRAS_RESEARCH_GROUP/'

    G = rdf_serializer(iri)
    G.serialize(destination='../data/STRAS-mapping.ttl', format='turtle')

if __name__ == "__main__":
    main()