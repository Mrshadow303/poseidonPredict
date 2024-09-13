// 目录管理页面
<template>
  <div>
    <el-input v-model="menuName" placeholder="请输入菜单名字" style="width: 200px;"></el-input>
    <el-button type="primary" style="margin-left: 5px;" @click="loadMenus">查询</el-button>
    <el-button type="success" @click="resetParams">重置</el-button>

    <el-button type="primary" style="margin-left: 5px;" @click="addMenu">新增菜单</el-button>

    <el-table :data="menuList" border>
      <el-table-column prop="id" label="ID" width="60"></el-table-column>
      <el-table-column prop="menuName" label="菜单名字" width="180"></el-table-column>
      <el-table-column prop="menuLevel" label="菜单级别" width="100"></el-table-column>
      <el-table-column prop="menuClick" label="菜单点击事件" width="180"></el-table-column>
      <el-table-column prop="menuComponent" label="菜单组件" width="180"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="small" type="success" @click="editMenu(scope.row)">编辑</el-button>
          <el-popconfirm title="确定删除吗？" @confirm="deleteMenu(scope.row.id)" style="margin-left: 5px;">
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

    <!-- 编辑/新增菜单的 Dialog -->
    <el-dialog title="编辑菜单" :visible.sync="dialogVisible" width="30%" center>
      <el-form ref="menuForm" :rules="menuRules" :model="currentMenu" label-width="80px">
        <el-form-item label="菜单名字" prop="menuName">
          <el-input v-model="currentMenu.menuName"></el-input>
        </el-form-item>
        <el-form-item label="菜单级别" prop="menuLevel">
          <el-input v-model="currentMenu.menuLevel"></el-input>
        </el-form-item>
        <el-form-item label="菜单点击事件" prop="menuClick">
          <el-input v-model="currentMenu.menuClick"></el-input>
        </el-form-item>
        <el-form-item label="菜单组件" prop="menuComponent">
          <el-input v-model="currentMenu.menuComponent"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMenu">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "MenuManage",
  data() {
    return {
      menuList: [],
      pageSize: 5,
      pageNum: 1,
      total: 0,
      menuName: "",
      dialogVisible: false,
      currentMenu: {
        id: "",
        menuName: "",
        menuLevel: "",
        menuClick: "",
        menuComponent: ""
      },
      menuRules: {
        menuName: [
          { required: true, message: "请输入菜单名字", trigger: "blur" }
        ],
        menuLevel: [
          { required: true, message: "请输入菜单级别", trigger: "blur" }
        ],
        menuClick: [
          { required: true, message: "请输入菜单点击事件", trigger: "blur" }
        ],
        menuComponent: [
          { required: true, message: "请输入菜单组件", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    resetParams() {
      this.menuName = "";
    },
    loadMenus() {
      // 模拟从后端获取菜单列表数据，实际应用需要调用 API
      // 示例数据，实际需根据后端返回的数据结构进行调整
      this.menuList = [
        { id: 1, menuName: "菜单1", menuLevel: 1, menuClick: "click1", menuComponent: "Component1.vue" },
        { id: 2, menuName: "菜单2", menuLevel: 2, menuClick: "click2", menuComponent: "Component2.vue" },
        { id: 3, menuName: "菜单3", menuLevel: 1, menuClick: "click3", menuComponent: "Component3.vue" }
      ];
      this.total = this.menuList.length;
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageNum = 1;
      this.pageSize = val;
      this.loadMenus();
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.pageNum = val;
      this.loadMenus();
    },
    addMenu() {
      this.dialogVisible = true;
      this.$refs.menuForm.resetFields();
      this.currentMenu = {
        id: "",
        menuName: "",
        menuLevel: "",
        menuClick: "",
        menuComponent: ""
      };
    },
    editMenu(menu) {
      this.dialogVisible = true;
      this.currentMenu = { ...menu };
    },
    saveMenu() {
      this.$refs.menuForm.validate(valid => {
        if (valid) {
          // 模拟保存菜单数据到后端，实际应用需要调用 API
          console.log("保存菜单：", this.currentMenu);
          this.dialogVisible = false;
          this.loadMenus(); // 保存成功后重新加载菜单列表
        } else {
          console.log("表单验证失败！");
        }
      });
    },
    deleteMenu(id) {
      console.log("删除菜单ID: ", id);
      // 模拟删除菜单，实际应用需要调用 API
      // 删除成功后重新加载菜单列表
      this.loadMenus();
    }
  },
  created() {
    this.loadMenus(); // 组件创建时加载菜单列表
  }
};
</script>

<style scoped>
</style>
