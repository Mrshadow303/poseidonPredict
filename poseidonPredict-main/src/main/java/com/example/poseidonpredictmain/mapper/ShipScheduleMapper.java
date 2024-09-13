package com.example.poseidonpredictmain.mapper;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.Constants;
import com.example.poseidonpredictmain.entity.ShipSchedule;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 船舶调度
 */
public interface ShipScheduleMapper extends BaseMapper<ShipSchedule>{
    @Select("SELECT * FROM ship_schedule")
    IPage<ShipSchedule> pageC(IPage<ShipSchedule> page);

    @Select("SELECT * FROM ship_schedule ${ew.customSqlSegment}")
    IPage<ShipSchedule> pageCC(IPage<ShipSchedule> page, @Param(Constants.WRAPPER) Wrapper<ShipSchedule> wrapper);
}
