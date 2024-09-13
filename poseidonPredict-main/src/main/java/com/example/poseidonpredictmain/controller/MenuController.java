package com.example.poseidonpredictmain.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.example.poseidonpredictmain.common.Result;
import com.example.poseidonpredictmain.service.MenuService;
import com.example.poseidonpredictmain.entity.Menu;

import java.util.List;

/**
 * 菜单控制器
 */
@RestController
@CrossOrigin
@RequestMapping("/menu")
public class MenuController {

    @Autowired
    private MenuService menuService;

    @GetMapping("/list")
    public Result list(@RequestParam String roleId) {
        List list = menuService.lambdaQuery().like(Menu::getMenuRight, roleId).list();
        return Result.suc(list);
    }
}
