data_format =  {
  "Inputs": {
    "input1": {
      "ColumnNames": [
        "currentTime",
        "indoorTemp",
        "humidity",
        "indoorIllum",
        "outdoorIllum",
        "ledStatus",
        "coffeeStatus",
        "curtainStatus"
      ],
      "Values": [
        [
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0",
          "0"
        ],
      ]
    }
  },
  "GlobalParameters": {}
}

sensor_value = { "ColumnNames": ["currentTime", "indoorTemp", "humidity", "indoorIllum", "outdoorIllum" ],
                    "Values": [ [ "0", "0" , "0", "0", "0"], ] }
user_input = { "ColumnNames": ["sleepStatus", "joyStatus" ],
                    "Values": [ [ "0", "0"], ] }

activators_state = { "ColumnNames": ["ledStatus", "coffeeStatus", "curtainStatus"],
                    "Values": [ [ "1", "0" , "0"], ] }
activators_lock_timer = { "ColumnNames": ["ledStatus", "coffeeStatus", "curtainStatus"],
                    "Values": [ [ 0, 0 , 0], ] }
lock_time = 10

