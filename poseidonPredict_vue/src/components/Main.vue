<template>
  <!-- 用于用户管理系统的用户列表展示和操作。 -->
  <div>
    <div style="margin-bottom: 5px;">
      <!-- 输入框用于输入名字，支持回车查询 -->
      <el-input
        v-model="name"
        placeholder="请输入名字"
        suffix-icon="el-icon-search"
        style="width: 200px;"
        @keyup.enter.native="loadPost"
      ></el-input>
      <!-- 选择框用于选择性别 -->
      <el-select v-model="sex" filterable placeholder="请选择性别" style="margin-left: 5px;">
        <el-option v-for="item in sexs" :key="item.value" :label="item.label" :value="item.value"></el-option>
      </el-select>
      <!-- 查询按钮 -->
      <el-button type="primary" style="margin-left: 5px;" @click="loadPost">查询</el-button>
      <!-- 重置按钮 -->
      <el-button type="success" @click="resetParam">重置</el-button>
      <!-- 新增按钮 -->
      <el-button type="primary" style="margin-left: 5px;" @click="add">新增</el-button>
    </div>

    <div>
      <!-- 表格显示数据 -->
      <el-table :data="tableData" :header-cell-style="{background:'#f2f5fc',color:'#555555'}">
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="number" label="账号" width="180"></el-table-column>
        <el-table-column prop="name" label="姓名" width="180"></el-table-column>
        <el-table-column prop="age" label="年龄" width="80"></el-table-column>
        <el-table-column prop="sex" label="性别" width="80">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.sex === 1 ? 'primary' : 'success'"
              disable-transitions
            >{{ scope.row.sex === 1 ? '男' : '女' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="roleId" label="角色" width="120">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.roleId === 0 ? 'danger' : (scope.row.roleId === 1 ? 'primary' : 'success')"
              disable-transitions
            >{{ scope.row.roleId === 0 ? '领导' : (scope.row.roleId === 1 ? '管理员' : '用户') }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="电话" width="180"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="180"></el-table-column>
        <el-table-column prop="operate" label="操作">
          <template slot-scope="scope">
            <el-button size="small" type="success" @click="mod(scope.row)">编辑</el-button>
            <el-popconfirm title="确定删除吗？" @confirm="del(scope.row.id)" style="margin-left: 5px;">
              <el-button slot="reference" size="small" type="danger">删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div>
      <!-- 分页组件 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pageNum"
        :page-sizes="[5, 10, 20, 30]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </div>

    <el-dialog title="提示" :visible.sync="centerDialogVisible" width="30%" center>
      <!-- 表单用于新增或编辑用户信息 -->
      <el-form ref="form" :rules="rules" :model="form" label-width="80px">
        <el-form-item label="账号" prop="number">
          <el-col :span="20">
            <el-input v-model="form.number"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="名字" prop="name">
          <el-col :span="20">
            <el-input v-model="form.name"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-col :span="20">
            <el-input v-model="form.password"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-col :span="20">
            <el-input v-model="form.age"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.sex">
            <el-radio label="1">男</el-radio>
            <el-radio label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-col :span="20">
            <el-input v-model="form.phone"></el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-col :span="20">
            <el-input v-model="form.email"></el-input>
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
  name: "Main",
  data() {
    // 验证年龄是否过大
    let checkAge = (rule, value, callback) => {
      if (value > 150) {
        callback(new Error("年龄输入过大"));
      } else {
        callback();
      }
    };
    // 验证账号是否重复
    let checkDuplicate = (rule, value, callback) => {
      if (this.form.id) {
        return callback();
      }
      this.$axios
        .get(
          this.$httpUrl +
            "/poseidonPredict/user/findByNo?number=" +
            this.form.number
        )
        .then(res => res.data)
        .then(res => {
          if (res.code != 200) {
            callback();
          } else {
            callback(new Error("账号已经存在"));
          }
        });
    };
    return {
      tableData: [],
      pageSize: 5,
      pageNum: 1,
      total: 0,
      name: "",
      sex: "",
      sexs: [
        {
          value: "1",
          label: "男"
        },
        {
          value: "0",
          label: "女"
        }
      ],
      centerDialogVisible: false,
      form: {
        id: "",
        number: "",
        name: "",
        password: "",
        age: "",
        phone: "",
        sex: "0",
        email: "",
        roleId: "1"
      },
      rules: {
        number: [
          { required: true, message: "请输入账号", trigger: "blur" },
          { min: 3, max: 8, message: "长度在 3 到 8 个字符", trigger: "blur" },
          { validator: checkDuplicate, trigger: "blur" }
        ],
        name: [{ required: true, message: "请输入名字", trigger: "blur" }],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 3, max: 8, message: "长度在 3 到 8 个字符", trigger: "blur" }
        ],
        age: [
          { required: true, message: "请输入年龄", trigger: "blur" },
          { min: 1, max: 3, message: "长度在 1 到 3 个位", trigger: "blur" },
          {
            pattern: /^([1-9][0-9]*){1,3}$/,
            message: "年龄必须为正整数字",
            trigger: "blur"
          },
          { validator: checkAge, trigger: "blur" }
        ],
        phone: [
          { required: true, message: "手机号不能为空", trigger: "blur" },
          {
            pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
            message: "请输入正确的手机号码",
            trigger: "blur"
          }
        ],
        email: [
          { required: true, message: "邮箱不能为空", trigger: "blur" },
          {
            pattern: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
            message: "请输入正确的邮箱地址",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    // 重置表单
    resetForm() {
      this.$refs.form.resetFields();
    },
    // 删除用户
    del(id) {
      this.$axios
        .get(this.$httpUrl + "/poseidonPredict/user/del?id=" + id)
        .then(res => res.data)
        .then(res => {
          if (res.code == 200) {
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
    // 编辑用户
    mod(row) {
      this.centerDialogVisible = true;
      this.$nextTick(() => {
        //赋值到表单
        this.form.id = row.id;
        this.form.number = row.number;
        this.form.name = row.name;
        this.form.password = row.password + "";
        this.form.age = row.age + "";
        this.form.sex = row.sex + "";
        this.form.phone = row.phone;
        this.form.email = row.email;
        this.form.roleId = row.roleId;
      });
    },
    // 新增用户
    add() {
      this.centerDialogVisible = true;
      this.$nextTick(() => {
        this.resetForm();
      });
    },
    // 保存用户信息
    doSave() {
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/user/save", this.form)
        .then(res => res.data)
        .then(res => {
          if (res.code == 200) {
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
    // 更新用户信息
    doMod() {
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/user/update", this.form)
        .then(res => res.data)
        .then(res => {
          console.log(res);
          if (res.code == 200) {
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
    // 保存或更新用户信息
    save() {
      this.$refs.form.validate(valid => {
        if (valid) {
          if (this.form.id) {
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
    // 改变每页显示条数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageNum = 1;
      this.pageSize = val;
      this.loadPost();
    },
    // 改变当前页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.pageNum = val;
      this.loadPost();
    },
    // 加载用户列表
    loadGet() {
      this.$axios
        .get(this.$httpUrl + "/poseidonPredict/user/list")
        .then(res => res.data)
        .then(res => {
          console.log(res);
        });
    },
    // 重置查询参数
    resetParam() {
      this.name = "";
      this.sex = "";
      this.loadPost();
    },
    // 加载分页数据
    loadPost() {
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/user/listPageC1", {
          pageSize: this.pageSize,
          pageNum: this.pageNum,
          param: {
            name: this.name,
            sex: this.sex
          }
        })
        .then(res => res.data)
        .then(res => {
          if (res.code == 200) {
            this.tableData = res.data;
            this.total = res.total;
          } else {
            this.$message({
              message: "操作失败！",
              type: "error"
            });
          }
        });
    }
  },
  beforeMount() {
    // this.loadGet();
    this.loadPost();
  }
};
</script>

<style scoped>
</style>