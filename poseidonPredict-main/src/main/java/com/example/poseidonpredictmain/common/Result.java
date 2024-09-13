package com.example.poseidonpredictmain.common;

import lombok.Data;

@Data
public class Result {

    private int code;    // 响应码 200 表示成功，其他表示不同的错误情况
    private String msg;  // 响应信息 描述成功或失败的原因
    private Long total;  // 总记录数（用于分页查询）
    private Object data; // 响应数据

    // 成功返回，无数据
    public static Result suc() {
        return result(200, "成功", 0L, null);
    }

    // 成功返回，包含数据
    public static Result suc(Object data) {
        return result(200, "成功", 0L, data);
    }

    // 成功返回，包含数据和总记录数
    public static Result suc(Object data, Long total) {
        return result(200, "成功", total, data);
    }

    // 失败返回，包含错误信息
    public static Result fail(String msg) {
        return result(400, msg, 0L, null);
    }
    public static Result fail() {
        return result(400, "失败", 0L, null);
    }

    // 统一构建响应结果
    private static Result result(int code, String msg, Long total, Object data) {
        Result res = new Result();
        res.setCode(code);
        res.setMsg(msg);
        res.setTotal(total);
        res.setData(data);
        return res;
    }

}
