package com.example.poseidonpredictmain.service.impl;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.poseidonpredictmain.entity.ShipSchedule;
import com.example.poseidonpredictmain.mapper.ShipScheduleMapper;
import com.example.poseidonpredictmain.service.ShipScheduleService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class ShipScheduleServiceImpl extends ServiceImpl<ShipScheduleMapper, ShipSchedule> implements ShipScheduleService {
    @Resource
    ShipScheduleMapper shipScheduleMapper;
    @Override
    public IPage pageC(IPage<ShipSchedule> page) {
        return shipScheduleMapper.pageC(page);
    }

    @Override
    public IPage pageCC(IPage<ShipSchedule> page, Wrapper wrapper) {
        return shipScheduleMapper.pageCC(page,wrapper);
    }
}
