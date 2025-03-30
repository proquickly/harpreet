# pip install pyspark

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, avg, desc, count
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

def main():
    os.environ['PYSPARK_PYTHON'] = 'python'
    os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'
    
    spark = SparkSession.builder \
        .appName("PySpark Example") \
        .master("local[*]") \
        .config("spark.driver.extraJavaOptions", "-Dderby.system.home=/tmp/derby") \
        .config("spark.sql.legacy.allowNonEmptyLocationInCTAS", "true") \
        .getOrCreate()
    
    print("Spark session created successfully!")
    
    print("\n--- Creating a simple DataFrame ---")
    data = [
        (1, "John", 28, 5000.0),
        (2, "Anna", 34, 6000.0),
        (3, "Bob", 45, 7500.0),
        (4, "Maria", 37, 8000.0),
        (5, "David", 42, 7200.0)
    ]
    
    columns = ["id", "name", "age", "salary"]
    df = spark.createDataFrame(data, columns)
    
    print("\n--- Original DataFrame ---")
    df.show()
    
    print("\n--- Basic DataFrame operations ---")
    
    print("Selecting columns:")
    df.select("name", "age").show()
    
    print("Filtering data (age > 35):")
    df.filter(col("age") > 35).show()
    
    print("Adding a new column (salary_after_raise):")
    df_with_raise = df.withColumn("salary_after_raise", col("salary") * 1.1)
    df_with_raise.show()
    
    print("\n--- Aggregation ---")
    print("Average salary by age group:")
    df.groupBy(expr("age >= 35").alias("is_senior")) \
        .agg(avg("salary").alias("avg_salary"), count("id").alias("count")) \
        .show()
    
    print("Data ordered by salary (descending):")
    df.orderBy(desc("salary")).show()
    
    print("\n--- Simple ML example with MLlib ---")
    
    ml_data = [
        (1.0, 4.5),
        (2.0, 6.0),
        (3.0, 7.5),
        (4.0, 9.0),
        (5.0, 10.5)
    ]
    ml_df = spark.createDataFrame(ml_data, ["feature", "label"])
    
    assembler = VectorAssembler(
        inputCols=["feature"],
        outputCol="features")
    
    ml_transformed = assembler.transform(ml_df)
    ml_transformed.show()
    
    lr = LinearRegression(featuresCol="features", labelCol="label", 
                          maxIter=5, regParam=0.0)
    lr_model = lr.fit(ml_transformed)
    
    print(f"Coefficients: {lr_model.coefficients}")
    print(f"Intercept: {lr_model.intercept}")
    
    print("\n--- SQL-like operations ---")
    
    df.createOrReplaceTempView("employees")
    
    spark.sql("SELECT name, age, salary FROM employees WHERE salary > 6000").show()
    
    spark.stop()
    print("\nSpark session stopped!")

if __name__ == "__main__":
    main()