from pipeline.extract import read_csv
from pipeline.load import generate_inserts, write_sql_files
from pipeline.transform import Transformer


def main():
    path = "data/nyc_test.csv"
    city = "ny"
    state = "ny"
    out_dir = "./database/add_data"
    
    # 1) Extract
    rows = read_csv(path)

    # 2) Transform
    tf = Transformer(city=city, state=state)
    data = tf.run(rows)

    # 3) Load / SQL generation
    inserts = generate_inserts(data)
    write_sql_files(inserts, out_dir=out_dir)

    print("SQL files generated for tables:", ", ".join(inserts.keys()))


if __name__ == "__main__":
    main()
