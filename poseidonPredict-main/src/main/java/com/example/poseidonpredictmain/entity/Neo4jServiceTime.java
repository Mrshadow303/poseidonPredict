package com.example.poseidonpredictmain.entity;

import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Id;
import lombok.Data;

@Node("ServiceTime")
@Data
public class Neo4jServiceTime {
    @Id
    private String year;

    // Getters and Setters
}
