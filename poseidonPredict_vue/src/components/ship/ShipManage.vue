// 船类管理页面
<template>
  <div>
    <div style="margin-bottom: 5px;">
      <el-input
        v-model="name"
        placeholder="请输入船名"
        suffix-icon="el-icon-search"
        style="width: 200px;"
        @keyup.enter.native="loadPost"
      ></el-input>
      <el-select v-model="shipTypeFilter" filterable placeholder="请选择船舶类型" style="margin-left: 5px;">
        <el-option v-for="item in shipTypes" :key="item.index" :label="item.label" :value="item.label"></el-option>
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
      <el-table-column prop="shipId" label="ID" width="60"></el-table-column>
      <el-table-column prop="name" label="船名" width="180"></el-table-column>
      <el-table-column prop="shipType" label="类型" width="180"></el-table-column>
      <el-table-column prop="shipClass" label="类别" width="180"></el-table-column>
      <el-table-column prop="capacityWeight" label="承载重量" width="160"></el-table-column>
      <el-table-column prop="capacityVolume" label="承载容量" width="160"></el-table-column>
      <el-table-column prop="status" label="状态" width="60"></el-table-column>
      <el-table-column prop="operate" label="操作">
        <template slot-scope="scope">
          <el-button size="small" type="success" @click="mod(scope.row)">编辑</el-button>
          <el-popconfirm title="确定删除吗？" @confirm="del(scope.row.shipId)" style="margin-left: 5px;">
            <el-button slot="reference" size="small" type="danger">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pageNum"
      :page-sizes="[5, 10, 20,30]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
    ></el-pagination>

    <el-dialog title="提示" :visible.sync="centerDialogVisible" width="30%" center>
      <el-form ref="form" :rules="rules" :model="form" label-width="80px">
        <el-form-item label="船名" prop="name">
          <el-col :span="20">
            <el-input v-model="form.name"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="类型" prop="shipType">
          <el-col :span="20">
            <el-input v-model="form.shipType"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="类别" prop="sshipClass">
          <el-col :span="20">
            <el-input v-model="form.shipClass"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="承载重量" prop="capacityWeight">
          <el-col :span="20">
            <el-input v-model="form.capacityWeight"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="承载容量" prop="capacityVolume">
          <el-col :span="20">
            <el-input v-model="form.capacityVolume"></el-input>
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
  name: "ShipManage",
  data() {
    let checkCapacity = (rule, value, callback) => {
      if (value <= 0) {
        callback(new Error("承载量必须大于0"));
      } else {
        callback();
      }
    };

    return {
      tableData: [],
      pageSize: 5,
      pageNum: 1,
      total: 0,
      name: "",
      shipTypeFilter: "",
      shipTypes:[
        {index:0,label:"全部"},
        {index:1,label:"货船"},
        {index:2,label:"渔船"},
        {index:3,label:"客船"},
        {index:4,label:"军舰"},
        {index:5,label:"集装箱船"},
        {index:6,label:"其他"}
      ],
      centerDialogVisible: false,
      form: {
        shipId: "",
        name: "",
        shipType: "",
        shipClass: "",
        capacityWeight: "",
        capacityVolume: "",
        status: ""
      },
      rules: {
        name: [{ required: true, message: "请输入船名", trigger: "blur" }],
        shipType: [{ required: true, message: "请输入类型", trigger: "blur" }],
        shipClass: [{ required: true, message: "请输入类别", trigger: "blur" }],
        capacityWeight: [
          { required: true, message: "请输入承载重量", trigger: "blur" },
          { validator: checkCapacity, trigger: "blur" }
        ],
        capacityVolume: [
          { required: true, message: "请输入承载容量", trigger: "blur" },
          { validator: checkCapacity, trigger: "blur" }
        ],
        status: [{ required: true, message: "请输入状态", trigger: "blur" }]
      }
    };
  },
  methods: {
    resetForm() {
      this.$refs.form.resetFields();
      this.shipId = "";
    },
    del(shipId) {
      console.log(shipId);
      this.$axios
        .delete(this.$httpUrl + "/poseidonPredict/ship/deleteById?shipId=" + shipId)
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
        //赋值到表单
        this.form.shipId = row.shipId;
        this.form.name = row.name;
        this.form.shipType = row.shipType;
        this.form.shipClass = row.shipClass;
        this.form.capacityWeight = row.capacityWeight;
        this.form.capacityVolume = row.capacityVolume;
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
        .post(this.$httpUrl + "/poseidonPredict/ship/save", this.form)
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
        .post(this.$httpUrl + "/poseidonPredict/ship/update", this.form)
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
          if (this.form.shipId) {
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
        .post(this.$httpUrl + "/poseidonPredict/ship/listPageC", {
          pageSize: this.pageSize,
          pageNum: this.pageNum,
          param: {
            name: this.name,
            type: this.shipTypeFilter
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
      this.name = "";
      this.shipTypeFilter = "";
    }
  },
  beforeMount() {
    this.loadPost();
  }
};
</script>

<style scoped>
</style>