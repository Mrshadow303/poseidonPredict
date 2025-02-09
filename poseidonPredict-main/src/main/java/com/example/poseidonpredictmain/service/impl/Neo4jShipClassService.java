package com.example.poseidonpredictmain.service.impl;

import org.springframework.stereotype.Service;

import com.example.poseidonpredictmain.entity.Neo4jShipClass;
import com.example.poseidonpredictmain.mapper.Neo4jShipClassRepository;

import java.util.Optional;

@Service
public class Neo4jShipClassService {
    private final Neo4jShipClassRepository shipClassRepository;

    public Neo4jShipClassService(Neo4jShipClassRepository shipClassRepository) {
        this.shipClassRepository = shipClassRepository;
    }

    public Optional<Neo4jShipClass> getShipClassDetails(String name) {
        return shipClassRepository.findShipClassWithRelationsByName(name);
    }
}
