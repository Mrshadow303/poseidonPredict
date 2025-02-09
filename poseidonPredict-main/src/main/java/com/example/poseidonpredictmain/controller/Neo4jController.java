package com.example.poseidonpredictmain.controller;

import org.springframework.web.bind.annotation.*;
import java.util.Optional;
import com.example.poseidonpredictmain.entity.Neo4jShipClass;
import com.example.poseidonpredictmain.service.impl.Neo4jShipClassService;

@RestController
@RequestMapping("/myNeo4j")
public class Neo4jController {

    private final Neo4jShipClassService shipClassService;

    public Neo4jController(Neo4jShipClassService shipClassService) {
        this.shipClassService = shipClassService;
    }

    @GetMapping("/{name}")
    public Optional<Neo4jShipClass> getShipClass(@PathVariable String name) {
        return shipClassService.getShipClassDetails(name);
    }
}