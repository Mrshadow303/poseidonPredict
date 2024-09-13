<template>
  <div class="container">
    <h1 class="title">船类识别系统</h1>

    <!-- 上传图片区域 -->
    <div class="upload-section">
      <input type="file" @change="onFileChange" accept="image/*" />
      <button @click="uploadImage" :disabled="!selectedFile" class="upload-btn">上传图片</button>
    </div>

    <!-- 图片显示区域 -->
    <div v-if="uploadedImageUrl" class="image-section">
      <h2>上传的图片:</h2>
      <div class="image-comparison">
        <div class="image-container">
          <img :src="uploadedImageUrl" alt="上传的图片" class="uploaded-image" />
          <a :href="uploadedImageUrl" download="uploaded_image.png" class="download-btn">下载上传的图片</a>
        </div>
        <div v-if="shipImage" class="image-container">
          <img :src="shipImage" alt="识别结果图片" class="result-image" />
          <a :href="shipImage" download="result_image.png" class="download-btn">下载识别结果图片</a>
        </div>
      </div>
    </div>

    <!-- 返回的识别结果 -->
    <div v-if="shipClass" class="result-section">
      <h2>识别结果</h2>
      <div class="result-block">
        <p>
          <strong>船只分类:</strong>
          {{ shipClass }}
        </p>
      </div>
    </div>

    <!-- 添加一些美观的提示信息 -->
    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      uploadedImageUrl: null,
      shipClass: "",
      shipImage: "",
      message: ""
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.uploadedImageUrl = URL.createObjectURL(this.selectedFile);
    },
    uploadImage() {
      // 在这里上传图片到后端，并处理返回的结果
      this.message = "图片上传中...";
      // 创建一个FormData对象
      let formData = new FormData();
      formData.append("image", this.selectedFile);

      // 发送POST请求到你的接口
      console.log("Request URL: ", this.$httpUrl + "/poseidonPredict/yolo/predict");
      this.$axios
        .post(this.$httpUrl + "/poseidonPredict/yolo/predict", formData)
        .then(response => {
          // 处理返回的结果
          let data = response.data;
          console.log("Response data: ", data);
          this.shipClass = data.classes[0];
          this.shipImage = data.image;
          console.log("shipClass: ", this.shipClass);
          console.log("shipImage: ", this.shipImage);
          this.message = "图片上传成功，识别完成！";
        })
        .catch(error => {
          // 处理错误
          this.message = "图片上传失败: " + error.message;
        });
    }
  }
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 50px;
}

.title {
  font-size: 2.5rem;
  color: #4caf50;
}

.upload-section {
  margin: 20px 0;
}

.upload-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
}

.upload-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.image-section,
.result-section {
  margin-top: 30px;
}

.image-comparison {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.image-container {
  width: 45%;
  text-align: center;
}

.uploaded-image,
.result-image {
  width: 100%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.download-btn {
  display: block;
  margin-top: 10px;
  background-color: #4caf50;
  color: white;
  padding: 5px 10px;
  text-decoration: none;
  border-radius: 5px;
}

.result-block {
  margin-top: 20px;
  font-size: 1.2rem;
  padding: 10px;
  border: 2px solid #4caf50;
  display: inline-block;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.message {
  margin-top: 20px;
  font-size: 1.1rem;
  color: #333;
}
</style>
