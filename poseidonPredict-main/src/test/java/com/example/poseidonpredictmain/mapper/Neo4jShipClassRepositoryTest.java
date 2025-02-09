package com.example.poseidonpredictmain.mapper;

import com.example.poseidonpredictmain.entity.Neo4jShipClass;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.Optional;


@SpringBootTest
public class Neo4jShipClassRepositoryTest {
    @Autowired
    private Neo4jShipClassRepository shipClassRepository;

    @Test
    public void testFindByNameWithRelations() {
        // List<Neo4jShipClass> shipClassList = shipClassRepository.findAll();
        // System.out.println("shipClassList: " + shipClassList);
        Optional<Neo4jShipClass> result = shipClassRepository.findShipClassWithRelationsByName("Ada");
        System.out.println("result: " + result);
    }
}
