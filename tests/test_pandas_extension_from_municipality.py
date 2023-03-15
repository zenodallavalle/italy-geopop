# import geopandas as gpd
# import pandas as pd
# import pytest

# from italy_geopop.geopop import ItalyGeopopDataFrame
# from italy_geopop.pandas_extension import pandas_activate_context


# _municipality_columns = [
#     'municipality',
#     'municipality_code',
# ]

# _province_columns = [
#     'province_code',
#     'province',
#     'province_short',
# ]


# _region_columns = [
#     'region',
#     'region_code',
# ]

# _population_columns = [
#     'population',
#     'population_M',
#     'population_F',
# ]


# @pytest.fixture
# def dummy_series() -> pd.Series:
#     """
#     Returns a pd.Series with empty string values '' indexed as range(0, 500, 5).
#     """
#     index = list(range(0, 500, 5))
#     return pd.Series(['' for _ in index], index=index)


# @pytest.fixture
# def municipality_names() -> pd.Series:
#     """
#     Returns a pd.Series with some valid municipality names. This function ensures that returned municipalities are unique in Italy municipalities.
#     """
#     return pd.Series(
#         [
#             'Ronzo-Chienis',
#             'Castelvisconti',
#             'Scafati',
#             'Gandosso',
#             'Vasto',
#             'Vigolo',
#             'Giffone',
#             'Mezzana Rabattone',
#             'Tissi',
#             'Boara Pisani',
#         ]
#     )


# @pytest.fixture
# def municipality_name_complex() -> pd.Series:
#     """
#     Returns a pd.Series with a valid complex municipality name.
#     """
#     return pd.Series(['Comune di Abano Terme'])


# @pytest.fixture
# def municipality_name_complex_to_simple() -> pd.Series:
#     """
#     Returns a pd.Series with a the right simple name for municipality_name_complex above.
#     """
#     return pd.Series(['abano terme'])


# @pytest.fixture
# def not_unequivocal_municipality_name_complex() -> pd.Series:
#     """
#     Returns a pd.Series with a non-unequivocal complex municipality name.
#     """
#     return pd.Series(['Verona or Milano'])


# @pytest.fixture
# def municipality_codes() -> pd.Series:
#     """
#     Returns a pd.Series with some valid municipalities codes.
#     """
#     return pd.Series(
#         [70070, 88007, 60018, 4001, 16131, 17097, 4071, 29026, 26084, 6015]
#     )


# def test_pandas_extension_find_correct_municipality_information_from_names_with_geometry(
#     geopop_df, municipality_names
# ):
#     with pandas_activate_context(include_geometry=True):
#         expected = (
#             geopop_df.set_index('municipality')
#             .loc[municipality_names.to_list()]
#             .reset_index()
#         )
#         expected = pd.merge(
#             expected,
#             ItalyGeopopDataFrame.get_municipalities_geometry(),
#             how='left',
#             left_on='municipality_code',
#             right_index=True,
#         )
#         expected = gpd.GeoDataFrame(expected)

#         output = municipality_names.italy_geopop.from_municipality()
#     output = output[expected.columns]

#     assert (output != expected).sum().sum() == 0


# def test_pandas_extension_find_correct_municipality_information_from_codes_with_geometry(
#     geopop_df, municipality_codes
# ):
#     with pandas_activate_context(include_geometry=True):
#         expected = (
#             geopop_df.set_index('municipality_code')
#             .loc[municipality_codes.to_list()]
#             .reset_index()
#         )
#         expected = pd.merge(
#             expected,
#             ItalyGeopopDataFrame.get_municipalities_geometry(),
#             how='left',
#             left_on='municipality_code',
#             right_index=True,
#         )
#         expected = gpd.GeoDataFrame(expected)

#         output = municipality_codes.italy_geopop.from_municipality()
#     output = output[expected.columns]

#     assert (output != expected).sum().sum() == 0


# def test_pandas_extension_find_correct_municipality_information_from_mixed_names_and_codes_with_geometry(
#     geopop_df, municipality_codes, municipality_names
# ):
#     with pandas_activate_context(include_geometry=True):
#         expected_names = (
#             geopop_df.set_index('municipality')
#             .loc[municipality_names.to_list()]
#             .reset_index()
#         )

#         expected_codes = (
#             geopop_df.set_index('municipality_code')
#             .loc[municipality_codes.to_list()]
#             .reset_index()
#         )
#         expected = pd.concat([expected_names, expected_codes], ignore_index=True)
#         expected = pd.merge(
#             expected,
#             ItalyGeopopDataFrame.get_municipalities_geometry(),
#             how='left',
#             left_on='municipality_code',
#             right_index=True,
#         )
#         expected = gpd.GeoDataFrame(expected)

#         input = pd.concat([municipality_names, municipality_codes], ignore_index=True)

#         output = input.italy_geopop.from_municipality()
#     output = output[expected.columns]

#     assert (output != expected).sum().sum() == 0


# def test_pandas_extension_find_correct_municipality_information_from_complex_municipality_name_with_geometry(
#     municipality_name_complex, municipality_name_complex_to_simple
# ):
#     with pandas_activate_context(include_geometry=True):
#         expected = municipality_name_complex_to_simple.italy_geopop.from_municipality()
#         output = municipality_name_complex.italy_geopop.smart_from_municipality()
#     assert (output != expected).sum().sum() == 0
