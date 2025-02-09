package com.example.poseidonpredictmain.mapper;

import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;
import org.springframework.data.repository.query.Param;

import com.example.poseidonpredictmain.entity.Neo4jShipClass;

import java.util.Optional;

public interface Neo4jShipClassRepository extends Neo4jRepository<Neo4jShipClass, String> {

    @Query("MATCH (s:ShipClass)-[r]-(related) WHERE s.name = $name RETURN s, collect(r), collect(related)")
    Optional<Neo4jShipClass> findShipClassWithRelationsByName(@Param("name") String name);
}
