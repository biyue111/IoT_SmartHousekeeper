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

sensor_value = { "ColumnNames": ["currentTime", "indoorTemp", "humidity", "indoorIllum", "outdoorIllum" ],
                    "Values": [ [ "value", "value" , "value", "value", "value"], ] }
user_input = { "ColumnNames": ["sleepStatus", "joyStatus" ],
                    "Values": [ [ "value", "value"], ] }

activators_state = { "ColumnNames": ["ledStatus", "coffeeStatus", "curtainStatus"],
                    "Values": [ [ "0", "0" , "0"], ] }
activators_lock_timer = { "ColumnNames": ["ledStatus", "coffeeStatus", "curtainStatus"],
                    "Values": [ [ 0, 0 , 0], ] }
lock_time = 10

