// 个人主页
<template>
  <div style="text-align: center;background-color: #f1f1f3;height: 100%;padding: 0px;margin: 0px;">
    <el-row :gutter="20" align="top">
      <el-col :style="{ width: '50%' }">
        <el-card class="box-card" style="height: 40vh;">
          <!-- 左上个人信息 -->
          <div class="user" style="height: 290px">
            <img :src="getRoleImage(user.roleId)" alt />
            <div class="userinfo">
              <p class="name" v-text="user.number ? user.number : '默认昵称'"></p>
              <p class="access">{{ user.roleId == 0 ? "超级管理员" : (user.roleId == 1 ? "管理员" : "用户") }}</p>
              <el-tag :type="user.sex === '1' ? 'primary' : 'danger'" disable-transitions>
                <i :class="user.sex==1?'el-icon-male':'el-icon-female'"></i>
                {{ user.sex == 1 ? "男" : "女" }}
              </el-tag>
              <el-tag
                type="success"
                disable-transitions
              >{{ user.roleId == 0 ? "超级管理员" : (user.roleId == 1 ? "管理员" : "用户") }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :style="{ width: '50%' }">
        <el-card class="box-card" style="height: 40vh;">
          <!-- 右上角折线图 -->
          <div class="line-chart">
            <h2>过去七天访问数</h2>
            <div ref="lineChart" style="width: 100%; height: 300px;"></div>
          </div>
        </el-card>
      </el-col>
      <el-col :style="{ width: '50%' }">
        <el-card class="box-card" style="height: 40vh; overflow-y: auto;">
          <!-- 左下角大屏 -->
          <div class="info-screen">
            <h2>船只状态信息</h2>
            <table style="width: 100%; border-collapse: collapse;">
              <thead>
                <tr>
                  <th style="text-align: left;">船名</th>
                  <th style="text-align: left;">船编号</th>
                  <th style="text-align: left;">状态</th>
                  <th style="text-align: left;">预计时间</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(info, index) in boardingInfo" :key="index" :style="{ backgroundColor: info.color }">
                  <td>{{ info.shipName }}</td>
                  <td>{{ info.shipId }}</td>
                  <td><strong>{{ info.status }}</strong></td>
                  <td>{{ info.estimatedTime }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </el-card>
      </el-col>
      <el-col :style="{ width: '50%' }">
        <el-card class="box-card" style="height: 40vh;">
          <!-- 右下角柱状图 -->
          <div class="bar-chart">
            <h2>过去七日船类识别接口调用次数</h2>
            <div ref="barChart" style="width: 100%; height: 300px;"></div>
          </div>
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
        "https://qiuqiu-bucket1.oss-cn-beijing.aliyuncs.com/f4336d71-4e95-4615-984b-4495e610cdb3.png",
      url2:
        "https://qiuqiu-bucket1.oss-cn-beijing.aliyuncs.com/02b78a5f-ee93-45ca-8e68-d7a0dddc35cb.png",
      url3:
        "https://qiuqiu-bucket1.oss-cn-beijing.aliyuncs.com/1dc2d4df-08ff-4577-ab15-28f6629aaed3%20%281%29.png",

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
      },

      optionZhu: {
        legend: {},
        tooltip: {},
        dataset: {},
        xAxis: { type: "category" },
        yAxis: {},
        series: [
          { type: "bar" },
          { type: "bar" },
          { type: "bar" },
          { type: "bar" }
        ]
      },
      boardingInfo: [
        { shipName: "船只A", shipId: "001", status: "正在离港", estimatedTime: "预计离港时间: 14:30", color: "#d1e7dd" },
        { shipName: "船只B", shipId: "002", status: "等待离港", estimatedTime: "预计离港时间: 15:00", color: "#fff3cd" },
        { shipName: "船只C", shipId: "003", status: "正在入港", estimatedTime: "预计入港时间: 16:00", color: "#d1e7cd" },
        { shipName: "船只D", shipId: "004", status: "即将入港", estimatedTime: "预计入港时间: 16:30", color: "#fff3cd" },
        { shipName: "船只E", shipId: "005", status: "正在装载", estimatedTime: "预计装载完毕时间: 17:00", color: "#cfe2f3" },
        { shipName: "船只F", shipId: "006", status: "装载完毕", estimatedTime: "预计完工时间: 18:00", color: "#d1a8dd" },
        { shipName: "船只G", shipId: "007", status: "已离港", estimatedTime: "预计到达时间: 19:00", color: "#a1ddff" }
      ],
      visitData: this.generateVisitData(), // 生成过去七天的访问数据
      recognitionData: this.generateRecognitionData() // 生成过去七天的识别数据
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
    },
    generateVisitData() {
      return Array.from({ length: 7 }, () => Math.floor(Math.random() * 200));
    },
    generateRecognitionData() {
      return Array.from({ length: 7 }, () => Math.floor(Math.random() * 100));
    },
    renderLineChart() {
      const chartDom = this.$refs.lineChart;
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: '过去七天访问数'
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: this.getLastSevenDays()
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          name: '访问数',
          type: 'line',
          data: this.visitData
        }]
      };
      myChart.setOption(option);
    },
    renderBarChart() {
      const chartDom = this.$refs.barChart;
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: '过去七日船类识别接口调用次数'
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: this.getLastSevenDays()
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          name: '调用次数',
          type: 'bar',
          data: this.recognitionData
        }]
      };
      myChart.setOption(option);
    },
    getLastSevenDays() {
      const days = [];
      const today = new Date();
      for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() - (6 - i));
        days.push(date.toLocaleDateString());
      }
      return days;
    }
  },
  created() {
    this.init();
  },
  mounted() {
    this.renderLineChart();
    this.renderBarChart();
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

.line-chart, .bar-chart, .info-screen {
  margin: 20px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}
.info-screen {
  max-height: 300px;
  overflow-y: auto;
}
.info-screen ul {
  list-style-type: none;
  padding: 0;
}
.info-screen li {
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
}
.info-screen .divider {
  border-top: 1px solid #ccc;
  margin: 5px 0;
}
</style>