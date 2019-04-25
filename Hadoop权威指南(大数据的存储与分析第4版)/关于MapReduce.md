MapReduce是一种可用于数据处理的**编程模型**；这是一种简单的模型，但是想写出有用的程序却是不太容易。Hadoop支持各种语言版本的MapReduce程序，这包括Java，Python。MapReduce程序本质上是并行运行的；它的优势在于处理大规模数据集。

# 2.1 气象数据集

## 数据格式

数据是按照行存储的，每行数据以ASCII格式存储，这些数据有很多个小文件组成，我们需要将数据先组合成一个大文件，便于Hadoop高效的处理

# 2.2 使用UNIX工具来分析数据

为了与Hadoop进行有效的对比，使用awk工具编写一个程序脚本，用于计算每年的最高气温。

为了提高程序的处理速度，我们需要并行处理程序来分析数据，但这样做存在一些问题：

1. 划分任务块；任务很难平均的分配到每个处理程序上，使得处理程序得到完整的利用

2. 合并各个程序上的运行结果的方式各不相同

3. 单台计算机的运行速度有限；这时就需要多台设备，此时就需要考虑更多的问题，比如可靠性和协调性。

因此并行处理虽然可行，但很麻烦；使用Hadoop可以解决这些问题

# 2.3 使用Hadoop来分析数据

为了充分利用Hadoop提供的并行处理优势，需要将查询表示成MapReduce作业

## 2.3.1 map和reduce

MapReduce任务过程分两个处理阶段：
1. map阶段
2. reduce阶段

每个阶段以**Key-Value对**作为输入和输出，类型由程序员选择。程序员还需要写两个函数: map函数和reduce函数

map阶段将原始数据读取到处理程序中，将数据处理筛选后传入到reduce阶段，reduce函数将数据合并处理后得到最终数据；让我们使用Hadoop来找出气象数据中每一年中的最高气温。

在本示例中，map阶段的输入数据是气象数据，输入格式为文本格式；输入的key是当前行的起始位置相对于文件起始位置的偏移量，value是数据集中的某一行数据；map函数值提取数据行中的年份和气温值，并筛选掉垃圾数据。处理之后将结果输出到reduce的输入中，在reduce函数中找出最大值。

让我们以数据为例，列举出每一阶段数据的变化
* 原始数据

![原始数据](static/img/2/示例数据.png)

* 经过Hadoop处理之后的Map输入

![Map输入](static/img/2/map输入.png)

* Map处理之后的输出

![Map输出](static/img/2/map输出.png)

* 经过Hadoop处理之后的Reduce输入(此处是对Map输出的key-value进行排序和分组)

![Map输出](static/img/2/reduce输入.png)

* Reduce处理之后的输出

![Map输出](static/img/2/reduce输出.png)

整体的数据处理流程

![数据处理流](static/img/2/数据处理流.png)

## 2.3.2 Java MapReduce

整个实现过程分为三步

1. 实现map函数

    map函数可以通过实现Mapper类中的map方法

    ```java
    import java.io.IOException;

    import org.apache.hadoop.io.IntWritable;
    import org.apache.hadoop.io.LongWritable;
    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.mapreduce.Mapper;
    
    // 正如前面所说，输入和输出的类型由程序员自己定义
    // 这里 输入的key是LongWritable类型的，等价于java中的Long，Hadoop对类型进行的包装使其可以处理更广泛的需求(可优化网络序列化传输)；表示行首相对于文件首的偏移位置
    // 输入的value为Text类型；表示某行数据
    // 输出的key为Text类型；表示年份
    // 输出的value为IntWritable；表示气温值
    public class MaxTemperatureMapper extends MapReduceBase implements Mapper<LongWritable,Text,Text,IntWritable> {

        private static final int MISSING = 9999;

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException,InterruptedException {
            // 将行数据转换为String
            String line = value.toString();
            // 获取年份
            String year = line.substring(15,19);
            // 解析气温值
            int airTemperature;
            if(line.charAt(87) == '+'){
                airTemperature = Intrger.parseInt(line.substring(88,92));
            }else{
                airTemperature = = Intrger.parseInt(line.substring(87,92))
            }
            // 检测值得有效性
            String quality = line.substring(92,93);
            if(airTemperature != MISSING && quality.matches("[01459]")){
                // 当值有效时，通过Context对象将数据传入到Reduce中
                // 第一个实参表示传入Reduce的key
                // 第二个实参表示传入Reduce的value
                // 这里必须和Reduce函数保持一致
                // Content用于输出内容的写入
                context.write(new Text(year),new IntWritable(airTemperature));
            }
        }
        

    }
    ```

2. 实现reduce函数

    reduce函数可以通过实现Reducer类中的reduce方法

    ```java
    import java.io.IOException;

    import org.apache.hadoop.io.IntWritable;
    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.mapreduce.Reducer;

    // 如前所述，输入类型由程序员决定；不过此处有个限制，Reduce的输入必须和Map的输出类型保持一致
    public class MaxTemperatureReducer extends Reducer<Text,IntWritable,Text,IntWritable>{

        // key为年份值
        // value为由Map处理之后的当前年份下的气温值，由于数据记录的是当前的，所以某年中气温值有多个，所以使用了迭代器
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException,InterruptedException {

            // 比较气温值
            int maxValue = Integer.Min_VALUE;
            for(IntWritable value : values){
                maxValue = Math.max(maxValue,value.get());
            }
            // 将最大值输出
            context.write(key, new IntWritable(maxValue));
        }
    }
    ```

3. 运行作业程序

    ```java
    import java.io.IOException;
    import org.apache.hadoop.fs.Path;
    import org.apache.hadoop.io.IntWritable;
    import org.apache.hadoop.io.Text;
    import org.apache.hadoop.mapreduce.Job;
    import org.apache.hadoop.mapreduce.input.FileOutputFormat;
    import org.apache.hadoop.mapreduce.input.FileInputFormat;

    public class MaxTemperature{

        public static void main(String[] args) throws Exception {
            // 校验输入参数
            if(args.length != 2){
                System.err.println("Usage: MaxTemperature <input path> <output path>");
                System.exit(-1);
            }

            // 创建运行MapReduce的工作
            Job job = new Job();
            // 设置jar包；由于在Hadoop上运行这个作业时，需要把代码打包成一个JAR文件
            // setJarByClass()方法接受一个类，Hadoop通过这个类查到到包含它的JAR文件，从而找到相关的JAR文件
            job.setJarByClass(MaxTemperature.class);
            job.setJobName("最高气温");

            // 添加工作的文件输入路径
            // 路径可以使单个的文件，一个目录(将目录下的所有文件当做输入)或符合特定文件模式的一系列文件
            // 函数名以add*开头，说明可以多次调用设置多条路径
            FileInputFormat.addInputPath(job,new Path(args[0]));
            // 设置工作的结果输出路径
            // 这里指的是reduce函数结果的输出目录
            // 注意：在运行前，该目录不应该存在，若果存在，Hadoop会报错并拒绝运行作业，这样坐是为了防止数据丢失(结果被意外覆盖)
            FileOutputFormat.setOutputPath(job,new Path(args(1)));

            // 设置mapper和reduce函数，在java中函数不能独立于类出现所以在此处设置类
            job.setMapperClass(MaxTemperatureMapper.class);
            job.setReducerClass(MaxTemperatureReducer.class);

            // 设置reduce的输出类型
            // 若map和reduce的输出类型相同时，可以不设置map的输出格式，如本例
            // 如果不同，则通过setMapOutputKeyClass和setMapOutputValueClass函数设置map的输出格式
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(IntWritable.class);
            
            // 运行作业并依靠运行的结果停止JVM
            // waitForCompletion方法接受一个Boolean参数；表示是否生成详细的输出
            System.exit(job.waitForCompletion(true) ? 0 : 1);
        }

    }

    ```





