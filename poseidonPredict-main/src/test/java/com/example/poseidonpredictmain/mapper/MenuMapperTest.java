package com.example.poseidonpredictmain.mapper;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class MenuMapperTest {
    @Autowired
    private MenuMapper menuMapper;

    @Test
    public void selectListTest(){
        System.out.println(menuMapper.selectList(null));
    }
}