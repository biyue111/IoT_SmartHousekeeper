data_format =  {

        "Inputs": {

                "input2":
                {
                    "ColumnNames": ["temperature", "humidity"],
                    "Values": [ [ "value", "value" ], ]
                },        },
            "GlobalParameters": {
}
    }

sensor_value = { "ColumnNames": ["currentTime", "indoorTemp", "indoorHumid", "indoorIllum", "outdoorIllum" ],
                    "Values": [ [ "value", "value" , "value", "value", "value"], ] }
user_input = { "ColumnNames": ["sleepStatus", "joyStatus" ],
                    "Values": [ [ "value", "value"], ] }

activators_state = { "ColumnNames": ["ledStatus", "coffeeStatus", "curtainStatus"],
                    "Values": [ [ "value", "value" , "value"], ] }
activators_lock_timer = { "ColumnNames": ["ledStatus", "coffeeStatus", "curtainStatus"],
                    "Values": [ [ 0, 0 , 0], ] }
lock_time = 100

web_url = 'https://ussouthcentral.services.azureml.net/workspaces/0a46720be6f3493bb4c2c05f05e3e5c4/services/27176938495a45368fbb33bb7f26e1e3/execute?api-version=2.0&details=true'
api_key = 'yuhAKrw329F26sq9vXkc6JPt2kpvW0jNZYocNdHL32z3a8yM1DlCyUcbT06FkllVND2PtghZWOucvu/1r5kgYw=='
