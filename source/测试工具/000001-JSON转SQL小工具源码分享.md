# JSON转SQL小工具源码分享
![](../wanggang.png)

将key-value的JSON数据，转换为insert的SQL语句，进而实现网页数据存储到数据库。

1. 解析MySQL建表语句，找出“字符串”字段

2. 遍历JSON结构，拼接为SQL语句

1、解析建表语句

之所以要解析建表语句，是因为在拼接SQL时，“字符串”字段没有双引号，需要手动加上。第一步就是通过JDBC来解析表字段，根据字段类型，筛选出“字符串”字段。

```java
public static Map<String, String[]> parseTable(String tableName) {
    List<String> stringType = new ArrayList<>(Arrays.asList("CHAR", "VARCHAR", "TEXT", "DATE", "TIME", "DATETIME", "TIMESTAMP"));
    List<String> stringFieldList = new ArrayList<>();
    try {
        DatabaseMetaData databaseMetaData = conn.getMetaData();
        ResultSet specificResultSet = databaseMetaData.getColumns(null, "%", tableName, "%");
        String columnName;
        String columnType;
        while (specificResultSet.next()) {
            columnName = specificResultSet.getString("COLUMN_NAME");
            columnType = specificResultSet.getString("TYPE_NAME");
            if (stringType.contains(columnType) && !stringFieldList.contains(columnName)) {
                stringFieldList.add(columnName);
            }
        }
    } catch (Exception e) {
        log.error("parse error ", e);
    }
    Map<String, String[]> map = new HashMap<>();
    map.put(tableName, stringFieldList.toArray(new String[0]));
    return map;
}
```

“字符串”字段识别了类型为"CHAR", "VARCHAR", "TEXT", "DATE", "TIME", "DATETIME", "TIMESTAMP"。conn是通过mysql-connector-java创建的数据库连接对象。

2、拼接insert语句

```java
public static String json2Sql(JSONObject json, String tableName) {
    Map<String, String[]> map = parseTable(tableName);
    ArrayList<String> keys = new ArrayList<>();
    ArrayList<String> values = new ArrayList<>();
    for (Map.Entry<String, Object> entry : json.entrySet()) {
        if (entry.getKey().equals("id")) {
            continue;
        }
        keys.add(entry.getKey());
        String value = entry.getValue() == null ? null : entry.getValue().toString();
        if (Arrays.asList(map.get(tableName)).contains(entry.getKey())) {
            if (value != null) {
                if (value.indexOf('"') != -1) {  // 处理扩展字段包含json情况
                    value = String.format("\"%s\"", value.replace("\"", "\\\""));
                } else {
                    value = '"' + value + '"';  // 字符串字段给sql语句手动加上双引号
                }
            }
        }
        values.add(value);
    }
    return String.format("insert into %s(%s) values (%s);", tableName, String.join(",", keys), String.join(",", values));
}
```

拼接时先过滤id字段，然后判空，最后根据“字符串”字段判断是否需要手动添加双引号，注意扩展字段有可能json，也就是会出现双重双引号，需要加上转移字符。

3、测试

```java
@Test
void json2sql() {
    String json = "{\n" +
            "    \"id\": \"1\",\n" +
            "    \"name\": \"gang\",\n" +
            "    \"no\": null,\n" +
            "    \"type\": 1,\n" +
            "    \"created\": \"2020-05-09 11:35:40\",\n" +
            "    \"ext\": \"{\\\"email\\\":\\\"abc@qq.com\\\"}\"\n" +
            "}";
    JSONObject jsonObject = JSON.parseObject(json);
    String sql = DBUtil.json2Sql(jsonObject, "my_test_table");
    log.info(sql);
}
```

输出：

```
insert into my_test_table(ext,no,created,name,type) values ("{\"email\":\"abc@qq.com\"}",null,"2020-05-09 11:35:40","gang",1);
```

JSON转SQL，需要根据字段类型做特殊处理转换。
