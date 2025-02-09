package com.example.poseidonpredictmain.entity;

import org.springframework.data.neo4j.core.schema.Node;
import org.springframework.data.neo4j.core.schema.Id;
import lombok.Data;

@Node("Purpose")
@Data
public class Neo4jPurpose {
    @Id
    private String name;

}
