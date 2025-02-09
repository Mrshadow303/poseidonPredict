package com.example.poseidonpredictmain.entity;

import org.springframework.data.neo4j.core.schema.Id;
import org.springframework.data.neo4j.core.schema.Node;
import lombok.Data;

@Data
@Node("Country")
public class Neo4jCountry {
    @Id
    private String name;

}

