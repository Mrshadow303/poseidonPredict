<template>
  <div class="login-page">
    <h1 class="title">Poseidon Predict</h1>
    <div class="login-box">
      <!-- 登录 -->
      <div class="logon" :class="{ hidden: !isLogin }">
        <h2>用户登录</h2>
        <el-form ref="loginForm" :model="loginForm" label-width="50px" :rules="loginFormRule">
          <div class="form-container1">
            <img
              class="login-avatar"
              :src="'https://qiuqiu-bucket1.oss-cn-beijing.aliyuncs.com/f4336d71-4e95-4615-984b-4495e610cdb3.png'"
              alt="Uploaded Image"
            />
            <el-form-item prop="number">
              <el-input
                v-model="loginForm.number"
                placeholder="请输入账号"
                maxlength="11"
                show-word-limit
                clearable
              >
                <template v-slot:prepend>账号</template>
              </el-input>
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                clearable
                placeholder="请输入密码"
                show-password
                style="margin-top: 20px"
              >
                <template v-slot:prepend>
                  密
                  <span class="second-font">码</span>
                </template>
              </el-input>
            </el-form-item>
          </div>
          <div class="btn-gourp">
            <div>
              <el-checkbox
                class="remeber-password"
                v-model="checked"
                style="color: #a0a0a0; margin: 0 0 0px 0"
              >记住密码</el-checkbox>
            </div>
            <div>
              <el-button :loading="loading" @click="login" type="primary" plain>登录</el-button>
            </div>
          </div>
        </el-form>
      </div>
      <!-- 注册 -->
      <div class="register" :class="{ hidden: isLogin }">
        <h2>用户注册</h2>
        <el-form ref="registerForm" :model="addForm" label-width="50px" :rules="addFormRule">
          <el-form-item prop="number">
            <el-input
              v-model="addForm.number"
              placeholder="请输入账号"
              maxlength="11"
              show-word-limit
              clearable
            >
              <template v-slot:prepend>账号</template>
            </el-input>
          </el-form-item>

          <el-form-item prop="name">
            <el-input v-model="addForm.name" placeholder="请输入昵称" clearable>
              <template v-slot:prepend>昵称</template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="addForm.password"
              type="password"
              clearable
              placeholder="请输入密码"
              show-password
            >
              <template v-slot:prepend>
                密
                <span class="second-font">码</span>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="age">
            <el-input v-model.number="addForm.age" placeholder="请输入年龄" clearable>
              <template v-slot:prepend>年龄</template>
            </el-input>
          </el-form-item>

          <el-form-item prop="sex">
            <el-select v-model="addForm.sex" placeholder="请选择性别" clearable>
              <el-option label="男" :value="1"></el-option>
              <el-option label="女" :value="2"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item prop="phone">
            <el-input v-model="addForm.phone" placeholder="请输入手机号" show-word-limit clearable>
              <template v-slot:prepend>手机号</template>
            </el-input>
          </el-form-item>

          <el-form-item prop="mail">
            <el-input v-model="addForm.mail" placeholder="请输入邮箱" show-word-limit clearable>
              <template v-slot:prepend>
                邮
                <span class="second-font">箱</span>
              </template>
            </el-input>
          </el-form-item>

          <div class="btn-gourp">
            <div></div>
            <div>
              <el-button :loading="loading" @click="register" type="primary" plain>注册</el-button>
            </div>
          </div>
        </el-form>
      </div>
      <!-- 左右移动的切换按钮 -->
      <div class="move" ref="moveRef">
        <span style="font-size: 18px; margin-bottom: 25px; color: rgb(225, 238, 250)">
          {{
          !isLogin ? '已有账号？' : '还没有账号？'
          }}
        </span>
        <span style="font-size: 16px; color: rgb(225, 238, 250)">
          {{
          !isLogin ? '欢迎登录账号！' : '欢迎注册账号！'
          }}
        </span>
        <el-button style="width: 100px; margin-top: 30px" @click="changeLogin">
          {{
          !isLogin ? '去登录' : '去注册'
          }}
        </el-button>
      </div>
    </div>
    <div ref="vantaRef" class="vanta"></div>
  </div>
</template>

<script>
import { setToken, setUsername, setAccountNumber } from "@/core/auth.js";
import axios from "axios";
import * as THREE from "three";
import WAVES from "vanta/src/vanta.waves";

console.log("WAVES:" + WAVES);

export default {
  name: "Login",
  data() {
    return {
      loginForm: {
        number: "qiuqiu",
        password: "12345678"
      },
      addForm: {
        number: "",
        name: "", // 昵称
        password: "",
        age: "",
        sex: null, // 性别
        phone: "",
        mail: ""
      },
      loading: false,
      checked: true,
      isLogin: true,
      addFormRule: {
        number: [
          { required: true, message: "请输入账号", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "账号长度必须在3到20位之间",
            trigger: "blur"
          }
        ],
        name: [
          { required: true, message: "请输入昵称", trigger: "blur" },
          {
            min: 2,
            max: 10,
            message: "昵称长度必须在2到10位之间",
            trigger: "blur"
          }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 8, max: 15, message: "密码长度为8~15位", trigger: "blur" }
        ],
        age: [
          { required: true, message: "请输入年龄", trigger: "blur" },
          {
            type: "number",
            min: 1,
            max: 150,
            message: "年龄必须在1到150之间",
            trigger: "blur"
          }
        ],
        sex: [{ required: true, message: "请选择性别", trigger: "change" }],
        phone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          {
            pattern: /^1[3|5|6|7|8|9]\d{9}$/,
            message: "请输入正确的手机号",
            trigger: "blur"
          },
          { min: 11, max: 11, message: "手机号必须是11位", trigger: "blur" }
        ],
        mail: [
          { required: true, message: "请输入邮箱", trigger: "blur" },
          {
            pattern: /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/,
            message: "请输入正确的邮箱号",
            trigger: "blur"
          }
        ]
      },

      loginFormRule: {
        number: [
          { required: true, message: "请输入账号", trigger: "blur" },
          {
            min: 3,
            max: 20,
            message: "账号长度必须在3到20位之间",
            trigger: "blur"
          }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 8, max: 15, message: "密码长度为8~15位", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    // 注册
    // 未实现
    async register() {
      this.$refs.registerForm.validate(async valid => {
        if (valid) {
          // 打印number的类型以及值
          console.log(this.addForm.number + " " + typeof this.addForm.number);
          const res1 = await axios.get(
            this.$httpUrl + "/poseidonPredict/user/hasThisOne",
            {params: { number: this.addForm.number }}
          );
          if (res1.data.success !== false) {
            const res2 = await axios.post(
              this.$httpUrl + "/poseidonPredict/user/save",
              this.addForm
            );
            if (res2.data.success === false) {
              this.$message.warning(res2.data.message);
            } else {
              const res3 = await axios.post(
                this.$httpUrl + "/poseidonPredict/user/login",
                { number: this.addForm.number, password: this.addForm.password }
              );
              const token = res3?.data?.data?.token;
              if (token) {
              }
              this.$message.success("注册登录成功！");
              this.$router.push("/home");
            }
          } else {
            this.$message.warning("账号已存在！");
          }
        } else {
          return false;
        }
      });
    },
    // 登录
    async login() {
      console.log("正在登陆。。。");
      console.log(
        "登录表单：" + this.loginForm.number + "," + this.loginForm.password
      );

      this.$refs.loginForm.validate(async valid => {
        if (valid) {
          const res1 = await axios.post(
            this.$httpUrl + "/poseidonPredict/user/login",
            this.loginForm
          );
          console.log("登录返回结果：" + JSON.stringify(res1));

          // 检查响应的状态码
          if (res1.data.code === 200) {
            // 获取用户信息而不是token
            const user = res1.data.data.user;
            if (user) {
              setToken(user); // 将用户信息作为 token 保存
              setUsername(user.name);
              setAccountNumber(user.number);
              localStorage.setItem("number", user.number);
            }
            this.$message.success("登录成功！");
            // 临时存储
            sessionStorage.setItem("CurUser", JSON.stringify(user));
            // 更新目录
            console.log("res.data.menu:" + JSON.stringify(res1.data.data.menu));
            this.$store.commit("setMenu", res1.data.data.menu);
            //跳转到主页
            this.$router.replace("/Index");
          } else {
            this.$message.warning("用户名或密码错误！");
          }
        } else {
          return false;
        }
      });
    },
    changeLogin() {
      // 切换登录和注册
      this.isLogin = !this.isLogin;
      this.$refs.moveRef.style.transform = this.isLogin
        ? "translate(0, 0)"
        : "translate(-420px, 0)";
    }
  },
  mounted() {
    this.moveRef = this.$refs.moveRef;
    this.vantaRef = this.$refs.vantaRef;

    // 重点 动态背景，这里的 THREE 不要使用最高版本，否则会报错，实测0.125.0版本兼容
    // vanta版本为0.5.24
    this.vantaEffect = WAVES({
      el: this.vantaRef, // 指定 Vanta.js 效果要挂载的 HTML 元素
      THREE: THREE, // 引入 THREE.js 库，用于渲染3D效果
      mouseControls: true, // 是否启用鼠标控制
      touchControls: true, // 是否启用触控控制
      gyroControls: true, // 是否启用陀螺仪控制
      minHeight: 200.0, // 效果显示的最小高度
      minWidth: 200.0, // 效果显示的最小宽度
      scale: 1.0, // 效果的缩放比例
      scaleMobile: 1.0, // 移动设备上的缩放比例
      color: 0x007bff, // 波浪的颜色（十六进制表示法）
      waveHeight: 10.0, // 波浪的高度
      waveSpeed: 1.4, // 波浪的速度
      zoom: 0.8 // 视图的缩放级别
    });
  },
  beforeDestroy() {
    if (this.vantaEffect) this.vantaEffect.destroy();
  }
};
</script>



<style lang="less" scoped>
.login-box {
  border: 2px solid #0984e3;
  overflow: hidden;
  display: flex;
  justify-content: space-between;
  border-radius: 20px;
  padding: 0 40px 0 40px;
  width: 700px;
  position: absolute;
  z-index: 999;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  background-color: #fff;
  animation: hideIndex 0.5s;

  h2 {
    font-size: 30px;
    font-family: PingFangSC-Semibold, PingFang SC;
    font-weight: 600;
    color: #3a3f63;
    width: 100%;
    text-align: center;
    padding: 20px;
  }

  .el-form-item {
    margin-bottom: 23px;
  }

  .btn-gourp {
    margin-top: 30px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;

    .el-button {
      width: 100px;
    }

    .remeber-password {
      left: 0;
      line-height: 0.5rem;
    }
  }

  .el-checkbox {
    width: 100%;
    text-align: center;
    margin-top: 1rem;
  }
}
/* 圆形头像 */
.login-avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  margin: 20px auto;
  display: block;
  transform: translateX(20px);
}

.deep .el-form-item__content {
  margin-left: 0 !important;
}

@keyframes hideIndex {
  0% {
    opacity: 0;
    transform: translate(7.3125rem, -50%);
  }

  100% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

.login-page {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.vanta {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1; /* 确保背景在其他元素的后面 */
}

.logon {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.hidden {
  animation: hidden 1s;
  animation-fill-mode: forwards; // 保持最后的状态
}

@keyframes hidden {
  0% {
    opacity: 1;
  }

  70% {
    opacity: 0;
  }

  100% {
    opacity: 0;
  }
}

.move {
  position: absolute;
  right: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 40%;
  transition-duration: 0.5s;
  align-items: center;
  background: #06beb6;
  background: linear-gradient(to right, #1a8fd5, #0984e3);
}

.title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 15%;
  z-index: 999;
  font-size: 40px;
  color: #fff;
  font-weight: bolder;
}

:deep(.el-input__suffix-inner) {
  width: 60px;
}

.form-container1 {
  transform: translateY(-20%);
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中（可选） */
}

.second-font {
  margin-left: 13px;
}
</style>
