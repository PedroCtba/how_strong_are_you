def main(raw_data_path, clean_data_path):
    """
    This function cleans raw data from a CSV file and saves the cleaned data to a parquet file.
    The function also makes the numerics fields as small as they can be.

    Parameters:
        raw_data_path (str): The path to the raw data CSV file.
        clean_data_path (str): The path to save the cleaned parquet file.

    Returns:
        None
    """
    # Imports
    import polars as pl

    # Load the data 
    df = pl.read_csv(raw_data_path, infer_schema_length=100_000)

    # Converter tipos float64 para float32
    df = df.with_columns(pl.col(pl.Float64).cast(pl.Float32))

    # Retirando sexo "Mx"
    df = df.filter(pl.col("Sex") != "Mx")

    # Marcando atletas nulos na coluna de testagem como não testados
    df = df.with_columns(Tested=pl.when(pl.col("Tested").is_null()).then(pl.lit("No")).otherwise(pl.col("Tested")))

    # Retirando linhas duplicadas
    df = df.filter(~df.is_duplicated())

    # Retirando linhas sem total
    df = df.filter(pl.col("TotalKg").is_not_null())

    # Pegar apenas casos usuais de competição com 3 tentativas por lift
    df = df.filter(pl.col("Bench4Kg").is_null() & pl.col("Squat4Kg").is_null() & pl.col("Deadlift4Kg").is_null())

    # Dropar colunas de 4 tentativa
    df = df.drop(["Bench4Kg", "Squat4Kg", "Deadlift4Kg"])

    # Shrink data types
    df = df.with_columns(pl.all().shrink_dtype())

    # Save data on clean path
    df.write_parquet(clean_data_path)

    # Return None
    return None

# Run as script
if __name__ == "__main__":
    # Import raw path
    from secret import path_to_raw_file, clean_data_path

    # Run script
    main(raw_data_path=path_to_raw_file, clean_data_path=clean_data_path)
