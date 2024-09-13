package com.example.poseidonpredictmain.service;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.poseidonpredictmain.entity.Ship;

/**
 * 船舶
 */
public interface ShipService extends IService<Ship> {
    IPage pageC(IPage<Ship> page);

    IPage pageCC(IPage<Ship> page, Wrapper wrapper);
}
