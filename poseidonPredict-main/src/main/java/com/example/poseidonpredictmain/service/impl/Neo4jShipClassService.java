package com.example.poseidonpredictmain.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.poseidonpredictmain.entity.Neo4jShipClass;
import com.example.poseidonpredictmain.mapper.Neo4jShipClassRepository;

import java.util.Optional;

@Service
public class Neo4jShipClassService {
    @Autowired
    private Neo4jShipClassRepository shipClassRepository;

    public Optional<Neo4jShipClass> getShipClassDetailsByName(String name) {
        return shipClassRepository.findShipClassWithRelationsByName(name);
    }
}
