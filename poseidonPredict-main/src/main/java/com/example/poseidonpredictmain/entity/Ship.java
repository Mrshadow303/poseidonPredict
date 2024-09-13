package com.example.poseidonpredictmain.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 船舶实体类
 */
@Data
@EqualsAndHashCode(callSuper = false)
@ApiModel(value="Ship对象", description="船舶信息")
public class Ship implements Serializable {

    private static final long serialVersionUID = 1L; // 推荐定义的 serialVersionUID

    @ApiModelProperty(value = "船舶ID", example = "1")
    @TableId(type = IdType.AUTO)
    private Integer shipId;

    @ApiModelProperty(value = "船舶名称", example = "Titanic")
    private String name;

    @ApiModelProperty(value = "船舶类型", example = "运输船")
    private String shipType;

    @ApiModelProperty(value = "船舶等级", example = "Luxury")
    private String shipClass;

    @ApiModelProperty(value = "船舶载重能力（吨）", example = "50000.00")
    private BigDecimal capacityWeight;

    @ApiModelProperty(value = "船舶容积能力（立方米）", example = "10000.00")
    private BigDecimal capacityVolume;

    @ApiModelProperty(value = "船舶载客量", example = "2000")
    private Integer capacityPassengers;

    @ApiModelProperty(value = "船舶状态", example = "Active")
    private String status;

    @ApiModelProperty(value = "创建时间", example = "2024-07-27T15:30:00")
    private LocalDateTime createdAt;

    @ApiModelProperty(value = "更新时间", example = "2024-07-27T15:30:00")
    private LocalDateTime updatedAt;
}
