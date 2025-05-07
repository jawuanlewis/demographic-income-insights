import pandas as pd
from typing import List


# Load the census dataset from file
def load_data(filepath: str, column_names: List[str]) -> pd.DataFrame:
    df = pd.read_csv(
        filepath, names=column_names, na_values=["?"], skipinitialspace=True
    )
    print(f"\nSuccessfully loaded data from {filepath}")
    return df


# Find the columns that contain missing values
def find_missing_values(df: pd.DataFrame) -> List[str]:
    columns_with_missing = []
    missing_counts = df.isnull().sum()

    for column, count in missing_counts.items():
        if count > 0:
            columns_with_missing.append(column)

    return columns_with_missing


# Clean the entire dataset
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    columns_with_missing = find_missing_values(df)

    # Replace missing values with column's mode
    for column in columns_with_missing:
        mode_value = df_cleaned[column].mode()[0]
        missing_count = df_cleaned[column].isnull().sum()
        df_cleaned[column] = df_cleaned[column].fillna(mode_value)
        print(
            f"\nReplaced {missing_count} missing values in {column} with mode: {mode_value}"
        )

    return df_cleaned


# Generate a comprehensive report of the cleaned dataset
def generate_cleaning_report(df: pd.DataFrame, df_cleaned: pd.DataFrame) -> None:
    print("\n=== Cleaning Report ===")
    print(f"Total rows in dataset: {len(df)}")

    # Report on columns that had missing values
    columns_with_missing = find_missing_values(df)
    print("\nDistribution of previously missing value columns:")
    for column in columns_with_missing:
        print(f"\n{column} value counts:")
        print(df[column].value_counts().head())

    # Check for any remaining missing values
    remaining_missing = df_cleaned.isnull().sum()
    if remaining_missing.any():
        print("\nWarning: Remaining missing values:")
        print(remaining_missing[remaining_missing > 0])
    else:
        print("\nNo missing values remain in the dataset.")


# Main function to coordinate the cleaning process
def clean_census_data(filepath: str) -> pd.DataFrame:
    columns = [
        "age",
        "workclass",
        "fnlwgt",
        "education",
        "education-num",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "capital-gain",
        "capital-loss",
        "hours-per-week",
        "native-country",
        "income",
    ]

    print("\nLoading data...")
    df = load_data(filepath, columns)

    find_missing_values(df)

    print("\nCleaning data...")
    df_cleaned = clean_data(df)

    generate_cleaning_report(df, df_cleaned)

    return df_cleaned


if __name__ == "__main__":
    try:
        print("Starting data cleaning process...")
        cleaned_df = clean_census_data("data/adult.data")

        # Save cleaned dataset
        cleaned_df.to_csv("data/cleaned_census_data.csv", index=False)
        print("\nCleaned dataset saved to 'cleaned_census_data.csv'")

    except Exception as e:
        print(f"Error during data cleaning: {e}")
