package com.example.poseidonpredictmain.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

import com.example.poseidonpredictmain.mapper.MenuMapper;
import com.example.poseidonpredictmain.entity.Menu;
import com.example.poseidonpredictmain.service.MenuService;
import org.springframework.stereotype.Service;


@Service
public class MenuServiceImpl extends ServiceImpl<MenuMapper, Menu> implements MenuService {

}
