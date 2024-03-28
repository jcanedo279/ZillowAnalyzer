import json
import os

from zillowanalyzer.utility.utility import PROPERTY_DETAILS_PATH
from zillowanalyzer.analyzers.preprocessing import load_data, preprocess_dataframe, FilterMethod
from zillowanalyzer.analyzers.iterator import get_property_info_from_property_details


zip_codes_lakeland = {33859,33863,33831,33813,33846,33884,33812,33880,33839,33811,33877,33807,33885,33566,33838,33840,33803,33563,33564,33882,33883,33888,33804,33802,33815,33801,33806,33851,33881,33844,33823,33850,33805,33565,33845,33810,33809,33868}
zip_codes_so_flo = {33158,33186,33176,33156,33256,33283,33296,33106,33193,33183,33173,33143,33149,33233,33185,33146,33114,33124,33133,33222,33165,33175,33155,33234,33194,33129,33145,33134,33255,33199,33184,33109,33174,33144,33135,33131,33130,33231,33188,33195,33197,33238,33239,33242,33243,33245,33247,33257,33265,33266,33269,33299,33101,33102,33111,33112,33116,33119,33151,33152,33153,33163,33164,33128,33206,33139,33132,33126,33125,33182,33136,33191,33172,33122,33192,33198,33142,33127,33137,33140,33010,33166,33178,33147,33150,33138,33141,33011,33017,33002,33013,33012,33261,33016,33167,33168,33161,33154,33181,33054,33014,33018,33162,33015,33160,33169,33055,33056,33280,33179,33180,33009,33008,33027,33025,33023,33029,33022,33081,33082,33083,33084,33028,33019,33021,33020,33026,33024,33330,33004,33329,33331,33328,33314,33312,33332,33315,33316,33324,33336,33317,33326,33325,33327,33348,33355,33388,33301,33394,33302,33303,33307,33310,33318,33320,33335,33338,33339,33340,33345,33346,33349,33337,33304,33311,33322,33305,33313,33323,33306,33319,33359,33334,33308,33351,33309,33321,33068,33093,33097,33060,33061,33077,33069,33071,33063,33066,33062,33075,33065,33074,33064,33072,33073,33067,33442,33076,33441,33443,33486,33432,33433,33428,33427,33429,33481,33497,33499,33488,33431,33434,33498,33487,33496,33484,33445,33446,33444,33482,33448,33483,33473,33437,33435,33474,33424,33425,33436,33426,33472,33462,33467,33463,33449,33464,33465,33466,33461,33460,33454,33414,33413,33415,33406,33405,33480,33411,33421,33422,33402,33416,33401,33409,33417,33407,33419,33404,33420,33403,33412,33410,33408,33418}

combined_df = load_data()
# combined_df = combined_df[combined_df['zip_code'].isin(zip_codes_so_flo)]
# combined_df = combined_df[combined_df['home_type'] == 'SINGLE_FAMILY']
# combined_df = combined_df[combined_df['year_built'] >= 2000]
# combined_df = combined_df[combined_df['purchase_price'] <= 200000]

sorted_df = combined_df.sort_values(by='adj_CoC 5.0% Down', ascending=False)

for zpid, property_instance in sorted_df.iterrows():
    zip_code = property_instance['zip_code']
    if not os.path.exists(f"{PROPERTY_DETAILS_PATH}/{zip_code}/{zpid}_property_details.json"):
        continue
    with open(f"{PROPERTY_DETAILS_PATH}/{zip_code}/{zpid}_property_details.json") as property_file:
        property_details = json.load(property_file)
        # Yield the loaded JSON data
        if 'props' not in property_details:
            continue
        property_info = get_property_info_from_property_details(property_details)
        has_waterfront_view = property_info['resoFacts']['hasWaterfrontView']
        if not has_waterfront_view or has_waterfront_view == 'None':
            sorted_df.drop(zpid, axis=0, inplace=True)

print(f'Found {sorted_df.shape[0]} homes which meet the criteria.')   
print(sorted_df['home_type'].unique())