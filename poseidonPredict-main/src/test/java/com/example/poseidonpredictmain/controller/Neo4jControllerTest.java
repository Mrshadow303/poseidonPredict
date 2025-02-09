package com.example.poseidonpredictmain.controller;

import com.example.poseidonpredictmain.entity.Neo4jShipClass;
import com.example.poseidonpredictmain.service.impl.Neo4jShipClassService;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Optional;

@SpringBootTest
public class Neo4jControllerTest {


    @Mock
    private Neo4jShipClassService shipClassService;

    @InjectMocks
    private Neo4jController neo4jController;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void getShipClassTest() {
        Optional<Neo4jShipClass> result = neo4jController.getShipClass("Ada");
        System.out.println("result: " + result);
    }
}