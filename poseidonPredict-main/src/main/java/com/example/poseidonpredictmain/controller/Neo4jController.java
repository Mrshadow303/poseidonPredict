package com.example.poseidonpredictmain.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;
import com.example.poseidonpredictmain.entity.Neo4jShipClass;
import com.example.poseidonpredictmain.service.impl.Neo4jShipClassService;

@RestController
@RequestMapping("/Neo4j-ship-class")
public class Neo4jController {

    @Autowired
    private Neo4jShipClassService shipClassService;

    @GetMapping("/{name}")
    public Optional<Neo4jShipClass> getShipClassByName(@PathVariable String name) {
        return shipClassService.getShipClassDetailsByName(name);
    }
}