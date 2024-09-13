// 个人主页
<template>
  <div style="text-align: center;background-color: #f1f1f3;height: 100%;padding: 0px;margin: 0px;">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="box-card">
          <!-- 左上个人信息 -->
          <div class="user" style="height: 290px">
            <img :src="getRoleImage(user.roleId)" alt />
            <div class="userinfo">
              <p class="name" v-text="user.number ? user.number : '默认昵称'"></p>
              <p class="access">{{ user.roleId == 0 ? "领导" : (user.roleId == 1 ? "管理员" : "用户") }}</p>
              <el-tag :type="user.sex === '1' ? 'primary' : 'danger'" disable-transitions>
                <i :class="user.sex==1?'el-icon-male':'el-icon-female'"></i>
                {{ user.sex == 1 ? "男" : "女" }}
              </el-tag>

              <el-tag
                type="success"
                disable-transitions
              >{{ user.roleId == 0 ? "领导" : (user.roleId == 1 ? "管理员" : "用户") }}</el-tag>
            </div>
          </div>
        </el-card>

        <el-card class="box-card">
          <h1>路径分布图</h1>
          <div ref="chart_A" style="width: 100%; height: 400px;"></div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="box-card">
          <h1>仓储数量</h1>
          <div ref="chart_B" style="width: 100%; height: 800px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import DateUtils from "./DateUtils";
import * as echarts from "echarts";

export default {
  name: "Home",
  components: { DateUtils },
  data() {
    return {
      user: {},
      url1:
        "https://drift-island.oss-cn-beijing.aliyuncs.com/f4336d71-4e95-4615-984b-4495e610cdb3.png",
      url2:
        "https://drift-island.oss-cn-beijing.aliyuncs.com/02b78a5f-ee93-45ca-8e68-d7a0dddc35cb.png",
      url3:
        "https://drift-island.oss-cn-beijing.aliyuncs.com/1dc2d4df-08ff-4577-ab15-28f6629aaed3.png",

      typeCountData: {
        sea: "",
        ground: "",
        air: ""
      },

      warehouseList: [],

      chart_A: null,
      chart_B: null,
      option: {
        tooltip: {
          trigger: "item"
        },
        legend: {
          top: "5%",
          left: "center"
        },
        series: [
          {
            name: "Route",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
              borderRadius: 10,
              color: function(params) {
                var colorList = ["#00FF00", "#00FFFF", "#FF007F"];
                return colorList[params.dataIndex];
              }
            },
            label: {
              show: false,
              position: "center"
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: "bold"
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 0, name: "陆运" },
              { value: 0, name: "海运" },
              { value: 0, name: "航空" }
            ]
          }
        ]
      },

      optionZhu: {
        legend: {},
        tooltip: {},
        dataset: {
          source: [
            ["物品种类", "A", "B", "C", "D"],
            ["新疆", 133, 334, 100, 20],
            ["西藏", 83.1, 73.4, 55.1, 56],
            ["内蒙古", 86.4, 65.2, 82.5, 78],
            ["青海", 72.4, 53.9, 39.1, 44]
          ]
        },
        xAxis: { type: "category" },
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
          { type: "bar" },
          { type: "bar" },
          { type: "bar" },
          { type: "bar" }
        ]
      }
    };
  },
  computed: {},
  methods: {
    init() {
      this.user = JSON.parse(sessionStorage.getItem("CurUser"));
    },
    getRoleImage(roleId) {
      if (roleId === 0) {
        return this.url1;
      } else if (roleId === 1) {
        return this.url2;
      } else {
        return this.url3;
      }
    }
  },
  created() {
    this.init();
  },
  mounted() {

  }
};
</script>

<style lang="less" scoped>
.el-descriptions {
  width: 90%;
  margin: 0 auto;
  text-align: center;
}

.el-card {
  width: 100%;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-top: 20px;
  margin-right: 20px;

  .user {
    padding-bottom: 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid #ccc;
    display: flex;
    align-items: center;
    img {
      margin-right: 40px;
      width: 150px;
      height: 150px;
      border-radius: 50%;
    }
    .userinfo {
      .name {
        font-size: 32px;
        margin-bottom: 10px;
      }
      .access {
        color: #999999;
      }
    }
  }
}
</style>