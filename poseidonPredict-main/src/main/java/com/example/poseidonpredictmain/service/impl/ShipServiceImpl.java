package com.example.poseidonpredictmain.service.impl;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.poseidonpredictmain.entity.Ship;
import com.example.poseidonpredictmain.mapper.ShipMapper;
import com.example.poseidonpredictmain.service.ShipService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class ShipServiceImpl extends ServiceImpl<ShipMapper, Ship> implements ShipService {
    @Resource
    ShipMapper shipMapper;
    @Override
    public IPage pageC(IPage<Ship> page) {
        return shipMapper.pageC(page);
    }

    @Override
    public IPage pageCC(IPage<Ship> page, Wrapper wrapper) {
        return shipMapper.pageCC(page,wrapper);
    }
}
