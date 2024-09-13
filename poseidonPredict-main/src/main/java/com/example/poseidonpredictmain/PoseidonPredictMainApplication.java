package com.example.poseidonpredictmain;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.example.poseidonpredictmain.mapper")
public class PoseidonPredictMainApplication {

	public static void main(String[] args) {
		SpringApplication.run(PoseidonPredictMainApplication.class, args);
	}

}
