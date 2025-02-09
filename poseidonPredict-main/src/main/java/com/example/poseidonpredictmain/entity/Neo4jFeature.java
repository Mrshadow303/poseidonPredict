package com.example.poseidonpredictmain.entity;

import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Id;
import lombok.Data;

@Node("Feature")
@Data
public class Neo4jFeature {
    @Id
    private String name;

    // Getters and Setters
}