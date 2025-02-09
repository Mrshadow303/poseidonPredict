package com.example.poseidonpredictmain.entity;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Relationship;
import java.util.Set;
import org.springframework.data.neo4j.core.schema.GeneratedValue;
import lombok.Data;

@Data
@Node("ShipClass")
public class Neo4jShipClass {
    @Id
    private String name;
    private String description;
    private String image_url;

    @Relationship(type = "HAS_TYPE", direction = Relationship.Direction.OUTGOING)
    private Set<Neo4jType> types;

    @Relationship(type = "BELONGS_TO", direction = Relationship.Direction.OUTGOING)
    private Set<Neo4jCountry> countries;

    @Relationship(type = "IN_SERVICE", direction = Relationship.Direction.OUTGOING)
    private Set<Neo4jServiceTime> serviceTimes;

    @Relationship(type = "HAS_FEATURE", direction = Relationship.Direction.OUTGOING)
    private Set<Neo4jFeature> features;

    @Relationship(type = "HAS_PURPOSE", direction = Relationship.Direction.OUTGOING)
    private Set<Neo4jPurpose> purposes;

    // Getters and Setters
}


