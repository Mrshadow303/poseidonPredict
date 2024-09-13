package com.example.poseidonpredictmain.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.poseidonpredictmain.common.QueryPageParam;
import com.example.poseidonpredictmain.common.Result;
import com.example.poseidonpredictmain.entity.Ship;
import com.example.poseidonpredictmain.service.ShipService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;

/**
 * 船舶接口
 */
@RestController
@CrossOrigin
@RequestMapping("/ship")
public class ShipController {

    @Autowired
    private ShipService shipService;

    // 查询所有船舶
    @GetMapping("/list")
    public Result list() {
        List<Ship> ships = shipService.list();
        return Result.suc(ships);
    }

    // 根据ID查询船舶
    @GetMapping("/findById")
    public Result getShip(@RequestParam String id) {
        Ship ship = shipService.getById(id);
        return ship != null ? Result.suc(ship) : Result.fail("船舶不存在");
    }

    // 新增船舶
    @PostMapping("/save")
    public Result save(@RequestBody Ship ship) {
        System.out.println(ship);
        boolean saved = shipService.save(ship);
        return saved ? Result.suc() : Result.fail("新增失败");
    }

    // 更新船舶
    @PostMapping("/update")
    public Result update(@RequestBody Ship ship) {
        System.out.println(ship);
        boolean updated = shipService.updateById(ship);
        return updated ? Result.suc() : Result.fail("更新失败");
    }

    // 删除船舶
    @DeleteMapping("/deleteById")
    public Result deleteById(@RequestParam String shipId) {
        System.out.println("shipId:"+shipId);
        boolean removed = shipService.removeById(shipId);
        return removed ? Result.suc() : Result.fail("删除失败");
    }

    // 查询（模糊匹配）
    @PostMapping("/listP")
    public Result listP(@RequestBody Ship ship) {
        LambdaQueryWrapper<Ship> queryWrapper = new LambdaQueryWrapper<>();
        if (StringUtils.isNotBlank(ship.getName())) {
            queryWrapper.like(Ship::getName, ship.getName());
        }
        if (StringUtils.isNotBlank(ship.getShipType())) {
            queryWrapper.like(Ship::getShipType, ship.getShipType());
        }
        if (StringUtils.isNotBlank(ship.getStatus())) {
            queryWrapper.like(Ship::getStatus, ship.getStatus());
        }
        List<Ship> ships = shipService.list(queryWrapper);
        return Result.suc(ships);
    }

    // 分页查询
    @PostMapping("/listPage")
    public Result listPage(@RequestBody QueryPageParam queryPageParam) {
        Page<Ship> page = new Page<>(queryPageParam.getPageNum(), queryPageParam.getPageSize());
        HashMap<String, Object> param = queryPageParam.getParam();
        String name = (String) param.get("name");
        String type = (String) param.get("type");
        String status = (String) param.get("status");

        LambdaQueryWrapper<Ship> queryWrapper = new LambdaQueryWrapper<>();
        if (StringUtils.isNotBlank(name)) {
            queryWrapper.like(Ship::getName, name);
        }
        if (StringUtils.isNotBlank(type)) {
            queryWrapper.like(Ship::getShipType, type);
        }
        if (StringUtils.isNotBlank(status)) {
            queryWrapper.like(Ship::getStatus, status);
        }

        IPage<Ship> result = shipService.page(page, queryWrapper);
        return Result.suc(result.getRecords(), result.getTotal());
    }

    // 分页查询（改进版）
    @PostMapping("/listPageC")
    public Result listPageC(@RequestBody QueryPageParam queryPageParam) {
        Page<Ship> page = new Page<>(queryPageParam.getPageNum(), queryPageParam.getPageSize());
        HashMap<String, Object> param = queryPageParam.getParam();
        String name = (String) param.get("name");
        String type = (String) param.get("type");
        String status = (String) param.get("status");

        LambdaQueryWrapper<Ship> queryWrapper = new LambdaQueryWrapper<>();
        if (StringUtils.isNotBlank(name)) {
            queryWrapper.like(Ship::getName, name);
        }
        if (StringUtils.isNotBlank(type)) {
            queryWrapper.like(Ship::getShipType, type);
        }
        if (StringUtils.isNotBlank(status)) {
            queryWrapper.like(Ship::getStatus, status);
        }

        IPage<Ship> result = shipService.pageCC(page, queryWrapper);
        return Result.suc(result.getRecords(), result.getTotal());
    }
}
