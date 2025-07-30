from tinydb import TinyDB,Query


db=TinyDB('db.json',indent=4)
user=Query()

# s=db.get('matematika')
db.insert_multiple(
    [
           {
               "savoli": "5 + 7 = ?",
               "a": 10,
               "b": 11,
               "c": 12,
               "d": 13
                },
           {
                    "savoli": "9 - 4 = ?",
                    "a": 3,
                    "b": 4,
                    "c": 5,
                    "d": 6
                },
            {
                    "savoli": "6 × 3 = ?",
                    "a": 12,
                    "b": 18,
                    "c": 24,
                    "d": 21
                },
            {
                    "savoli": "20 ÷ 5 = ?",
                    "a": 3,
                    "b": 4,
                    "c": 5,
                    "d": 6
                },
            {
                    "savoli": "15 + 8 = ?",
                    "a": 22,
                    "b": 23,
                    "c": 24,
                    "d": 25
                },
    ]
)
# db.insert(
#      {
#         "matematika": {
#             "test_malumoti": "Salom, bu test matematikaga taalluqli bo'lib, u 10 ta savoldan iborat",
#             "testlar": {
#                 "1-savol": {
#                     "savoli": "5 + 7 = ?",
#                     "a": 10,
#                     "b": 11,
#                     "c": 12,
#                     "d": 13
#                 },
                # "2-savol": {
                #     "savoli": "9 - 4 = ?",
                #     "a": 3,
                #     "b": 4,
                #     "c": 5,
                #     "d": 6
                # },
                # "3-savol": {
                #     "savoli": "6 × 3 = ?",
                #     "a": 12,
                #     "b": 18,
                #     "c": 24,
                #     "d": 21
                # },
                # "4-savol": {
                #     "savoli": "20 ÷ 5 = ?",
                #     "a": 3,
                #     "b": 4,
                #     "c": 5,
                #     "d": 6
                # },
                # "5-savol": {
                #     "savoli": "15 + 8 = ?",
                #     "a": 22,
                #     "b": 23,
                #     "c": 24,
                #     "d": 25
                # },
#                 "6-savol": {
#                     "savoli": "12 - 7 = ?",
#                     "a": 4,
#                     "b": 5,
#                     "c": 6,
#                     "d": 7
#                 },
#                 "7-savol": {
#                     "savoli": "8 × 7 = ?",
#                     "a": 54,
#                     "b": 55,
#                     "c": 56,
#                     "d": 57
#                 },
#                 "8-savol": {
#                     "savoli": "81 ÷ 9 = ?",
#                     "a": 8,
#                     "b": 9,
#                     "c": 10,
#                     "d": 11
#                 },
#                 "9-savol": {
#                     "savoli": "14 + 19 = ?",
#                     "a": 32,
#                     "b": 33,
#                     "c": 34,
#                     "d": 35
#                 },
#                 "10-savol": {
#                     "savoli": "50 - 28 = ?",
#                     "a": 21,
#                     "b": 22,
#                     "c": 23,
#                     "d": 24
#                 }
#             }
#         }
#     }
# )
