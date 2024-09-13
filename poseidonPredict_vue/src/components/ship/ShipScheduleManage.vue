// 船类调度管理页面
<template>
  <div>
    <div style="margin-bottom: 5px;">
      <el-input
        v-model="departurePort"
        placeholder="请输入出发港"
        suffix-icon="el-icon-search"
        style="width: 200px;"
        @keyup.enter.native="loadPost"
      ></el-input>
      <el-input
        v-model="arrivalPort"
        placeholder="请输入到达港"
        suffix-icon="el-icon-search"
        style="width: 200px; margin-left: 5px;"
        @keyup.enter.native="loadPost"
      ></el-input>
      <el-date-picker
        v-model="departureTime"
        type="datetime"
        placeholder="选择出发时间"
        style="width: 250px; margin-left: 5px;"
      ></el-date-picker>
      <el-date-picker
        v-model="arrivalTime"
        type="datetime"
        placeholder="选择到达时间"
        style="width: 250px; margin-left: 5px;"
      ></el-date-picker>
      <el-select v-model="statusFilter" filterable placeholder="请选择状态" style="margin-left: 5px;">
        <el-option
          v-for="item in statuses"
          :key="item.index"
          :label="item.label"
          :value="item.label"
        ></el-option>
      </el-select>
      <el-button type="primary" style="margin-left: 5px;" @click="loadPost">查询</el-button>
      <el-button type="success" @click="resetParam">重置</el-button>
      <el-button type="primary" style="margin-left: 5px;" @click="add">新增</el-button>
    </div>
    <el-table
      :data="tableData"
      :header-cell-style="{ background: '#f2f5fc', color: '#555555' }"
      border
    >
      <el-table-column prop="scheduleId" label="ID" width="60"></el-table-column>
      <el-table-column prop="shipId" label="船舶ID" width="100"></el-table-column>
      <el-table-column prop="departurePort" label="出发港" width="180"></el-table-column>
      <el-table-column prop="arrivalPort" label="到达港" width="180"></el-table-column>
      <el-table-column prop="departureTime" label="出发时间" width="200"></el-table-column>
      <el-table-column prop="arrivalTime" label="到达时间" width="200"></el-table-column>
      <el-table-column prop="status" label="状态" width="100"></el-table-column>
      <el-table-column prop="operate" label="操作">
        <template slot-scope="scope">
          <el-button size="small" type="success" @click="mod(scope.row)">编辑</el-button>
          <el-popconfirm
            title="确定删除吗？"
            @confirm="del(scope.row.scheduleId)"
            style="margin-left: 5px;"
          >
            <el-button slot="reference" size="small" type="danger">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pageNum"
      :page-sizes="[5, 10, 20, 30]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
    ></el-pagination>

    <el-dialog title="提示" :visible.sync="centerDialogVisible" width="30%" center>
      <el-form ref="form" :rules="rules" :model="form" label-width="80px">
        <el-form-item label="船舶ID" prop="shipId">
          <el-col :span="20">
            <el-input v-model="form.shipId"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="出发港" prop="departurePort">
          <el-col :span="20">
            <el-input v-model="form.departurePort"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="到达港" prop="arrivalPort">
          <el-col :span="20">
            <el-input v-model="form.arrivalPort"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="出发时间" prop="departureTime">
          <el-col :span="20">
            <el-date-picker v-model="form.departureTime" type="datetime" placeholder="选择出发时间"></el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="到达时间" prop="arrivalTime">
          <el-col :span="20">
            <el-date-picker v-model="form.arrivalTime" type="datetime" placeholder="选择到达时间"></el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-col :span="20">
            <el-input v-model="form.status"></el-input>
          </el-col>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ShipScheduleManage",
  data() {
    let checkValidTime = (rule, value, callback) => {
      if (!value) {
        callback(new Error("时间不能为空"));
      } else {
        callback();
      }
    };

    return {
      tableData: [],
      pageSize: 5,
      pageNum: 1,
      total: 0,
      departurePort: "",
      arrivalPort: "",
      departureTime: "",
      arrivalTime: "",
      statusFilter: "",
      statuses: [
        { index: 0, label: "全部" },
        { index: 1, label: "计划中" },
        { index: 2, label: "进行中" },
        { index: 3, label: "已完成" },
        { index: 4, label: "取消" }
      ],
      centerDialogVisible: false,
      form: {
        scheduleId: "",
        shipId: "",
        departurePort: "",
        arrivalPort: "",
        departureTime: "",
        arrivalTime: "",
        status: ""
      },
      rules: {
        shipId: [{ required: true, message: "请输入船舶ID", trigger: "blur" }],
        departurePort: [
          { required: true, message: "请输入出发港", trigger: "blur" }
        ],
        arrivalPort: [
          { required: true, message: "请输入到达港", trigger: "blur" }
        ],
        departureTime: [
          { required: true, message: "请选择出发时间", trigger: "blur" },
          { validator: checkValidTime, trigger: "blur" }
        ],
        arrivalTime: [
          { required: true, message: "请选择到达时间", trigger: "blur" },
          { validator: checkValidTime, trigger: "blur" }
        ],
        status: [{ required: true, message: "请输入状态", trigger: "blur" }]
      }
    };
  },
  methods: {
    resetForm() {
      this.$refs.form.resetFields();
    },
    del(scheduleId) {
      console.log(scheduleId);

      this.$axios
        .get(
          this.$httpUrl +
            "/poseidonPredict/shipSchedule/del?scheduleId=" +
            scheduleId
        )
        .then(res => res.data)
        .then(res => {
          console.log(res);
          if (res.code === 200) {
            this.$message({
              message: "操作成功！",
              type: "success"
            });
            this.loadPost();
          } else {
            this.$message({
              message: "操作失败！",
              type: "error"
            });
          }
        });
    },
    mod(row) {
      console.log(row);

      this.centerDialogVisible = true;
      this.$nextTick(() => {
        // 赋值到表单
        this.form.scheduleId = row.scheduleId;
        this.form.shipId = row.shipId;
        this.form.departurePort = row.departurePort;
        this.form.arrivalPort = row.arrivalPort;
        this.form.departureTime = row.departureTime;
        this.form.arrivalTime = row.arrivalTime;
        this.form.status = row.status;
      });
    },
    add() {
      this.centerDialogVisible = true;
      this.$nextTick(() => {
        this.resetForm();
      });
    },
    doSave() {
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/shipSchedule/save", this.form)
        .then(res => res.data)
        .then(res => {
          console.log(res);
          if (res.code === 200) {
            this.$message({
              message: "操作成功！",
              type: "success"
            });
            this.centerDialogVisible = false;
            this.loadPost();
            this.resetForm();
          } else {
            this.$message({
              message: "操作失败！",
              type: "error"
            });
          }
        });
    },
    doMod() {
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/shipSchedule/update", this.form)
        .then(res => res.data)
        .then(res => {
          console.log(res);
          if (res.code === 200) {
            this.$message({
              message: "操作成功！",
              type: "success"
            });
            this.centerDialogVisible = false;
            this.loadPost();
            this.resetForm();
          } else {
            this.$message({
              message: "操作失败！",
              type: "error"
            });
          }
        });
    },
    save() {
      this.$refs.form.validate(valid => {
        if (valid) {
          if (this.form.scheduleId) {
            this.doMod();
          } else {
            this.doSave();
          }
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageNum = 1;
      this.pageSize = val;
      this.loadPost();
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.pageNum = val;
      this.loadPost();
    },
    loadPost() {
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/shipSchedule/listPageC", {
          pageSize: this.pageSize,
          pageNum: this.pageNum,
          param: {
            departurePort: this.departurePort,
            arrivalPort: this.arrivalPort,
            departureTime: this.departureTime,
            arrivalTime: this.arrivalTime,
            status: this.statusFilter
          }
        })
        .then(res => res.data)
        .then(res => {
          console.log(res);
          if (res.code === 200) {
            this.tableData = res.data;
            this.total = res.total;
          } else {
            alert("获取数据失败");
          }
        });
    },
    resetParam() {
      this.departurePort = "";
      this.arrivalPort = "";
      this.departureTime = "";
      this.arrivalTime = "";
      this.statusFilter = "";
    }
  },
  beforeMount() {
    this.loadPost();
  }
};
</script>

<style scoped>
</style>