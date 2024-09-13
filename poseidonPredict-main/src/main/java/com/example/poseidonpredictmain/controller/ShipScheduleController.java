package com.example.poseidonpredictmain.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.poseidonpredictmain.common.QueryPageParam;
import com.example.poseidonpredictmain.common.Result;
import com.example.poseidonpredictmain.entity.ShipSchedule;
import com.example.poseidonpredictmain.service.ShipScheduleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;

/**
 * 船舶调度接口
 */
@RestController
@CrossOrigin
@RequestMapping("/shipSchedule")
public class ShipScheduleController {

    @Autowired
    private ShipScheduleService shipScheduleService;

    // 查询所有船舶
    @GetMapping("/list")
    public Result list() {
        List<ShipSchedule> shipSchedules = shipScheduleService.list();
        return Result.suc(shipSchedules);
    }

    // 根据ID查询船舶
    @GetMapping("/findById")
    public Result getShipSchedule(@RequestParam String id) {
        ShipSchedule shipSchedule = shipScheduleService.getById(id);
        return shipSchedule != null ? Result.suc(shipSchedule) : Result.fail("船舶不存在");
    }

    // 新增船舶
    @PostMapping("/save")
    public Result save(@RequestBody ShipSchedule shipSchedule) {
        boolean saved = shipScheduleService.save(shipSchedule);
        return saved ? Result.suc() : Result.fail("新增失败");
    }

    // 更新船舶
    @PostMapping("/update")
    public Result update(@RequestBody ShipSchedule shipSchedule) {
        boolean updated = shipScheduleService.updateById(shipSchedule);
        return updated ? Result.suc() : Result.fail("更新失败");
    }

    // 删除船舶
    @DeleteMapping("/del")
    public Result delete(@RequestParam String id) {
        boolean removed = shipScheduleService.removeById(id);
        return removed ? Result.suc() : Result.fail("删除失败");
    }


    @PostMapping("/listPage")
    public Result listPage(@RequestBody QueryPageParam queryPageParam) {
        Page<ShipSchedule> page = new Page<>(queryPageParam.getPageNum(), queryPageParam.getPageSize());
        HashMap<String, Object> param = queryPageParam.getParam();
        Integer shipId = (Integer) param.get("ship_id");
        String departurePort = (String) param.get("departure_port");
        String arrivalPort = (String) param.get("arrival_port");
        String departureTime = (String) param.get("departure_time");
        String arrivalTime = (String) param.get("arrival_time");
        String status = (String) param.get("status");

        LambdaQueryWrapper<ShipSchedule> queryWrapper = new LambdaQueryWrapper<>();
        if (shipId != null) {
            queryWrapper.eq(ShipSchedule::getShipId, shipId);
        }
        if (StringUtils.isNotBlank(departurePort)) {
            queryWrapper.like(ShipSchedule::getDeparturePort, departurePort);
        }
        if (StringUtils.isNotBlank(arrivalPort)) {
            queryWrapper.like(ShipSchedule::getArrivalPort, arrivalPort);
        }
        if (StringUtils.isNotBlank(departureTime)) {
            queryWrapper.eq(ShipSchedule::getDepartureTime, departureTime);
        }
        if (StringUtils.isNotBlank(arrivalTime)) {
            queryWrapper.eq(ShipSchedule::getArrivalTime, arrivalTime);
        }
        if (StringUtils.isNotBlank(status)) {
            queryWrapper.like(ShipSchedule::getStatus, status);
        }

        IPage<ShipSchedule> result = shipScheduleService.page(page, queryWrapper);
        return Result.suc(result.getRecords(), result.getTotal());
    }

    // 分页查询（改进版）
    @PostMapping("/listPageC")
    public Result listPageC(@RequestBody QueryPageParam queryPageParam) {
        Page<ShipSchedule> page = new Page<>(queryPageParam.getPageNum(), queryPageParam.getPageSize());
        HashMap<String, Object> param = queryPageParam.getParam();
        Integer shipId = (Integer) param.get("ship_id");
        String departurePort = (String) param.get("departure_port");
        String arrivalPort = (String) param.get("arrival_port");
        String departureTime = (String) param.get("departure_time");
        String arrivalTime = (String) param.get("arrival_time");
        String status = (String) param.get("status");

        LambdaQueryWrapper<ShipSchedule> queryWrapper = new LambdaQueryWrapper<>();
        if (shipId != null) {
            queryWrapper.eq(ShipSchedule::getShipId, shipId);
        }
        if (StringUtils.isNotBlank(departurePort)) {
            queryWrapper.like(ShipSchedule::getDeparturePort, departurePort);
        }
        if (StringUtils.isNotBlank(arrivalPort)) {
            queryWrapper.like(ShipSchedule::getArrivalPort, arrivalPort);
        }
        if (StringUtils.isNotBlank(departureTime)) {
            queryWrapper.eq(ShipSchedule::getDepartureTime, departureTime);
        }
        if (StringUtils.isNotBlank(arrivalTime)) {
            queryWrapper.eq(ShipSchedule::getArrivalTime, arrivalTime);
        }
        if (StringUtils.isNotBlank(status)) {
            queryWrapper.like(ShipSchedule::getStatus, status);
        }

        IPage<ShipSchedule> result = shipScheduleService.page(page, queryWrapper);
        return Result.suc(result.getRecords(), result.getTotal());
    }
}
