package com.example.poseidonpredictmain.service;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.poseidonpredictmain.entity.ShipSchedule;

/**
 * 船舶调度
 */
public interface ShipScheduleService extends IService<ShipSchedule> {
    IPage pageC(IPage<ShipSchedule> page);

    IPage pageCC(IPage<ShipSchedule> page, Wrapper wrapper);
}
