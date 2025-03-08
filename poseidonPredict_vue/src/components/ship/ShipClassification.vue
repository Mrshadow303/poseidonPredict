<template>
  <div class="container">
    <h1 class="title">船类红外图像识别系统</h1>
    <!-- <h1 class="title">基于知识图谱增强神经网络的图像识别系统</h1> -->
    <h3>适用于红外图像、可见光图像,准确率达到了97.2%</h3>

    <!-- 图片显示区域 -->
    <div class="image-section">
      <div class="image-comparison">
        <div class="image-container">
          <!-- 左边的图片框，包含上传按钮等 -->
          <h2>上传的图片:</h2>
          <div class="image-frame" v-if="!uploadedImageUrl">
              <img src="https://qiuqiu-bucket1.oss-cn-beijing.aliyuncs.com/%E9%BB%98%E8%AE%A4%E5%9B%BE%E7%89%87%E5%9B%BE%E6%A0%87.jpg" alt="默认图标" class="default-image" />
              <!-- 未上传图片时显示上传按钮 -->
              <input type="file" @change="onFileChange" accept="image/*" class="upload-input" />
          </div>
          <div class="image-frame" v-else>
              <!-- 上传图片后显示的内容 -->
              <img :src="uploadedImageUrl" alt="上传的图片" class="uploaded-image" />
          </div>
          <div class = "upload-btn-container" v-if = "uploadedImageUrl">
              <button @click="cancelSelection" class="cancel-btn">取消选择</button>
              <a :href="uploadedImageUrl" download="uploaded_image.png" class="download-btn">下载上传的图片</a>
              <button @click="uploadImage" class="start-recognition-btn">开始识别</button>
          </div>
        </div>
        <div class="image-container">
          <!-- 右边的识别结果图片框 -->
          <h2>识别结果:</h2>
          <div class = "image-frame" v-if ="!shipImage">
            <img src="https://qiuqiu-bucket1.oss-cn-beijing.aliyuncs.com/%E9%BB%98%E8%AE%A4%E5%9B%BE%E7%89%87%E5%9B%BE%E6%A0%87.jpg" alt="默认图标" class="default-image" />
            <p>图片识别结果将在这里展示</p>
          </div>
          <div class="image-frame" v-else >
            <img :src="shipImage" alt="识别结果图片" class="result-image" />
          </div>
          <div class="result-btn-container" v-if="shipImage">
              <a :href="shipImage" download="result_image.png" class="download-btn">下载识别结果图片</a>
          </div>
        </div>
      </div>
    </div>

    <!-- 返回的识别结果 -->
    <div class="result-section" v-if="shipClass.length > 0">
      <div class="result-block" v-for="(className, index) in shipClass" :key="index" style="text-align: left;">
        <p>
          <strong>船只分类:</strong>
          {{ className }}
        </p>
        <p>
          <strong>置信度:</strong>
          {{ shipConfidence[index] }}
        </p>
        <p>
          <strong>边界框:</strong>
          {{ shipBbox[index] }}
        </p>
        <p v-if="shipDetails[index]">
          <strong>船只描述:</strong>
          {{ shipDetails[index].description }}
        </p>
        <p v-if="shipDetails[index]">
          <strong>船只类型:</strong>
          {{ shipDetails[index].types.map(type => type.name).join(', ') }}
        </p>
        <p v-if="shipDetails[index]">
          <strong>所属国家:</strong>
          {{ shipDetails[index].countries.map(country => country.name).join(', ') }}
        </p>
        <p v-if="shipDetails[index]">
          <strong>服役时间:</strong>
          {{ shipDetails[index].serviceTimes.map(service => service.year).join(', ') }}
        </p>
        <p v-if="shipDetails[index]">
          <strong>特点:</strong>
          {{ shipDetails[index].features.map(feature => feature.name).join(', ') }}
        </p>
        <p v-if="shipDetails[index]">
          <strong>用途:</strong>
          {{ shipDetails[index].purposes.map(purpose => purpose.name).join(', ') }}
        </p>
      </div>
    </div>

    <!-- 提示信息 -->
    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      uploadedImageUrl: null,
      shipClass: [],
      shipConfidence: [],
      shipBbox: [],
      shipImage: "",
      shipDetails: [],
      message: ""
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.uploadedImageUrl = URL.createObjectURL(this.selectedFile);
    },
    uploadImage() {
      this.message = "图片上传中...";
      let formData = new FormData();
      formData.append("image", this.selectedFile);

      const requestUrl = `${this.$httpUrl}/poseidonPredict/yolo/predict`;
      this.$axios
        .post(requestUrl, formData)
        .then(response => {
          let data = response.data;
          console.log("data: ", data);
          console.log("data type: ", typeof data);
          console.log("data.classes: ", data.classes);
          console.log("data.confidences: ", data.confidences);
          console.log("data.bboxes: ", data.bboxes);
          this.shipClass = data.classes;
          this.shipConfidence = data.confidences;
          this.shipBbox = data.bboxes;
          this.shipImage = data.image;
          this.shipDetails = data.shipDetails;
          this.message = "图片上传成功，识别完成！";

        })
        .catch(error => {
          this.message = "图片上传失败: " + error.message;
          console.log("error: ", error);
        });
    },
    cancelSelection() {
      this.selectedFile = null;
      this.uploadedImageUrl = null;
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

.image-section {
  margin-top: 30px;
}

.image-comparison {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.image-container {
  display: flex;
  flex-direction: column;
  width: 45%;
  text-align: left;
  padding: 10px;
}

.image-frame {
  width: 100%;
  min-height: 500px;
  border: 4px solid #494949;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  padding: 20px;
  box-sizing: border-box;
}

.upload-btn-container,
.result-btn-container {
  display: flex;
  gap:10px;
  margin-top: 10px;
  justify-content: flex-end; /* 靠右排列 */
}

.upload-input {
  margin-bottom: 10px;
  color: #494949;
  background-color: #929292;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

.default-image {
  width: 100px;
  height: 50%;
}

.start-recognition-btn,
.cancel-btn,
.download-btn {
  background-color: #494949;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

.cancel-btn {
  background-color: #929292;
}

.uploaded-image,
.result-image {
  width: 100%;
  height: auto;
}

.result-section {
  margin-top: 30px;
}

.result-block {
  margin-top: 20px;
  font-size: 1.2rem;
  padding: 10px;
  border: 2px solid #494949;
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
