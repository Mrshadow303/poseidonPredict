package com.example.poseidonpredictmain.controller;

import javax.imageio.ImageIO;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.core.io.FileSystemResource;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

@RestController
@CrossOrigin
@RequestMapping("/yolo")
public class ShipClassificationController {
    private static final String[] names = {
            "Ada",
            "Independence",
            "Visby",
            "Alvaro De Bazan",
            "Jiangkai II",
            "Oliver Hazard Perry",
            "Akizuki",
            "Sejong Daewang",
            "Zumwalt",
            "Armourique"
    };
    private static final String FLASK_SERVER_URL = "http://localhost:5000/predict";  // Flask 服务的 URL

    @PostMapping("/predict")
    public ResponseEntity<?> predict(@RequestParam("image") MultipartFile imageFile) {
        System.out.println("收到图片识别请求");
        try {
            // 将上传的图像文件保存到本地
            String filePath = saveFile(imageFile);

            // 通过HTTP请求将图像文件发送到Flask服务器
            String response = sendImageToFlask(filePath);
            System.out.println("flask返回值为"+response);

            // 解析Flask返回的JSON响应
            JSONObject jsonResponse = new JSONObject(response);
            JSONArray predictions = jsonResponse.getJSONArray("predictions");
            List<String> classes = new ArrayList<>();
            List<List<Integer>> bboxes = new ArrayList<>();
            for (int i = 0; i < predictions.length(); i++) {
                JSONObject prediction = predictions.getJSONObject(i);
                int classIndex = prediction.getInt("class");
                classes.add(names[classIndex]);
                JSONArray bbox = prediction.getJSONArray("box");
                List<Integer> box = new ArrayList<>();
                for (int j = 0; j < bbox.length(); j++) {
                    box.add(bbox.getInt(j));
                }
                bboxes.add(box);
            }
            System.out.println(classes);
            System.out.println(bboxes);


            // 在图片上绘制框并添加类别标签
            BufferedImage image = ImageIO.read(new File(filePath));
            Graphics2D g2d = image.createGraphics();
            for (int i = 0; i < bboxes.size(); i++) {
                List<Integer> box = bboxes.get(i);
                int x1 = box.get(0); // 左上角x坐标
                int y1 = box.get(1); // 左上角y坐标
                int x2 = box.get(2); // 右下角x坐标
                int y2 = box.get(3); // 右下角y坐标
                float hue = (float) i / bboxes.size(); // 根据索引计算色调
                Color color = Color.getHSBColor(hue, 1.0f, 1.0f); // 生成随机颜色
                g2d.setColor(color); // 设置颜色
                g2d.drawRect(x1, y1, x2 - x1, y2 - y1); // 绘制矩形
                g2d.drawString(classes.get(i), x1, y1 - 5); // 添加类别标签
            }
            g2d.dispose();

            // 将图片转换为Base64编码的字符串
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ImageIO.write(image, "png", baos);
            byte[] imageBytes = baos.toByteArray();
            String base64Image = Base64.getEncoder().encodeToString(imageBytes);

            // 返回处理结果
            //System.out.println(ResponseEntity.ok().body("{\"classes\":" + classes.toString() + ", \"image\":\"data:image/png;base64," + base64Image + "\"}").toString());
            return ResponseEntity.ok().body("{\"classes\":" + "\""+classes.toString() +"\""+ ", \"image\":\"data:image/png;base64," + base64Image + "\"}");


        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("文件处理时发生错误: " + e.getMessage());
        }
    }

    // 保存上传的图像文件
    private String saveFile(MultipartFile imageFile) throws IOException {
        String fileName = imageFile.getOriginalFilename();
        String filePath = "E:\\Idea\\mywork\\poseidonPredict\\poseidonPredict-main\\src/main/resources/static/images/income_image/" + fileName;
        File file = new File(filePath);
        imageFile.transferTo(file);
        return filePath;
    }

    // 发送图像文件到 Flask 服务器，并返回推理结果
    private String sendImageToFlask(String filePath) {
        RestTemplate restTemplate = new RestTemplate();

        // 准备文件
        FileSystemResource fileResource = new FileSystemResource(new File(filePath));

        // 准备请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        // 创建 HttpEntity 以包含文件和头
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("image", fileResource);
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        // 发送请求并获取响应
        ResponseEntity<String> response = restTemplate.exchange(FLASK_SERVER_URL, HttpMethod.POST, requestEntity, String.class);

        // 返回 Flask 服务器的推理结果
        return response.getBody();
    }
}
