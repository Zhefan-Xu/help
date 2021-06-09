# HELP
history-aware exploration learning planner (HELP)


# Data Collection
Run exploration in the following environments:
- Cafe
- Maze
- Apartment

Run the simulation 3 times for each environment at **DIFFERENT** start locations. Please refer to [drone_gazebo](https://github.com/Zhefan-Xu/drone_gazebo) on how to do this. 

# Data File Structure
```
Dataset
├── Env1
│   ├── Experiment 1
│       ├──color image
│          ├──img1.txt
│          └──img2.txt
│       ├──depth image
│          ├──img1.txt
│          └──img2.txt
│       └──waypoint
│          └──waypoint_file.txt
│   └── Experiment 2
│       ...
├── Env 2
│   ├── Experiment 1
│       ...
│   ├── Experiment 2
│       ...
│   └── Experiment 3
├── Env 3
│   ...
└── 
```

# Model (TODO)
<img width="1090" alt="Screen Shot 2021-06-09 at 11 46 43 PM" src="https://user-images.githubusercontent.com/55560905/121387737-7f5f9e80-c97d-11eb-8682-dddb120cf2b5.png">
