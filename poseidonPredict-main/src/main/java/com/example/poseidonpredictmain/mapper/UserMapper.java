package com.example.poseidonpredictmain.mapper;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.Constants;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import com.example.poseidonpredictmain.entity.User;
import org.apache.ibatis.annotations.Select;

/**
 *用户
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {

    @Select("SELECT * FROM user")
    IPage<User> pageC(IPage<User> page);

    @Select("SELECT * FROM user ${ew.customSqlSegment}")
    IPage<User> pageCC(IPage<User> page, @Param(Constants.WRAPPER) Wrapper<User> wrapper);
}
