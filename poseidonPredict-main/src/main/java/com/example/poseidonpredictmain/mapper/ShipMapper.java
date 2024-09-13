package com.example.poseidonpredictmain.mapper;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.Constants;
import com.example.poseidonpredictmain.entity.Ship;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 船舶
 */
public interface ShipMapper extends BaseMapper<Ship> {
    @Select("SELECT * FROM ship")
    IPage<Ship> pageC(IPage<Ship> page);

    @Select("SELECT * FROM ship ${ew.customSqlSegment}")
    IPage<Ship> pageCC(IPage<Ship> page, @Param(Constants.WRAPPER) Wrapper<Ship> wrapper);
}
