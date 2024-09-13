package com.example.poseidonpredictmain.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 船舶调度实体类
 */
@Data
@EqualsAndHashCode(callSuper = false)
@ApiModel(value="ShipSchedule对象", description="船舶调度信息")
public class ShipSchedule implements Serializable {

    private static final long serialVersionUID = 1L; // 推荐定义的 serialVersionUID

    @ApiModelProperty(value = "调度ID", example = "1")
    @TableId(type = IdType.AUTO)
    private Integer scheduleId;

    @ApiModelProperty(value = "船舶ID", example = "1")
    private Integer shipId;

    @ApiModelProperty(value = "出发港口", example = "上海港")
    private String departurePort;

    @ApiModelProperty(value = "到达港口", example = "洛杉矶港")
    private String arrivalPort;

    @ApiModelProperty(value = "出发时间", example = "2024-08-01T08:00:00")
    private LocalDateTime departureTime;

    @ApiModelProperty(value = "到达时间", example = "2024-08-20T16:00:00")
    private LocalDateTime arrivalTime;

    @ApiModelProperty(value = "状态", example = "已完成")
    private String status;

    @ApiModelProperty(value = "创建时间", example = "2024-07-27T15:30:00")
    private LocalDateTime createdAt;

    @ApiModelProperty(value = "更新时间", example = "2024-07-27T15:30:00")
    private LocalDateTime updatedAt;
}
